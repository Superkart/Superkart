"""Unit tests for scripts/update_readme.py.

All tests run fully in-process — no network calls are made.
The GitHub API helpers (get_all_repos, get_topics) are tested via
monkeypatching / mocking at the call-site; the pure-logic helpers are
tested directly with hand-crafted inputs.
"""

import sys
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

# ---------------------------------------------------------------------------
# Make the scripts package importable without a package __init__.py
# ---------------------------------------------------------------------------
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import update_readme  # noqa: E402  (import after sys.path mutation)


# ---------------------------------------------------------------------------
# Helpers used across several tests
# ---------------------------------------------------------------------------

def _repo(name, language=None, description=None, fork=False, archived=False):
    """Build a minimal repo dict that mirrors the GitHub API response shape."""
    return {
        "name": name,
        "language": language,
        "description": description,
        "fork": fork,
        "archived": archived,
    }


# ---------------------------------------------------------------------------
# classify()
# ---------------------------------------------------------------------------

class TestClassify(unittest.TestCase):
    """Verify the two-tier classification logic (topics → heuristics)."""

    # ── Topic-based (tier 1) ────────────────────────────────────────────────

    def test_unity_topic_takes_priority_over_language(self):
        repo = _repo("MyGame", language="Python")
        self.assertEqual(update_readme.classify(repo, {"unity"}), "unity")

    def test_game_development_topic_maps_to_unity(self):
        repo = _repo("TankGame", language=None)
        self.assertEqual(update_readme.classify(repo, {"game-development"}), "unity")

    def test_unity3d_topic_maps_to_unity(self):
        repo = _repo("PlatformerX", language=None)
        self.assertEqual(update_readme.classify(repo, {"unity3d"}), "unity")

    def test_game_topic_maps_to_unity(self):
        repo = _repo("Shooter", language="C#")
        self.assertEqual(update_readme.classify(repo, {"game"}), "unity")

    def test_learning_topic_takes_priority(self):
        repo = _repo("PyNotes", language="TypeScript")
        self.assertEqual(update_readme.classify(repo, {"learning"}), "learning")

    def test_practice_topic_maps_to_learning(self):
        repo = _repo("Exercises", language=None)
        self.assertEqual(update_readme.classify(repo, {"practice"}), "learning")

    def test_tutorial_topic_maps_to_learning(self):
        repo = _repo("Guided", language=None)
        self.assertEqual(update_readme.classify(repo, {"tutorial"}), "learning")

    def test_education_topic_maps_to_learning(self):
        repo = _repo("CS101", language=None)
        self.assertEqual(update_readme.classify(repo, {"education"}), "learning")

    def test_web_topic_maps_to_web(self):
        repo = _repo("SiteX", language=None)
        self.assertEqual(update_readme.classify(repo, {"web"}), "web")

    def test_frontend_topic_maps_to_web(self):
        repo = _repo("Dashboard", language="Python")
        self.assertEqual(update_readme.classify(repo, {"frontend"}), "web")

    def test_backend_topic_maps_to_web(self):
        repo = _repo("API", language=None)
        self.assertEqual(update_readme.classify(repo, {"backend"}), "web")

    def test_website_topic_maps_to_web(self):
        repo = _repo("Landing", language=None)
        self.assertEqual(update_readme.classify(repo, {"website"}), "web")

    def test_web_app_topic_maps_to_web(self):
        repo = _repo("App", language=None)
        self.assertEqual(update_readme.classify(repo, {"web-app"}), "web")

    # ── Language / name heuristics (tier 2) ────────────────────────────────

    def test_csharp_language_maps_to_unity(self):
        repo = _repo("UnityProject", language="C#")
        self.assertEqual(update_readme.classify(repo, set()), "unity")

    def test_shaderlabs_language_maps_to_unity(self):
        repo = _repo("Shader", language="ShaderLab")
        self.assertEqual(update_readme.classify(repo, set()), "unity")

    def test_name_journey_maps_to_learning(self):
        repo = _repo("Python_Journey", language=None)
        self.assertEqual(update_readme.classify(repo, set()), "learning")

    def test_name_learn_maps_to_learning(self):
        repo = _repo("LearnRust", language=None)
        self.assertEqual(update_readme.classify(repo, set()), "learning")

    def test_name_practice_maps_to_learning(self):
        repo = _repo("practice-problems", language=None)
        self.assertEqual(update_readme.classify(repo, set()), "learning")

    def test_name_exercise_maps_to_learning(self):
        repo = _repo("exercise-tracker", language=None)
        self.assertEqual(update_readme.classify(repo, set()), "learning")

    def test_name_tutorial_maps_to_learning(self):
        repo = _repo("flask-tutorial", language=None)
        self.assertEqual(update_readme.classify(repo, set()), "learning")

    def test_cpp_language_maps_to_learning(self):
        repo = _repo("CppNotes", language="C++")
        self.assertEqual(update_readme.classify(repo, set()), "learning")

    def test_typescript_maps_to_web(self):
        repo = _repo("FrontEndApp", language="TypeScript")
        self.assertEqual(update_readme.classify(repo, set()), "web")

    def test_javascript_maps_to_web(self):
        repo = _repo("Widget", language="JavaScript")
        self.assertEqual(update_readme.classify(repo, set()), "web")

    def test_html_maps_to_web(self):
        repo = _repo("StaticSite", language="HTML")
        self.assertEqual(update_readme.classify(repo, set()), "web")

    def test_css_maps_to_web(self):
        repo = _repo("Styles", language="CSS")
        self.assertEqual(update_readme.classify(repo, set()), "web")

    # ── Uncategorised ───────────────────────────────────────────────────────

    def test_unknown_language_no_topics_returns_none(self):
        repo = _repo("RandomRepo", language="Haskell")
        self.assertIsNone(update_readme.classify(repo, set()))

    def test_no_language_no_topics_returns_none(self):
        repo = _repo("Mystery")
        self.assertIsNone(update_readme.classify(repo, set()))

    # ── Topics always beat heuristics ───────────────────────────────────────

    def test_learning_topic_beats_web_language(self):
        # TypeScript would normally classify as "web" via heuristic, but an
        # explicit "learning" topic must win.
        repo = _repo("TSNotes", language="TypeScript")
        self.assertEqual(update_readme.classify(repo, {"learning"}), "learning")

    def test_unity_topic_beats_cpp_heuristic(self):
        repo = _repo("Game", language="C++")
        self.assertEqual(update_readme.classify(repo, {"unity"}), "unity")


# ---------------------------------------------------------------------------
# get_already_linked()
# ---------------------------------------------------------------------------

class TestGetAlreadyLinked(unittest.TestCase):
    """Verify that the URL-scanning regex returns the correct repo names."""

    _START = "<!-- UNITY-GAMES-START -->"
    _END = "<!-- UNITY-GAMES-END -->"

    def _make_content(self, rows: str) -> str:
        return f"{self._START}\n{rows}\n{self._END}"

    def test_single_repo_detected(self):
        content = self._make_content(
            "| [MiniTankMania](https://github.com/Superkart/MiniTankMania) | desc | Unity · C# |"
        )
        result = update_readme.get_already_linked(content, self._START, self._END)
        self.assertIn("MiniTankMania", result)

    def test_multiple_repos_all_detected(self):
        content = self._make_content(
            "| [RepoA](https://github.com/Superkart/RepoA) | d | T |\n"
            "| [RepoB](https://github.com/Superkart/RepoB) | d | T |"
        )
        result = update_readme.get_already_linked(content, self._START, self._END)
        self.assertEqual(result, {"RepoA", "RepoB"})

    def test_empty_section_returns_empty_set(self):
        content = self._make_content("| Project | Description | Tech |\n|---|---|---|")
        result = update_readme.get_already_linked(content, self._START, self._END)
        self.assertEqual(result, set())

    def test_missing_markers_returns_empty_set_with_warning(self):
        content = "no markers here"
        import io
        with patch("sys.stderr", new_callable=io.StringIO) as mock_err:
            result = update_readme.get_already_linked(
                content, self._START, self._END
            )
        self.assertEqual(result, set())
        self.assertIn("WARNING", mock_err.getvalue())

    def test_does_not_capture_repos_outside_section(self):
        content = (
            "https://github.com/Superkart/OutsideRepo\n"
            f"{self._START}\n"
            "| [InsideRepo](https://github.com/Superkart/InsideRepo) | d | T |\n"
            f"{self._END}"
        )
        result = update_readme.get_already_linked(content, self._START, self._END)
        self.assertEqual(result, {"InsideRepo"})
        self.assertNotIn("OutsideRepo", result)


# ---------------------------------------------------------------------------
# build_new_row()
# ---------------------------------------------------------------------------

class TestBuildNewRow(unittest.TestCase):
    """Verify the Markdown table-row strings produced for each category."""

    def test_unity_row_includes_unity_prefix_and_language(self):
        repo = _repo("NewGame", language="C#", description="A cool game")
        row = update_readme.build_new_row(repo, "unity")
        self.assertIn("https://github.com/Superkart/NewGame", row)
        self.assertIn("A cool game", row)
        self.assertIn("Unity · C#", row)

    def test_unity_row_without_language_shows_unity_only(self):
        repo = _repo("ShaderDemo", language=None, description="Shader experiments")
        row = update_readme.build_new_row(repo, "unity")
        self.assertIn("Unity", row)
        self.assertNotIn("Unity · ", row)

    def test_learning_row_has_two_columns(self):
        repo = _repo("CppNotes", language="C++", description="C++ practice")
        row = update_readme.build_new_row(repo, "learning")
        # learning rows: | Name | Description |  (no Tech column)
        parts = [p.strip() for p in row.split("|") if p.strip()]
        self.assertEqual(len(parts), 2)

    def test_web_row_has_three_columns(self):
        repo = _repo("MyApp", language="TypeScript", description="A web app")
        row = update_readme.build_new_row(repo, "web")
        parts = [p.strip() for p in row.split("|") if p.strip()]
        self.assertEqual(len(parts), 3)
        self.assertIn("TypeScript", row)

    def test_missing_description_falls_back_to_dash(self):
        repo = _repo("Silent", language="JavaScript", description=None)
        row = update_readme.build_new_row(repo, "web")
        self.assertIn("—", row)

    def test_empty_description_falls_back_to_dash(self):
        repo = _repo("Empty", language="HTML", description="")
        row = update_readme.build_new_row(repo, "web")
        self.assertIn("—", row)

    def test_missing_language_falls_back_to_dash_in_web_row(self):
        repo = _repo("NoLang", language=None, description="No language set")
        row = update_readme.build_new_row(repo, "web")
        self.assertIn("—", row)

    def test_url_contains_username_and_repo_name(self):
        repo = _repo("SpecialRepo", language="Python")
        for category in ("unity", "learning", "web"):
            with self.subTest(category=category):
                row = update_readme.build_new_row(repo, category)
                self.assertIn(f"https://github.com/{update_readme.USERNAME}/SpecialRepo", row)


# ---------------------------------------------------------------------------
# insert_rows_before_end()
# ---------------------------------------------------------------------------

class TestInsertRowsBeforeEnd(unittest.TestCase):
    """Verify the append-only insertion helper."""

    _END = "<!-- UNITY-GAMES-END -->"

    def test_rows_inserted_before_end_marker(self):
        content = f"| existing row |\n{self._END}"
        new_rows = ["| new row A |", "| new row B |"]
        result = update_readme.insert_rows_before_end(content, self._END, new_rows)
        self.assertIn("| new row A |", result)
        self.assertIn("| new row B |", result)
        # end marker must still be present
        self.assertIn(self._END, result)

    def test_existing_content_preserved(self):
        original = "| [OldGame](url) | desc | Unity · C# |\n"
        content = f"{original}{self._END}"
        result = update_readme.insert_rows_before_end(
            content, self._END, ["| [NewGame](url2) | d2 | Unity · C# |"]
        )
        self.assertIn("OldGame", result)
        self.assertIn("NewGame", result)

    def test_new_rows_appear_after_existing_rows(self):
        content = f"| old |\n{self._END}"
        result = update_readme.insert_rows_before_end(
            content, self._END, ["| new |"]
        )
        old_pos = result.index("| old |")
        new_pos = result.index("| new |")
        end_pos = result.index(self._END)
        self.assertLess(old_pos, new_pos)
        self.assertLess(new_pos, end_pos)

    def test_empty_new_rows_list_inserts_only_newline(self):
        content = f"| old |\n{self._END}"
        result = update_readme.insert_rows_before_end(content, self._END, [])
        # Content should still have old row and end marker
        self.assertIn("| old |", result)
        self.assertIn(self._END, result)

    def test_end_marker_not_duplicated(self):
        content = f"stuff\n{self._END}"
        result = update_readme.insert_rows_before_end(
            content, self._END, ["| row |"]
        )
        self.assertEqual(result.count(self._END), 1)


# ---------------------------------------------------------------------------
# Integration: main() with mocked I/O and network
# ---------------------------------------------------------------------------

class TestMainIntegration(unittest.TestCase):
    """Smoke-test the main() entry point with all external calls mocked."""

    _MINIMAL_README = (
        "# Profile\n"
        "<!-- UNITY-GAMES-START -->\n"
        "| Project | Description | Tech |\n"
        "|---|---|---|\n"
        "<!-- UNITY-GAMES-END -->\n"
        "<!-- LEARNING-REPOS-START -->\n"
        "| Repo | Focus |\n"
        "|---|---|\n"
        "<!-- LEARNING-REPOS-END -->\n"
        "<!-- WEB-PROJECTS-START -->\n"
        "| Repo | Description | Tech |\n"
        "|---|---|---|\n"
        "<!-- WEB-PROJECTS-END -->\n"
    )

    def test_new_unity_repo_appended(self):
        fake_repos = [
            _repo("BrandNewGame", language="C#", description="A new Unity game"),
        ]
        with (
            patch.object(update_readme, "get_all_repos", return_value=fake_repos),
            patch.object(update_readme, "get_topics", return_value=set()),
            patch("builtins.open", mock_open(read_data=self._MINIMAL_README)) as open_mock,
        ):
            update_readme.main()

        written = "".join(
            call.args[0]
            for call in open_mock().write.call_args_list
        )
        self.assertIn("BrandNewGame", written)
        self.assertIn("A new Unity game", written)

    def test_already_linked_repo_not_duplicated(self):
        existing_readme = self._MINIMAL_README.replace(
            "<!-- UNITY-GAMES-END -->",
            "| [OldGame](https://github.com/Superkart/OldGame) | old | Unity · C# |\n"
            "<!-- UNITY-GAMES-END -->",
        )
        fake_repos = [_repo("OldGame", language="C#", description="Already there")]
        with (
            patch.object(update_readme, "get_all_repos", return_value=fake_repos),
            patch.object(update_readme, "get_topics", return_value=set()),
            patch("builtins.open", mock_open(read_data=existing_readme)) as open_mock,
        ):
            update_readme.main()

        written = "".join(
            call.args[0]
            for call in open_mock().write.call_args_list
        )
        # Each markdown row contains the name twice (display text + URL).
        # The repo is already linked so nothing new should be inserted; the
        # written content must have the same count as the original.
        self.assertEqual(
            written.count("OldGame"),
            existing_readme.count("OldGame"),
        )

    def test_featured_repo_excluded(self):
        featured_name = next(iter(update_readme.FEATURED_REPOS - {update_readme.USERNAME}))
        fake_repos = [_repo(featured_name, language="C#", description="Featured")]
        with (
            patch.object(update_readme, "get_all_repos", return_value=fake_repos),
            patch.object(update_readme, "get_topics", return_value=set()),
            patch("builtins.open", mock_open(read_data=self._MINIMAL_README)) as open_mock,
        ):
            update_readme.main()

        written = "".join(
            call.args[0]
            for call in open_mock().write.call_args_list
        )
        # The featured repo must NOT appear in the auto-managed tables
        self.assertNotIn(f"github.com/Superkart/{featured_name}", written)

    def test_forked_repo_excluded(self):
        fake_repos = [_repo("ForkOfSomething", language="C#", fork=True)]
        with (
            patch.object(update_readme, "get_all_repos", return_value=fake_repos),
            patch.object(update_readme, "get_topics", return_value=set()),
            patch("builtins.open", mock_open(read_data=self._MINIMAL_README)) as open_mock,
        ):
            update_readme.main()

        written = "".join(
            call.args[0]
            for call in open_mock().write.call_args_list
        )
        self.assertNotIn("ForkOfSomething", written)

    def test_archived_repo_excluded(self):
        fake_repos = [_repo("OldProject", language="TypeScript", archived=True)]
        with (
            patch.object(update_readme, "get_all_repos", return_value=fake_repos),
            patch.object(update_readme, "get_topics", return_value=set()),
            patch("builtins.open", mock_open(read_data=self._MINIMAL_README)) as open_mock,
        ):
            update_readme.main()

        written = "".join(
            call.args[0]
            for call in open_mock().write.call_args_list
        )
        self.assertNotIn("OldProject", written)

    def test_uncategorised_repo_excluded(self):
        fake_repos = [_repo("HaskellMisc", language="Haskell", description="Misc")]
        with (
            patch.object(update_readme, "get_all_repos", return_value=fake_repos),
            patch.object(update_readme, "get_topics", return_value=set()),
            patch("builtins.open", mock_open(read_data=self._MINIMAL_README)) as open_mock,
        ):
            update_readme.main()

        written = "".join(
            call.args[0]
            for call in open_mock().write.call_args_list
        )
        self.assertNotIn("HaskellMisc", written)


if __name__ == "__main__":
    unittest.main()
