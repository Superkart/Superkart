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

Category rules (topics take priority over heuristics):
  unity    — topics: unity, game-development, game, unity3d
             OR language C# / ShaderLab
  learning — topics: learning, practice, tutorial, education
             OR name contains: journey, learn, practice, exercise, tutorial
             OR language C++
  web      — topics: web, web-app, frontend, backend, website
             OR language TypeScript / JavaScript / HTML / CSS

Repos listed under "Featured Projects" are excluded from all auto-managed
tables so their hand-written descriptions are never touched.
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
FEATURED_REPOS: frozenset = frozenset({
    "Steam_Accountabilibuddy",
    "Immersive_Cosmology_Explorer",
    "Pandas_Provenance",
    "Student_Survey_Analysis",
    "Store_Spring_Boot",
    "AirSimApiCpp",
    "ARModelViewer",
    USERNAME,  # the profile repo itself
})

# Section markers — these must match the markers inside README.md exactly.
MARKERS: dict[str, tuple[str, str]] = {
    "unity":    ("<!-- UNITY-GAMES-START -->",   "<!-- UNITY-GAMES-END -->"),
    "learning": ("<!-- LEARNING-REPOS-START -->", "<!-- LEARNING-REPOS-END -->"),
    "web":      ("<!-- WEB-PROJECTS-START -->",   "<!-- WEB-PROJECTS-END -->"),
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
    """Return 'unity', 'learning', 'web', or None if uncategorised."""
    language = repo.get("language") or ""
    name_lower = repo["name"].lower()

    # Topics take highest priority (explicit beats heuristic)
    if topics & {"unity", "game-development", "game", "unity3d"}:
        return "unity"
    if topics & {"learning", "practice", "tutorial", "education"}:
        return "learning"
    if topics & {"web", "web-app", "frontend", "backend", "website"}:
        return "web"

    # Language / name heuristics
    if language in ("C#", "ShaderLab"):
        return "unity"
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
    # web
    tech = repo.get("language") or "—"
    return f"| [{name}]({url}) | {desc} | {tech} |"


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

    # Snapshot which repos are already represented in each section
    already_linked: dict[str, set[str]] = {
        cat: get_already_linked(content, *markers)
        for cat, markers in MARKERS.items()
    }

    new_rows: dict[str, list[str]] = {"unity": [], "learning": [], "web": []}

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
