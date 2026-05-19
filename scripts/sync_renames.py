#!/usr/bin/env python3
"""sync_renames.py — Syncs README repo links with current GitHub repo names.

Approach:
  1. Fetch all current repo names from GitHub API (one bulk call).
  2. Scan README for all [display](github.com/Superkart/name) links.
  3. For each link:
     - URL name not in current repo list → renamed. Resolve via GitHub API
       redirect, update URL and display text.
     - URL name is current but display text is stale (normalised display was an
       old name that now redirects here) → update display text only.

Run manually via the "Sync Repo Renames" GitHub Actions workflow.
"""

import os
import re
import sys

import requests

USERNAME = "Superkart"
README_PATH = "README.md"

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
_BASE_HEADERS = {"Accept": "application/vnd.github+json"}
if GITHUB_TOKEN:
    _BASE_HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


def get_all_repo_names() -> set[str]:
    """Fetch all current public repo names from GitHub API."""
    names: set[str] = set()
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
        names.update(r["name"] for r in batch)
        page += 1
    return names


def get_linked(content: str) -> list[tuple[str, str]]:
    """Return deduplicated (display_text, url_name) pairs for all GitHub links."""
    pattern = re.compile(
        rf"\[([^\]]+)\]\(https://github\.com/{re.escape(USERNAME)}/([^)\"'\s]+)\)"
    )
    seen: dict[str, str] = {}
    for m in pattern.finditer(content):
        display, name = m.group(1), m.group(2)
        if name not in seen:
            seen[name] = display
    return [(display, name) for name, display in seen.items()]


def resolve_renamed(old_name: str) -> str | None:
    """Call GitHub API; return new name if old_name was renamed, else None."""
    resp = requests.get(
        f"https://api.github.com/repos/{USERNAME}/{old_name}",
        headers=_BASE_HEADERS,
        timeout=10,
        allow_redirects=True,
    )
    if resp.status_code == 404:
        print(f"  WARNING: '{old_name}' not found (deleted or private?)", file=sys.stderr)
        return None
    if not resp.ok:
        print(f"  WARNING: '{old_name}' returned HTTP {resp.status_code}", file=sys.stderr)
        return None
    current = resp.json().get("name", old_name)
    return current if current != old_name else None


def is_stale_display(display: str, url_name: str) -> bool:
    """Return True if display is a stale humanized old name that now redirects to url_name."""
    normalized = display.replace(" ", "_").replace("-", "_")
    if normalized == url_name:
        return False
    resp = requests.get(
        f"https://api.github.com/repos/{USERNAME}/{normalized}",
        headers=_BASE_HEADERS,
        timeout=10,
        allow_redirects=True,
    )
    if not resp.ok:
        return False
    return resp.json().get("name", "") == url_name


def apply_update(content: str, old_url_name: str, new_url_name: str, new_display: str) -> str:
    old_url = f"https://github.com/{USERNAME}/{old_url_name}"
    new_url = f"https://github.com/{USERNAME}/{new_url_name}"
    content = content.replace(old_url, new_url)
    content = re.sub(
        rf"\[([^\]]+)\]\({re.escape(new_url)}\)",
        f"[{new_display}]({new_url})",
        content,
    )
    return content


def main() -> None:
    print("Fetching current repo names from GitHub...")
    current_names = get_all_repo_names()
    print(f"  {len(current_names)} repos found")

    with open(README_PATH, encoding="utf-8") as fh:
        content = fh.read()

    linked = get_linked(content)
    print(f"Checking {len(linked)} linked repo(s)...")

    updates: list[tuple[str, str, str]] = []  # (old_url_name, new_url_name, new_display)

    for display, url_name in linked:
        if url_name not in current_names:
            # Repo missing from current list — likely renamed
            new_name = resolve_renamed(url_name)
            if new_name:
                human = new_name.replace("_", " ").replace("-", " ")
                updates.append((url_name, new_name, human))
                print(f"  Renamed: {url_name} -> {new_name}")
        else:
            # URL name is current — check if display text is stale
            human = url_name.replace("_", " ").replace("-", " ")
            if display in (human, url_name):
                continue
            if is_stale_display(display, url_name):
                updates.append((url_name, url_name, human))
                print(f"  Stale display: [{display}] -> [{human}] for /{url_name}")

    if not updates:
        print("No changes needed — README.md unchanged.")
        return

    for old_url_name, new_url_name, new_display in updates:
        content = apply_update(content, old_url_name, new_url_name, new_display)

    with open(README_PATH, "w", encoding="utf-8") as fh:
        fh.write(content)

    print(f"\nREADME.md updated — {len(updates)} change(s) applied.")


if __name__ == "__main__":
    main()
