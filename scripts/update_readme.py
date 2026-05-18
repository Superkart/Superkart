#!/usr/bin/env python3
"""update_readme.py — Automatically appends newly-created GitHub repositories
to the relevant table sections in README.md.

Classification pipeline (in priority order):
  1. GitHub topics  → exact match against each category's topics set
  2. Language / name heuristics  → language and name-based rules
  3. AI classification via GitHub Models (free with GITHUB_TOKEN)
  4. 'other' catch-all  → nothing is silently dropped

Categories are defined in CATEGORIES below. To add a new one:
  1. Add an entry to CATEGORIES with the required fields.
  2. Add matching <!-- KEY-START --> / <!-- KEY-END --> markers to README.md.

Existing rows are NEVER modified — append-only.
Repos already linked anywhere in the README are skipped entirely.
Repos in FEATURED_REPOS are excluded from all auto-managed tables.
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

FEATURED_REPOS: frozenset = frozenset({
    # Hand-written featured entries — excluded from all auto-managed tables.
    # Update REPO_NAME values once those repos are created on GitHub.
    "Steam_Accountabilibuddy",
    "Immersive_Cosmology_Explorer",
    "Drone_Simulator",
    "Incident_Response_Agent",
    "RequirementsEngineering_Agents",
    USERNAME,
})

# ── Category definitions ──────────────────────────────────────────────────────
# Add a new category by adding an entry here + markers in README.md.
# 'columns' controls the table shape: 3 items → 3-column row, 2 items → 2-column row.
CATEGORIES: dict[str, dict] = {
    "unity": {
        "name": "Game Development",
        "start": "<!-- UNITY-GAMES-START -->",
        "end":   "<!-- UNITY-GAMES-END -->",
        "columns": ["Project", "Description", "Tech"],
        "topics": {"unity", "game-development", "game", "unity3d"},
        "languages": {"C#", "ShaderLab"},
        "ai_description": (
            "Unity game development, C#, ShaderLab, game engines, "
            "interactive simulations, 2D/3D games"
        ),
    },
    "web": {
        "name": "Web Projects",
        "start": "<!-- WEB-PROJECTS-START -->",
        "end":   "<!-- WEB-PROJECTS-END -->",
        "columns": ["Repo", "Description", "Tech"],
        "topics": {"web", "web-app", "frontend", "website", "react", "astro", "svelte", "nextjs"},
        "languages": {"TypeScript", "JavaScript", "HTML", "CSS", "Astro"},
        "ai_description": (
            "Web applications, frontend, full-stack web, React, Astro, Angular, "
            "HTML/CSS/TypeScript/JavaScript — NOT backend-only services"
        ),
    },
    "backend": {
        "name": "Backend & APIs",
        "start": "<!-- BACKEND-START -->",
        "end":   "<!-- BACKEND-END -->",
        "columns": ["Repo", "Description", "Tech"],
        "topics": {"backend", "api", "rest-api", "spring-boot", "microservices", "server", "grpc"},
        "languages": {"Java", "Go", "Rust", "Kotlin", "Scala", "PHP", "Ruby"},
        "ai_description": (
            "Backend services, REST APIs, Spring Boot, Java server-side, Go servers, "
            "Rust servers, microservices, gRPC, databases — server-side only"
        ),
    },
    "data_eng": {
        "name": "Data Engineering",
        "start": "<!-- DATA-ENG-START -->",
        "end":   "<!-- DATA-ENG-END -->",
        "columns": ["Repo", "Description", "Tech"],
        "topics": {
            "data-engineering", "etl", "pipeline", "data-pipeline",
            "spark", "airflow", "kafka", "data-processing", "dbt",
        },
        "languages": set(),
        "ai_description": (
            "Data pipelines, ETL, data processing, Apache Spark, Airflow, Kafka, "
            "data warehousing, ingestion, batch/stream processing — "
            "NOT machine learning or AI model training"
        ),
    },
    "ml_ai": {
        "name": "ML & AI Projects",
        "start": "<!-- ML-AI-PROJECTS-START -->",
        "end":   "<!-- ML-AI-PROJECTS-END -->",
        "columns": ["Repo", "Description", "Tech"],
        "topics": {
            "ml", "ai", "machine-learning", "deep-learning",
            "artificial-intelligence", "data-science", "nlp", "computer-vision", "llm",
        },
        "languages": {"Jupyter Notebook"},
        "ai_description": (
            "Machine learning, deep learning, AI, neural networks, NLP, "
            "computer vision, LLMs, data science models, training, inference, datasets"
        ),
    },
    "systems": {
        "name": "Systems & Robotics",
        "start": "<!-- SYSTEMS-START -->",
        "end":   "<!-- SYSTEMS-END -->",
        "columns": ["Repo", "Description", "Tech"],
        "topics": {
            "robotics", "simulation", "autonomous", "embedded",
            "systems-programming", "drone", "ros", "unreal-engine",
        },
        "languages": {"C++", "C"},
        "ai_description": (
            "Systems programming, robotics, simulation, autonomous vehicles/drones, "
            "C/C++, embedded systems, AirSim, Unreal Engine, ROS, low-level programming"
        ),
    },
    "learning": {
        "name": "Learning & Practice",
        "start": "<!-- LEARNING-REPOS-START -->",
        "end":   "<!-- LEARNING-REPOS-END -->",
        "columns": ["Repo", "Focus"],
        "topics": {"learning", "practice", "tutorial", "education", "exercises", "leetcode"},
        "languages": set(),
        "ai_description": (
            "Learning repositories, practice exercises, tutorials, educational projects, "
            "coding challenges, LeetCode, following along with courses"
        ),
    },
    "other": {
        "name": "Other Projects",
        "start": "<!-- OTHER-PROJECTS-START -->",
        "end":   "<!-- OTHER-PROJECTS-END -->",
        "columns": ["Repo", "Description", "Tech"],
        "topics": set(),
        "languages": set(),
        "ai_description": "",  # catch-all — not used for AI prompting
    },
}

# ── Keyword sets used by heuristics ───────────────────────────────────────────
_ML_AI_DESC_KEYWORDS: frozenset = frozenset({
    "machine learning", "deep learning", "artificial intelligence",
    "neural", "transformer", "llm", "nlp", "computer vision",
    "model training", "inference", "dataset", "classifier",
})

_DATA_ENG_DESC_KEYWORDS: frozenset = frozenset({
    "pipeline", "etl", "data engineering", "data pipeline",
    "airflow", "spark", "kafka", "warehouse", "ingestion",
    "batch processing", "stream processing", "dbt",
})

_LEARNING_NAME_KEYWORDS: frozenset = frozenset({
    "journey", "learn", "practice", "exercise", "tutorial",
})


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
            f"(HTTP {resp.status_code}) — skipping topics",
            file=sys.stderr,
        )
        return set()
    return set(resp.json().get("names", []))


# ── Classification ────────────────────────────────────────────────────────────
def _classify_by_heuristics(repo: dict, topics: set[str]) -> str | None:
    """Return a category key via topic/language/name rules, or None if no match."""
    language = repo.get("language") or ""
    name_lower = repo["name"].lower()
    desc_lower = (repo.get("description") or "").lower()

    # 1. GitHub topics — highest priority, beats everything below
    for key, cat in CATEGORIES.items():
        if key == "other":
            continue
        if topics & cat["topics"]:
            return key

    # 2. Name-based learning heuristic — beats language (e.g. Cpp_Journey → learning, not systems)
    if any(k in name_lower for k in _LEARNING_NAME_KEYWORDS):
        return "learning"

    # 3. Explicit language → category mappings
    for key in ("unity", "web", "backend", "systems", "ml_ai"):
        if language in CATEGORIES[key]["languages"]:
            return key

    # 4. Python needs description keywords to disambiguate data-eng vs ml_ai
    if language == "Python":
        has_data = any(k in desc_lower for k in _DATA_ENG_DESC_KEYWORDS)
        has_ml = any(k in desc_lower for k in _ML_AI_DESC_KEYWORDS)
        if has_data and not has_ml:
            return "data_eng"
        if has_ml:
            return "ml_ai"

    return None


def classify_with_ai(repo: dict, topics: set[str]) -> str | None:
    """Classify using GitHub Models (free with GITHUB_TOKEN). Returns category key or None."""
    if not GITHUB_TOKEN:
        return None

    try:
        from openai import OpenAI  # noqa: PLC0415
    except ImportError:
        print("WARNING: openai package not installed — skipping AI classification", file=sys.stderr)
        return None

    options = "\n".join(
        f'"{key}": {cat["ai_description"]}'
        for key, cat in CATEGORIES.items()
        if key != "other" and cat["ai_description"]
    )
    prompt = (
        "Classify this GitHub repository into exactly one of the listed categories.\n\n"
        f"Repository:\n"
        f"  Name: {repo['name']}\n"
        f"  Language: {repo.get('language') or 'unknown'}\n"
        f"  Description: {repo.get('description') or 'none'}\n"
        f"  Topics: {', '.join(topics) or 'none'}\n\n"
        f"Categories:\n{options}\n"
        '"other": does not fit any category above\n\n'
        'Reply with ONLY the category key (e.g. "web"), nothing else.'
    )

    try:
        client = OpenAI(base_url="https://models.inference.ai.azure.com", api_key=GITHUB_TOKEN)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0,
        )
        result = response.choices[0].message.content.strip().lower().strip("\"'")
        return result if result in CATEGORIES else "other"
    except Exception as exc:
        print(f"WARNING: AI classification failed for '{repo['name']}': {exc}", file=sys.stderr)
        return None


def classify(repo: dict, topics: set[str]) -> str:
    """Return a category key. Always returns a valid key — falls back to 'other'."""
    result = _classify_by_heuristics(repo, topics)
    if result:
        return result
    print(f"  [AI] classifying '{repo['name']}'...", file=sys.stderr)
    return classify_with_ai(repo, topics) or "other"


# ── README helpers ────────────────────────────────────────────────────────────
def get_already_linked(content: str, start: str, end: str) -> set[str]:
    """Return repo names whose GitHub URLs appear inside a section."""
    pattern = re.compile(re.escape(start) + r"(.*?)" + re.escape(end), re.DOTALL)
    m = pattern.search(content)
    if not m:
        print(f"WARNING: markers not found — '{start}'", file=sys.stderr)
        return set()
    link_re = re.compile(rf"https://github\.com/{re.escape(USERNAME)}/([^)]+)\)")
    return {lm.group(1) for lm in link_re.finditer(m.group(1))}


def build_new_row(repo: dict, category: str) -> str:
    """Build a Markdown table row for a new repo, matching each section's column style."""
    cat = CATEGORIES[category]
    name = repo["name"]
    url = f"https://github.com/{USERNAME}/{name}"
    desc = (repo.get("description") or "—").strip()
    language = repo.get("language") or "—"

    if len(cat["columns"]) == 3:
        tech = (f"Unity · {language}" if language != "—" else "Unity") if category == "unity" else language
        return f"| [{name}]({url}) | {desc} | {tech} |"
    return f"| [{name}]({url}) | {desc} |"


def insert_rows_before_end(content: str, end_marker: str, new_rows: list[str]) -> str:
    """Insert new_rows immediately before end_marker, preserving everything else."""
    rows_text = "\n".join(new_rows) + "\n"
    return content.replace(end_marker, rows_text + end_marker, 1)


# ── Entry point ───────────────────────────────────────────────────────────────
def main() -> None:
    print(f"Fetching repositories for {USERNAME}...")
    all_repos = get_all_repos()
    print(f"  {len(all_repos)} public repos found")

    with open(README_PATH, encoding="utf-8") as fh:
        content = fh.read()

    # Build per-section and global already-linked sets
    already_linked: dict[str, set[str]] = {
        cat: get_already_linked(content, CATEGORIES[cat]["start"], CATEGORIES[cat]["end"])
        for cat in CATEGORIES
    }
    all_linked: set[str] = set().union(*already_linked.values())

    new_rows: dict[str, list[str]] = {cat: [] for cat in CATEGORIES}

    for repo in all_repos:
        name = repo["name"]
        if name in FEATURED_REPOS or repo.get("fork") or repo.get("archived"):
            continue
        if name in all_linked:
            continue
        topics = get_topics(name)
        category = classify(repo, topics)
        new_rows[category].append(build_new_row(repo, category))
        print(f"  [{CATEGORIES[category]['name']}] + {name}")

    for cat, rows in new_rows.items():
        if rows:
            content = insert_rows_before_end(content, CATEGORIES[cat]["end"], rows)

    with open(README_PATH, "w", encoding="utf-8") as fh:
        fh.write(content)

    total = sum(len(r) for r in new_rows.values())
    print(f"\nREADME.md updated — {total} new row(s) added.")

    other_count = len(new_rows.get("other", []))
    if other_count:
        print(
            f"  NOTE: {other_count} repo(s) landed in 'Other Projects'. "
            "Add GitHub topics to them for better auto-categorisation.",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
