# How This Profile Project Works

This repository is a **self-updating GitHub profile page**.  When you visit
[github.com/Superkart](https://github.com/Superkart), GitHub renders the
`README.md` from this repository as the profile home page.  A small Python
automation script and a GitHub Actions workflow keep four sections of that
README in sync with your public repositories — completely hands-free.

---

## Repository layout

```
Superkart/               ← the "username/username" special profile repo
├── README.md            ← your profile page (rendered by GitHub)
├── scripts/
│   └── update_readme.py ← automation: fetches repos, appends new rows
├── .github/
│   └── workflows/
│       └── update-readme.yml  ← runs the script on a daily schedule
├── docs/
│   └── how-it-works.md  ← you are here
├── tests/
│   └── test_update_readme.py  ← unit tests for the automation script
├── .gitignore
└── LICENSE
```

---

## The three moving parts

### 1 · `README.md` — the profile page

This is ordinary Markdown with one special feature: **HTML comment markers**
that act as anchors for the automation script.

```
<!-- UNITY-GAMES-START -->
| Project | Description | Tech |
|---|---|---|
| [MiniTankMania](…) | … | Unity · C# |
<!-- UNITY-GAMES-END -->
```

Everything between a `*-START` / `*-END` pair is an *auto-managed section*.
Content outside those markers (the featured projects write-ups, the tech-stack
badges, the stats cards, etc.) is **never touched by the script**.

Four auto-managed sections exist today:

| Marker pair | What goes in it |
|---|---|
| `UNITY-GAMES-START/END` | Unity / game-dev repositories |
| `LEARNING-REPOS-START/END` | Learning and practice repositories |
| `WEB-PROJECTS-START/END` | Web / front-end / back-end repositories |
| `ML-AI-PROJECTS-START/END` | Machine learning and AI repositories |

### 2 · `scripts/update_readme.py` — the automation script

The script runs in five steps every time it is invoked:

```
1. Fetch all public repos  →  GitHub REST API
2. Read README.md          →  snapshot which repos are already listed
3. Classify each repo      →  unity / learning / web / ml_ai / (uncategorised)
4. Build new table rows    →  only for repos not yet in the section
5. Write README.md         →  append new rows just before the END marker
```

**Fetching repos** (`get_all_repos`)  
Paginates `GET /users/Superkart/repos` with `per_page=100` until the API
returns an empty page.

**Detecting already-linked repos** (`get_already_linked`)  
Scans a section's text for GitHub URLs matching
`https://github.com/Superkart/<name>)`.  Any name found there is considered
*already linked* and will not be appended again.

**Classifying repos** (`classify`)  
Uses a two-tier priority system:

```
Tier 1 — GitHub Topics (explicit, set by you on the repo):
  unity, game-development, game, unity3d  →  "unity"
  learning, practice, tutorial, education →  "learning"
  ml, ai, machine-learning, deep-learning,
  artificial-intelligence, data-science,
  nlp, computer-vision                    →  "ml_ai"
  web, web-app, frontend, backend, website→  "web"

Tier 2 — Heuristics (fallback when no matching topic exists):
  language C# or ShaderLab               →  "unity"
  name contains journey/learn/practice/… →  "learning"
  language Jupyter Notebook               →  "ml_ai"
  language Python + description has ML/AI terms
  (model/training/inference/dataset/…)   →  "ml_ai"
  name contains ml/ai/neural/nlp/vision/… →  "ml_ai"
  language TypeScript/JavaScript/HTML/CSS →  "web"
  language C++                           →  "learning"
```

If a repo matches none of the above it is silently skipped (no "Other"
section exists yet).

Three filters run **before** classification:

- **Featured repos** — eight repos have hand-written descriptions in the
  "Featured Projects" section.  The `FEATURED_REPOS` set keeps them out of the
  auto-managed tables so they are never duplicated.
- **Forks** — `repo["fork"] == True` → skipped.
- **Archived** — `repo["archived"] == True` → skipped.

**Building table rows** (`build_new_row`)  
Each category has its own column layout:

```
unity    →  | [Name](url) | description | Unity · Language |
learning →  | [Name](url) | description |
ml_ai    →  | [Name](url) | description | Language |
web      →  | [Name](url) | description | Language |
```

**Inserting rows** (`insert_rows_before_end`)  
New rows are inserted immediately before the `END` marker so the most
recently created repos appear at the bottom of each table.

### 3 · `.github/workflows/update-readme.yml` — the scheduler

```yaml
on:
  schedule:
    - cron: '0 0 * * *'   # every day at 00:00 UTC
  workflow_dispatch:        # or click "Run workflow" in the Actions tab
```

The workflow:
1. Checks out the repository.
2. Sets up Python 3.12 and installs `requests`.
3. Runs `python scripts/update_readme.py` (with `GITHUB_TOKEN` injected for
   authenticated API calls).
4. Commits and pushes `README.md` only if it changed (the `[skip ci]` flag in
   the commit message prevents an infinite loop of re-triggering the workflow).

---

## Running the script locally

```bash
# From the repo root
pip install requests

# Optional — avoids the 60 req/hour unauthenticated rate limit
export GITHUB_TOKEN="ghp_…your_personal_access_token…"

python scripts/update_readme.py
```

Expected output:

```
Fetching repositories for Superkart...
  42 public repos found
  New unity repos to add: 0
  New learning repos to add: 0
  New ml_ai repos to add: 0
  New web repos to add: 0
README.md updated.
```

If new repos were created since the last run the count will be non-zero and
`README.md` will be modified in place.

---

## Running the tests

```bash
pip install requests   # only external dependency
python -m unittest discover -s tests -v
```

The test suite (`tests/test_update_readme.py`) exercises every core function
in the script with in-process mocks — no network calls are made.

---

## Customising the project

### Adding a new category

1. Choose a marker name, e.g. `DATA-PROJECTS`.
2. Add the table block to `README.md`:
   ```markdown
   <!-- DATA-PROJECTS-START -->
   | Repo | Description | Tech |
   |---|---|---|
   <!-- DATA-PROJECTS-END -->
   ```
3. Add the marker pair to `MARKERS` in `update_readme.py`:
   ```python
   "data": ("<!-- DATA-PROJECTS-START -->", "<!-- DATA-PROJECTS-END -->"),
   ```
4. Add classification logic to `classify()`:
   ```python
   if topics & {"data-science", "machine-learning"}:
       return "data"
   ```
5. Add a row builder branch to `build_new_row()` if the column layout differs.

### Pinning a repo as a Featured Project

1. Write the description block in the "Featured Projects" section of `README.md`.
2. Add the repository name (exact, case-sensitive) to `FEATURED_REPOS` in
   `update_readme.py`:
   ```python
   FEATURED_REPOS: frozenset = frozenset({
       …
       "My_New_Repo",
   })
   ```

### Changing the schedule

Edit the cron expression in `.github/workflows/update-readme.yml`:

```yaml
- cron: '0 6 * * 1'   # every Monday at 06:00 UTC, for example
```

---

## Design decisions and trade-offs

| Decision | Reason |
|---|---|
| Append-only writes | Preserves all hand-written descriptions and row ordering |
| Topics over heuristics | Explicit beats guessing; add a topic to override language-based detection |
| Forks / archived filtered out | They clutter the portfolio without representing original work |
| `[skip ci]` in commit message | Prevents the daily commit from re-triggering the workflow |
| Single `requests` dependency | Keeps the environment minimal; no heavy framework needed |
