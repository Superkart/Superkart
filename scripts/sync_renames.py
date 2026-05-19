#!/usr/bin/env python3
"""sync_renames.py — Detects renamed GitHub repos and updates their URLs in README.md.

For every repo URL currently linked in the README, calls the GitHub API.
If the repo was renamed, the API returns the new name — the script updates
both the URL and the display text (when the display text matches the old
repo name exactly, which is always true for auto-managed table rows).

Hand-written display names in Featured Projects are left untouched because
they rarely match the raw repo name.

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


def get_linked_names(content: str) -> list[str]:
    """Return deduplicated repo names extracted from all GitHub URLs in README."""
    pattern = re.compile(rf"https://github\.com/{re.escape(USERNAME)}/([^)\"'\s]+)\)")
    return list(dict.fromkeys(pattern.findall(content)))


def check_rename(old_name: str) -> str | None:
    """Return the current repo name if it differs from old_name, else None."""
    resp = requests.get(
        f"https://api.github.com/repos/{USERNAME}/{old_name}",
        headers=_BASE_HEADERS,
        timeout=10,
        allow_redirects=True,
    )
    if resp.status_code == 404:
        print(f"  WARNING: '{old_name}' not found (deleted or made private?)", file=sys.stderr)
        return None
    if not resp.ok:
        print(f"  WARNING: '{old_name}' returned HTTP {resp.status_code}", file=sys.stderr)
        return None
    current = resp.json().get("name", old_name)
    return current if current != old_name else None


def apply_rename(content: str, old_name: str, new_name: str) -> str:
    old_url = f"https://github.com/{USERNAME}/{old_name}"
    new_url = f"https://github.com/{USERNAME}/{new_name}"

    # Update every occurrence of the old URL
    content = content.replace(old_url, new_url)

    # Update display text when it exactly matches the old repo name (auto-managed rows)
    content = re.sub(
        rf"\[{re.escape(old_name)}\]\({re.escape(new_url)}\)",
        f"[{new_name}]({new_url})",
        content,
    )

    # Update display text in featured headings even when it doesn't match the raw
    # repo name — e.g. "### 🚁 [Drone Simulator](url)" where display ≠ "Drone_Simulator".
    # Replace [Any Display Text](new_url) with [new_name humanised](new_url).
    human_name = new_name.replace("_", " ").replace("-", " ")
    content = re.sub(
        rf"\[([^\]]+)\]\({re.escape(new_url)}\)",
        f"[{human_name}]({new_url})",
        content,
    )
    return content


def main() -> None:
    with open(README_PATH, encoding="utf-8") as fh:
        content = fh.read()

    linked = get_linked_names(content)
    print(f"Checking {len(linked)} linked repo(s) for renames...")

    renames: dict[str, str] = {}
    for name in linked:
        new_name = check_rename(name)
        if new_name:
            renames[name] = new_name

    if not renames:
        print("No renames detected — README.md unchanged.")
        return

    for old, new in renames.items():
        content = apply_rename(content, old, new)
        print(f"  {old} → {new}")

    with open(README_PATH, "w", encoding="utf-8") as fh:
        fh.write(content)

    print(f"\nREADME.md updated — {len(renames)} rename(s) applied.")


if __name__ == "__main__":
    main()
