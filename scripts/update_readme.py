#!/usr/bin/env python3
"""update_readme.py — Automatically appends newly-created GitHub repositories
to the relevant table sections in README.md.

Existing rows are NEVER modified — the script only appends rows for repos that
do not yet have a link inside the section.  This preserves all hand-written
display names, descriptions, and row ordering exactly as the author left them.

Sections managed (identified by HTML comment markers):
  - Unity Game Development Portfolio   <!-- UNITY-GAMES-START/END -->
  - Learning & Practice Repositories   <!-- LEARNING-REPOS-START/END -->
  - Web Projects                        <!-- WEB-PROJECTS-START/END -->
    - ML & AI Projects                     <!-- ML-AI-PROJECTS-START/END -->

Category rules (topics take priority over heuristics):
  unity    — topics: unity, game-development, game, unity3d
             OR language C# / ShaderLab
  learning — topics: learning, practice, tutorial, education
             OR name contains: journey, learn, practice, exercise, tutorial
             OR language C++
    ml_ai    — topics: ml, ai, machine-learning, deep-learning,
                         artificial-intelligence, data-science, nlp, computer-vision
                         OR language Jupyter Notebook
                 OR language Python + description contains ML/AI terms
                         OR name contains: ml, ai, machine-learning, deep-learning,
                         neural, nlp, vision, datascience
  web      — topics: web, web-app, frontend, backend, website
             OR language TypeScript / JavaScript / HTML / CSS

Repos listed under "Featured Projects" are excluded from all auto-managed
tables so their hand-written descriptions are never touched.  Use
validate_featured_repos() to check for drift between FEATURED_REPOS and the
README featured section.
"""

import os
import re
import sys

import requests

# ── Configuration ─────────────────────────────────────────────────────────────
USERNAME = "Superkart"
README_PATH = "README.md"

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
_BASE_HEADERS = {"Accept": "application/vnd.github+json"}
if GITHUB_TOKEN:
    _BASE_HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"

# Repos whose entries are hand-written in the "Featured Projects" section.
# They are intentionally excluded from the auto-managed tables below.
# A project belongs here when it has a substantial, hand-authored description
# in the "Featured Projects" section of README.md.  Use validate_featured_repos()
# to detect any drift between this set and the README.
FEATURED_REPOS: frozenset = frozenset({
    "Steam_Accountabilibuddy",
    "Immersive_Cosmology_Explorer",
    "Pandas_Provenance",
    "Store_Spring_Boot",
    "AirSimApiCpp",
    "Drone_Simulator",
    "PuglleRunner-",
    "Reddit_Moderator_Tool",
    "The-Lost-Isle",
    USERNAME,  # the profile repo itself
})

# Marker that separates the hand-written Featured Projects section from the
# auto-managed tables.  Everything before this line is considered "featured".
FEATURED_SECTION_END_MARKER = "<!-- UNITY-GAMES-START -->"

# Section markers — these must match the markers inside README.md exactly.
MARKERS: dict[str, tuple[str, str]] = {
    "unity":    ("<!-- UNITY-GAMES-START -->",   "<!-- UNITY-GAMES-END -->"),
    "learning": ("<!-- LEARNING-REPOS-START -->", "<!-- LEARNING-REPOS-END -->"),
    "web":      ("<!-- WEB-PROJECTS-START -->",   "<!-- WEB-PROJECTS-END -->"),
    "ml_ai":    ("<!-- ML-AI-PROJECTS-START -->", "<!-- ML-AI-PROJECTS-END -->"),
}


# ── GitHub API helpers ────────────────────────────────────────────────────────
def get_all_repos() -> list[dict]:
    """Return all public repositories for USERNAME."""
    repos: list[dict] = []
    page = 1
    while True:
        resp = requests.get(
            f"https://api.github.com/users/{USERNAME}/repos",
            params={"per_page": 100, "page": page, "type": "public"},
            headers=_BASE_HEADERS,
            timeout=30,
        )
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        repos.extend(batch)
        page += 1
    return repos


def get_topics(repo_name: str) -> set[str]:
    """Return the set of topics for a repository."""
    resp = requests.get(
        f"https://api.github.com/repos/{USERNAME}/{repo_name}/topics",
        headers={**_BASE_HEADERS, "Accept": "application/vnd.github.mercy-preview+json"},
        timeout=10,
    )
    if not resp.ok:
        print(
            f"WARNING: could not fetch topics for '{repo_name}' "
            f"(HTTP {resp.status_code}) — falling back to heuristics",
            file=sys.stderr,
        )
        return set()
    return set(resp.json().get("names", []))


# ── Categorisation ────────────────────────────────────────────────────────────
def classify(repo: dict, topics: set[str]) -> str | None:
    """Return 'unity', 'learning', 'web', 'ml_ai', or None if uncategorised."""
    language = repo.get("language") or ""
    name_lower = repo["name"].lower()
    description_lower = (repo.get("description") or "").lower()

    # Topics take highest priority (explicit beats heuristic)
    if topics & {"unity", "game-development", "game", "unity3d"}:
        return "unity"
    if topics & {"learning", "practice", "tutorial", "education"}:
        return "learning"
    if topics & {
        "ml",
        "ai",
        "machine-learning",
        "deep-learning",
        "artificial-intelligence",
        "data-science",
        "nlp",
        "computer-vision",
    }:
        return "ml_ai"
    if topics & {"web", "web-app", "frontend", "backend", "website"}:
        return "web"

    # Language / name heuristics
    if language in ("C#", "ShaderLab"):
        return "unity"
    if language == "Jupyter Notebook":
        return "ml_ai"
    if language == "Python" and any(
        k in description_lower
        for k in (
            "machine learning",
            "deep learning",
            "artificial intelligence",
            "ai",
            "ml",
            "model",
            "training",
            "inference",
            "dataset",
            "transformer",
            "neural",
            "computer vision",
            "nlp",
        )
    ):
        return "ml_ai"
    if any(
        k in name_lower
        for k in (
            "machine-learning",
            "deep-learning",
            "datascience",
            "data-science",
            "neural",
            "vision",
            "nlp",
            "_ml",
            "-ml",
            "_ai",
            "-ai",
        )
    ) and language != "Python":
        return "ml_ai"
    if any(k in name_lower for k in ("journey", "learn", "practice", "exercise", "tutorial")):
        return "learning"
    if language in ("TypeScript", "JavaScript", "HTML", "CSS"):
        return "web"
    if language == "C++":
        return "learning"

    return None


# ── Already-linked repo detection ─────────────────────────────────────────────
def get_already_linked(content: str, start: str, end: str) -> set[str]:
    """Return the repo names whose GitHub URLs appear inside a section."""
    pattern = re.compile(re.escape(start) + r"(.*?)" + re.escape(end), re.DOTALL)
    m = pattern.search(content)
    if not m:
        print(f"WARNING: markers not found — '{start}'", file=sys.stderr)
        return set()
    section_body = m.group(1)
    link_re = re.compile(rf"https://github\.com/{re.escape(USERNAME)}/([^)]+)\)")
    return {lm.group(1) for lm in link_re.finditer(section_body)}


# ── New-row builders ──────────────────────────────────────────────────────────
def _tech_label(repo: dict, category: str) -> str:
    language = repo.get("language") or "—"
    if category == "unity":
        return f"Unity · {language}" if language != "—" else "Unity"
    return language


def build_new_row(repo: dict, category: str) -> str:
    """Build a single table row for a brand-new repo, matching existing style."""
    name = repo["name"]
    url = f"https://github.com/{USERNAME}/{name}"
    desc = (repo.get("description") or "—").strip()
    if category == "unity":
        return f"| [{name}]({url}) | {desc} | {_tech_label(repo, 'unity')} |"
    if category == "learning":
        return f"| [{name}]({url}) | {desc} |"
    if category == "ml_ai":
        tech = repo.get("language") or "—"
        return f"| [{name}]({url}) | {desc} | {tech} |"
    # web
    tech = repo.get("language") or "—"
    return f"| [{name}]({url}) | {desc} | {tech} |"


# ── Featured-projects integrity check ────────────────────────────────────────
def validate_featured_repos(content: str) -> list[str]:
    """Return a list of warning strings for any FEATURED_REPOS/README mismatch.

    A project is considered worthy of the Featured Projects section when it has
    a hand-written entry (i.e. its GitHub URL appears in the text before the
    first auto-managed table marker).  This function reports:
      • repos in FEATURED_REPOS that have no hand-written entry in README.md
      • repos with a hand-written featured entry that are not in FEATURED_REPOS
        (they would be duplicated by the auto-managed tables)

    The check intentionally excludes the profile repo (USERNAME) because that
    repo represents the README itself and needs no featured entry.
    """
    featured_text_end = content.find(FEATURED_SECTION_END_MARKER)
    if featured_text_end == -1:
        return [f"WARNING: '{FEATURED_SECTION_END_MARKER}' not found in README — skipping featured validation"]

    featured_section = content[:featured_text_end]
    link_re = re.compile(rf"https://github\.com/{re.escape(USERNAME)}/([^\s)]+)")
    linked_repos: set[str] = {m.group(1) for m in link_re.finditer(featured_section)}

    expected = FEATURED_REPOS - {USERNAME}
    warnings: list[str] = []
    for repo in sorted(expected - linked_repos):
        warnings.append(
            f"WARNING: '{repo}' is in FEATURED_REPOS but has no hand-written entry in the Featured Projects section"
        )
    for repo in sorted(linked_repos - expected):
        warnings.append(
            f"WARNING: '{repo}' has a featured entry in README.md but is not in FEATURED_REPOS — "
            "it may be duplicated by the auto-managed tables"
        )
    return warnings


# ── README update (append-only) ───────────────────────────────────────────────
def insert_rows_before_end(content: str, end_marker: str, new_rows: list[str]) -> str:
    """Insert *new_rows* immediately before *end_marker*, preserving everything else."""
    rows_text = "\n".join(new_rows) + "\n"
    return content.replace(end_marker, rows_text + end_marker, 1)


# ── Entry point ───────────────────────────────────────────────────────────────
def main() -> None:
    print(f"Fetching repositories for {USERNAME}...")
    all_repos = get_all_repos()
    print(f"  {len(all_repos)} public repos found")

    with open(README_PATH, encoding="utf-8") as fh:
        content = fh.read()

    for warning in validate_featured_repos(content):
        print(warning, file=sys.stderr)

    # Snapshot which repos are already represented in each section
    already_linked: dict[str, set[str]] = {
        cat: get_already_linked(content, *markers)
        for cat, markers in MARKERS.items()
    }

    new_rows: dict[str, list[str]] = {
        "unity": [],
        "learning": [],
        "web": [],
        "ml_ai": [],
    }

    for repo in all_repos:
        name = repo["name"]
        if name in FEATURED_REPOS or repo.get("fork") or repo.get("archived"):
            continue
        topics = get_topics(name)
        category = classify(repo, topics)
        if category not in new_rows:
            continue
        if name not in already_linked[category]:
            new_rows[category].append(build_new_row(repo, category))

    for cat, rows in new_rows.items():
        print(f"  New {cat} repos to add: {len(rows)}")
        if rows:
            content = insert_rows_before_end(content, MARKERS[cat][1], rows)

    with open(README_PATH, "w", encoding="utf-8") as fh:
        fh.write(content)

    print("README.md updated.")


if __name__ == "__main__":
    main()
