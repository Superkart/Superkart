#!/usr/bin/env python3
"""update_readme.py — Automatically updates README.md sections with the latest
GitHub repositories fetched from the GitHub API.

Sections managed (identified by HTML comment markers):
  - Unity Game Development Portfolio   <!-- UNITY-GAMES-START/END -->
  - Learning & Practice Repositories   <!-- LEARNING-REPOS-START/END -->
  - Web Projects                        <!-- WEB-PROJECTS-START/END -->

Category rules (topics take priority over heuristics):
  unity    — topics: unity, game-development, game, unity3d
             OR language C# / ShaderLab
  learning — topics: learning, practice, tutorial, education
             OR name contains: journey, learn, practice, exercise, tutorial
             OR language C++ (non-featured)
  web      — topics: web, web-app, frontend, backend, website
             OR language TypeScript / JavaScript / HTML / CSS

Repos listed under "Featured Projects" are excluded from the auto-managed
tables so their hand-written descriptions are preserved.
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
    """Return all public, non-forked repositories for USERNAME."""
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
    """Return 'unity', 'learning', 'web', or None."""
    language = repo.get("language") or ""
    name_lower = repo["name"].lower()

    # Topics take highest priority
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
        # Non-featured C++ repos are treated as learning / practice projects
        return "learning"

    return None


# ── Table builders ─────────────────────────────────────────────────────────────
def _repo_link(name: str) -> str:
    return f"[{name}](https://github.com/{USERNAME}/{name})"


def _tech_label(repo: dict, category: str) -> str:
    language = repo.get("language") or "—"
    if category == "unity":
        return f"Unity · {language}" if language != "—" else "Unity"
    return language


def build_unity_table(entries: list[tuple[dict, set]]) -> str:
    lines = ["| Project | Description | Tech |", "|---|---|---|"]
    for repo, topics in entries:
        name = repo["name"]
        desc = (repo.get("description") or "—").strip()
        tech = _tech_label(repo, "unity")
        lines.append(f"| {_repo_link(name)} | {desc} | {tech} |")
    return "\n".join(lines)


def build_learning_table(entries: list[tuple[dict, set]]) -> str:
    lines = ["| Repo | Focus |", "|---|---|"]
    for repo, _topics in entries:
        name = repo["name"]
        desc = (repo.get("description") or "—").strip()
        lines.append(f"| {_repo_link(name)} | {desc} |")
    return "\n".join(lines)


def build_web_table(entries: list[tuple[dict, set]]) -> str:
    lines = ["| Repo | Description | Tech |", "|---|---|---|"]
    for repo, _topics in entries:
        name = repo["name"]
        desc = (repo.get("description") or "—").strip()
        tech = repo.get("language") or "—"
        lines.append(f"| {_repo_link(name)} | {desc} | {tech} |")
    return "\n".join(lines)


# ── README update ─────────────────────────────────────────────────────────────
def replace_section(content: str, start: str, end: str, new_body: str) -> str:
    """Replace the block between *start* and *end* markers with *new_body*."""
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    replacement = f"{start}\n{new_body}\n{end}"
    updated, count = pattern.subn(replacement, content)
    if count == 0:
        print(f"WARNING: markers not found — '{start}'", file=sys.stderr)
    return updated


# ── Entry point ───────────────────────────────────────────────────────────────
def main() -> None:
    print(f"Fetching repositories for {USERNAME}...")
    all_repos = get_all_repos()
    print(f"  {len(all_repos)} public repos found")

    buckets: dict[str, list[tuple[dict, set]]] = {
        "unity": [], "learning": [], "web": [],
    }

    for repo in all_repos:
        name = repo["name"]
        if name in FEATURED_REPOS or repo.get("fork") or repo.get("archived"):
            continue
        topics = get_topics(name)
        category = classify(repo, topics)
        if category in buckets:
            buckets[category].append((repo, topics))

    # Sort each bucket alphabetically by repo name for stable, reproducible output
    for key in buckets:
        buckets[key].sort(key=lambda r: r[0]["name"].lower())

    print(f"  Unity games:    {len(buckets['unity'])}")
    print(f"  Learning repos: {len(buckets['learning'])}")
    print(f"  Web projects:   {len(buckets['web'])}")

    with open(README_PATH, encoding="utf-8") as fh:
        content = fh.read()

    content = replace_section(content, *MARKERS["unity"],    build_unity_table(buckets["unity"]))
    content = replace_section(content, *MARKERS["learning"], build_learning_table(buckets["learning"]))
    content = replace_section(content, *MARKERS["web"],      build_web_table(buckets["web"]))

    with open(README_PATH, "w", encoding="utf-8") as fh:
        fh.write(content)

    print("README.md updated.")


if __name__ == "__main__":
    main()
