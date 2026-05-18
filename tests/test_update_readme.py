"""Unit tests for scripts/update_readme.py.

All tests run fully in-process — no network calls, no real AI calls.
GitHub API helpers are tested via monkeypatching; pure-logic helpers
are tested directly with hand-crafted inputs.
"""

import io
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import update_readme  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _repo(name, language=None, description=None, fork=False, archived=False):
    return {
        "name": name,
        "language": language,
        "description": description,
        "fork": fork,
        "archived": archived,
    }


def _mock_openai_module(reply: str) -> MagicMock:
    """Return a fake openai module whose OpenAI client replies with *reply*."""
    mock_mod = MagicMock()
    mock_client = MagicMock()
    mock_mod.OpenAI.return_value = mock_client
    mock_response = MagicMock()
    mock_response.choices[0].message.content = reply
    mock_client.chat.completions.create.return_value = mock_response
    return mock_mod


# ---------------------------------------------------------------------------
# _classify_by_heuristics()
# ---------------------------------------------------------------------------

class TestClassifyByHeuristics(unittest.TestCase):

    # ── Topic tier (highest priority) ───────────────────────────────────────

    def test_unity_topic_beats_language(self):
        repo = _repo("Game", language="Python")
        self.assertEqual(update_readme._classify_by_heuristics(repo, {"unity"}), "unity")

    def test_game_development_topic(self):
        self.assertEqual(
            update_readme._classify_by_heuristics(_repo("TankX"), {"game-development"}),
            "unity",
        )

    def test_learning_topic_beats_web_language(self):
        repo = _repo("TSNotes", language="TypeScript")
        self.assertEqual(update_readme._classify_by_heuristics(repo, {"learning"}), "learning")

    def test_backend_topic(self):
        self.assertEqual(
            update_readme._classify_by_heuristics(_repo("API"), {"rest-api"}),
            "backend",
        )

    def test_data_eng_topic(self):
        self.assertEqual(
            update_readme._classify_by_heuristics(_repo("ETL"), {"data-pipeline"}),
            "data_eng",
        )

    def test_ml_topic(self):
        self.assertEqual(
            update_readme._classify_by_heuristics(_repo("ModelLab", language="Python"), {"ml"}),
            "ml_ai",
        )

    def test_systems_topic(self):
        self.assertEqual(
            update_readme._classify_by_heuristics(_repo("Bot"), {"robotics"}),
            "systems",
        )

    def test_web_topic(self):
        self.assertEqual(
            update_readme._classify_by_heuristics(_repo("Site"), {"web"}),
            "web",
        )

    # ── Name-based learning heuristic (tier 2, beats language) ─────────────

    def test_journey_name_beats_cpp_language(self):
        # C++ would normally → systems, but "journey" in name → learning
        repo = _repo("Cpp_Journey", language="C++")
        self.assertEqual(update_readme._classify_by_heuristics(repo, set()), "learning")

    def test_learn_in_name(self):
        self.assertEqual(
            update_readme._classify_by_heuristics(_repo("LearnRust"), set()),
            "learning",
        )

    def test_practice_in_name(self):
        self.assertEqual(
            update_readme._classify_by_heuristics(_repo("practice-problems"), set()),
            "learning",
        )

    def test_tutorial_in_name(self):
        self.assertEqual(
            update_readme._classify_by_heuristics(_repo("flask-tutorial"), set()),
            "learning",
        )

    def test_exercise_in_name(self):
        self.assertEqual(
            update_readme._classify_by_heuristics(_repo("exercise-tracker"), set()),
            "learning",
        )

    # ── Language tier (tier 3) ───────────────────────────────────────────────

    def test_csharp_maps_to_unity(self):
        self.assertEqual(
            update_readme._classify_by_heuristics(_repo("UnityProj", language="C#"), set()),
            "unity",
        )

    def test_shaderlab_maps_to_unity(self):
        self.assertEqual(
            update_readme._classify_by_heuristics(_repo("Shader", language="ShaderLab"), set()),
            "unity",
        )

    def test_typescript_maps_to_web(self):
        self.assertEqual(
            update_readme._classify_by_heuristics(_repo("App", language="TypeScript"), set()),
            "web",
        )

    def test_javascript_maps_to_web(self):
        self.assertEqual(
            update_readme._classify_by_heuristics(_repo("Widget", language="JavaScript"), set()),
            "web",
        )

    def test_html_maps_to_web(self):
        self.assertEqual(
            update_readme._classify_by_heuristics(_repo("Static", language="HTML"), set()),
            "web",
        )

    def test_java_maps_to_backend(self):
        self.assertEqual(
            update_readme._classify_by_heuristics(_repo("SpringApp", language="Java"), set()),
            "backend",
        )

    def test_go_maps_to_backend(self):
        self.assertEqual(
            update_readme._classify_by_heuristics(_repo("GoServer", language="Go"), set()),
            "backend",
        )

    def test_rust_maps_to_backend(self):
        self.assertEqual(
            update_readme._classify_by_heuristics(_repo("RustApi", language="Rust"), set()),
            "backend",
        )

    def test_kotlin_maps_to_backend(self):
        self.assertEqual(
            update_readme._classify_by_heuristics(_repo("KtService", language="Kotlin"), set()),
            "backend",
        )

    def test_cpp_maps_to_systems(self):
        self.assertEqual(
            update_readme._classify_by_heuristics(_repo("DroneCtrl", language="C++"), set()),
            "systems",
        )

    def test_c_maps_to_systems(self):
        self.assertEqual(
            update_readme._classify_by_heuristics(_repo("Firmware", language="C"), set()),
            "systems",
        )

    def test_jupyter_maps_to_ml_ai(self):
        self.assertEqual(
            update_readme._classify_by_heuristics(
                _repo("Notebook", language="Jupyter Notebook"), set()
            ),
            "ml_ai",
        )

    # ── Python description tier (tier 4) ────────────────────────────────────

    def test_python_pipeline_desc_maps_to_data_eng(self):
        repo = _repo("ETLJob", language="Python", description="ETL pipeline for data warehouse")
        self.assertEqual(update_readme._classify_by_heuristics(repo, set()), "data_eng")

    def test_python_ml_desc_maps_to_ml_ai(self):
        repo = _repo("Clf", language="Python", description="Neural network classifier for images")
        self.assertEqual(update_readme._classify_by_heuristics(repo, set()), "ml_ai")

    def test_python_ml_beats_data_when_both_present(self):
        # description has both ml and pipeline keywords — ml_ai should win
        repo = _repo(
            "MLPipeline",
            language="Python",
            description="Machine learning pipeline for model training",
        )
        self.assertEqual(update_readme._classify_by_heuristics(repo, set()), "ml_ai")

    def test_python_no_desc_keywords_returns_none(self):
        repo = _repo("PythonMisc", language="Python", description=None)
        self.assertIsNone(update_readme._classify_by_heuristics(repo, set()))

    # ── Unclassified ─────────────────────────────────────────────────────────

    def test_unknown_language_returns_none(self):
        self.assertIsNone(
            update_readme._classify_by_heuristics(_repo("HaskellThing", language="Haskell"), set())
        )

    def test_no_language_no_topics_returns_none(self):
        self.assertIsNone(update_readme._classify_by_heuristics(_repo("Mystery"), set()))


# ---------------------------------------------------------------------------
# classify_with_ai()
# ---------------------------------------------------------------------------

class TestClassifyWithAi(unittest.TestCase):

    def test_returns_none_without_token(self):
        with patch.object(update_readme, "GITHUB_TOKEN", ""):
            result = update_readme.classify_with_ai(_repo("Repo"), set())
        self.assertIsNone(result)

    def test_returns_none_when_openai_missing(self):
        with patch.dict(sys.modules, {"openai": None}):
            with patch.object(update_readme, "GITHUB_TOKEN", "fake-token"):
                result = update_readme.classify_with_ai(_repo("Repo"), set())
        self.assertIsNone(result)

    def test_valid_category_returned(self):
        mock_mod = _mock_openai_module("backend")
        with patch.dict(sys.modules, {"openai": mock_mod}):
            with patch.object(update_readme, "GITHUB_TOKEN", "fake-token"):
                result = update_readme.classify_with_ai(
                    _repo("HaskellServer", language="Haskell", description="Web server"), set()
                )
        self.assertEqual(result, "backend")

    def test_unknown_ai_reply_falls_back_to_other(self):
        mock_mod = _mock_openai_module("nonsense_category")
        with patch.dict(sys.modules, {"openai": mock_mod}):
            with patch.object(update_readme, "GITHUB_TOKEN", "fake-token"):
                result = update_readme.classify_with_ai(_repo("X"), set())
        self.assertEqual(result, "other")

    def test_ai_reply_stripped_of_quotes(self):
        mock_mod = _mock_openai_module('"web"')
        with patch.dict(sys.modules, {"openai": mock_mod}):
            with patch.object(update_readme, "GITHUB_TOKEN", "fake-token"):
                result = update_readme.classify_with_ai(_repo("Site"), set())
        self.assertEqual(result, "web")

    def test_api_exception_returns_none(self):
        mock_mod = MagicMock()
        mock_mod.OpenAI.return_value.chat.completions.create.side_effect = RuntimeError("timeout")
        with patch.dict(sys.modules, {"openai": mock_mod}):
            with patch.object(update_readme, "GITHUB_TOKEN", "fake-token"):
                result = update_readme.classify_with_ai(_repo("Repo"), set())
        self.assertIsNone(result)


# ---------------------------------------------------------------------------
# classify() — top-level with AI fallback
# ---------------------------------------------------------------------------

class TestClassify(unittest.TestCase):

    def test_heuristic_match_skips_ai(self):
        repo = _repo("GameX", language="C#")
        # AI should never be called when heuristics match
        with patch.object(update_readme, "classify_with_ai") as mock_ai:
            result = update_readme.classify(repo, set())
        mock_ai.assert_not_called()
        self.assertEqual(result, "unity")

    def test_no_heuristic_match_calls_ai(self):
        repo = _repo("Misc", language="Haskell")
        with patch.object(update_readme, "classify_with_ai", return_value="other") as mock_ai:
            result = update_readme.classify(repo, set())
        mock_ai.assert_called_once()
        self.assertEqual(result, "other")

    def test_ai_returning_none_falls_back_to_other(self):
        repo = _repo("Strange", language="Erlang")
        with patch.object(update_readme, "classify_with_ai", return_value=None):
            result = update_readme.classify(repo, set())
        self.assertEqual(result, "other")

    def test_never_returns_none(self):
        repo = _repo("NoMatch")
        with patch.object(update_readme, "classify_with_ai", return_value=None):
            result = update_readme.classify(repo, set())
        self.assertIsNotNone(result)
        self.assertIn(result, update_readme.CATEGORIES)


# ---------------------------------------------------------------------------
# get_already_linked()
# ---------------------------------------------------------------------------

class TestGetAlreadyLinked(unittest.TestCase):
    _START = "<!-- UNITY-GAMES-START -->"
    _END = "<!-- UNITY-GAMES-END -->"

    def _wrap(self, rows: str) -> str:
        return f"{self._START}\n{rows}\n{self._END}"

    def test_single_repo_detected(self):
        content = self._wrap(
            "| [MiniTankMania](https://github.com/Superkart/MiniTankMania) | d | T |"
        )
        result = update_readme.get_already_linked(content, self._START, self._END)
        self.assertIn("MiniTankMania", result)

    def test_multiple_repos_all_detected(self):
        content = self._wrap(
            "| [RepoA](https://github.com/Superkart/RepoA) | d | T |\n"
            "| [RepoB](https://github.com/Superkart/RepoB) | d | T |"
        )
        self.assertEqual(
            update_readme.get_already_linked(content, self._START, self._END),
            {"RepoA", "RepoB"},
        )

    def test_empty_section_returns_empty_set(self):
        content = self._wrap("| Project | Description | Tech |\n|---|---|---|")
        self.assertEqual(
            update_readme.get_already_linked(content, self._START, self._END),
            set(),
        )

    def test_missing_markers_returns_empty_with_warning(self):
        with patch("sys.stderr", new_callable=io.StringIO) as mock_err:
            result = update_readme.get_already_linked("no markers", self._START, self._END)
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

    def test_unity_row_has_unity_prefix(self):
        row = update_readme.build_new_row(_repo("NewGame", language="C#", description="Cool"), "unity")
        self.assertIn("Unity · C#", row)
        self.assertIn("Cool", row)
        self.assertIn("https://github.com/Superkart/NewGame", row)

    def test_unity_row_no_language(self):
        row = update_readme.build_new_row(_repo("ShaderDemo", language=None), "unity")
        self.assertIn("Unity", row)
        self.assertNotIn("Unity · ", row)

    def test_learning_row_two_columns(self):
        row = update_readme.build_new_row(_repo("CppNotes", language="C++", description="C++ notes"), "learning")
        parts = [p.strip() for p in row.split("|") if p.strip()]
        self.assertEqual(len(parts), 2)

    def test_web_row_three_columns(self):
        row = update_readme.build_new_row(_repo("MyApp", language="TypeScript", description="Web app"), "web")
        parts = [p.strip() for p in row.split("|") if p.strip()]
        self.assertEqual(len(parts), 3)
        self.assertIn("TypeScript", row)

    def test_backend_row_three_columns(self):
        row = update_readme.build_new_row(_repo("ApiSvc", language="Java", description="REST API"), "backend")
        parts = [p.strip() for p in row.split("|") if p.strip()]
        self.assertEqual(len(parts), 3)
        self.assertIn("Java", row)

    def test_data_eng_row_three_columns(self):
        row = update_readme.build_new_row(_repo("ETL", language="Python", description="Pipeline"), "data_eng")
        parts = [p.strip() for p in row.split("|") if p.strip()]
        self.assertEqual(len(parts), 3)

    def test_systems_row_three_columns(self):
        row = update_readme.build_new_row(_repo("Drone", language="C++", description="Autopilot"), "systems")
        parts = [p.strip() for p in row.split("|") if p.strip()]
        self.assertEqual(len(parts), 3)
        self.assertIn("C++", row)

    def test_other_row_three_columns(self):
        row = update_readme.build_new_row(_repo("Misc", language="Haskell", description="Misc"), "other")
        parts = [p.strip() for p in row.split("|") if p.strip()]
        self.assertEqual(len(parts), 3)

    def test_missing_description_falls_back_to_dash(self):
        row = update_readme.build_new_row(_repo("Silent", language="JavaScript"), "web")
        self.assertIn("—", row)

    def test_missing_language_falls_back_to_dash(self):
        row = update_readme.build_new_row(_repo("NoLang", description="no lang"), "web")
        self.assertIn("—", row)

    def test_url_always_includes_username_and_name(self):
        for cat in update_readme.CATEGORIES:
            with self.subTest(category=cat):
                row = update_readme.build_new_row(_repo("SpecialRepo", language="Python"), cat)
                self.assertIn(
                    f"https://github.com/{update_readme.USERNAME}/SpecialRepo", row
                )


# ---------------------------------------------------------------------------
# insert_rows_before_end()
# ---------------------------------------------------------------------------

class TestInsertRowsBeforeEnd(unittest.TestCase):
    _END = "<!-- UNITY-GAMES-END -->"

    def test_rows_inserted_before_marker(self):
        content = f"| old |\n{self._END}"
        result = update_readme.insert_rows_before_end(content, self._END, ["| new A |", "| new B |"])
        self.assertIn("| new A |", result)
        self.assertIn(self._END, result)

    def test_existing_content_preserved(self):
        content = f"| old |\n{self._END}"
        result = update_readme.insert_rows_before_end(content, self._END, ["| new |"])
        self.assertIn("| old |", result)
        self.assertIn("| new |", result)

    def test_new_rows_appear_after_existing(self):
        content = f"| old |\n{self._END}"
        result = update_readme.insert_rows_before_end(content, self._END, ["| new |"])
        self.assertLess(result.index("| old |"), result.index("| new |"))
        self.assertLess(result.index("| new |"), result.index(self._END))

    def test_end_marker_not_duplicated(self):
        content = f"stuff\n{self._END}"
        result = update_readme.insert_rows_before_end(content, self._END, ["| row |"])
        self.assertEqual(result.count(self._END), 1)


# ---------------------------------------------------------------------------
# Integration: main() with all external calls mocked
# ---------------------------------------------------------------------------

class TestMainIntegration(unittest.TestCase):

    _MINIMAL_README = (
        "# Profile\n"
        "<!-- UNITY-GAMES-START -->\n"
        "| Project | Description | Tech |\n|---|---|---|\n"
        "<!-- UNITY-GAMES-END -->\n"
        "<!-- WEB-PROJECTS-START -->\n"
        "| Repo | Description | Tech |\n|---|---|---|\n"
        "<!-- WEB-PROJECTS-END -->\n"
        "<!-- BACKEND-START -->\n"
        "| Repo | Description | Tech |\n|---|---|---|\n"
        "<!-- BACKEND-END -->\n"
        "<!-- DATA-ENG-START -->\n"
        "| Repo | Description | Tech |\n|---|---|---|\n"
        "<!-- DATA-ENG-END -->\n"
        "<!-- ML-AI-PROJECTS-START -->\n"
        "| Repo | Description | Tech |\n|---|---|---|\n"
        "<!-- ML-AI-PROJECTS-END -->\n"
        "<!-- SYSTEMS-START -->\n"
        "| Repo | Description | Tech |\n|---|---|---|\n"
        "<!-- SYSTEMS-END -->\n"
        "<!-- LEARNING-REPOS-START -->\n"
        "| Repo | Focus |\n|---|---|\n"
        "<!-- LEARNING-REPOS-END -->\n"
        "<!-- OTHER-PROJECTS-START -->\n"
        "| Repo | Description | Tech |\n|---|---|---|\n"
        "<!-- OTHER-PROJECTS-END -->\n"
    )

    def _run_main(self, repos, readme=None, topics=None):
        readme = readme or self._MINIMAL_README
        topics_fn = topics or (lambda _: set())
        written_chunks = []

        def capture_write(data):
            written_chunks.append(data)

        m = mock_open(read_data=readme)
        m.return_value.write.side_effect = capture_write

        with (
            patch.object(update_readme, "get_all_repos", return_value=repos),
            patch.object(update_readme, "get_topics", side_effect=topics_fn),
            patch.object(update_readme, "classify_with_ai", return_value=None),
            patch("builtins.open", m),
        ):
            update_readme.main()

        return "".join(written_chunks)

    def test_new_unity_repo_appended(self):
        written = self._run_main([_repo("BrandNewGame", language="C#", description="New game")])
        self.assertIn("BrandNewGame", written)
        self.assertIn("Unity · C#", written)

    def test_new_backend_repo_appended(self):
        written = self._run_main([_repo("SpringSvc", language="Java", description="REST service")])
        self.assertIn("SpringSvc", written)
        self.assertIn("Java", written)

    def test_new_systems_repo_appended(self):
        written = self._run_main([_repo("DroneApi", language="C++", description="Drone control")])
        self.assertIn("DroneApi", written)

    def test_already_linked_anywhere_not_added_again(self):
        # Repo already in the unity section — must not appear in any other section
        readme_with_existing = self._MINIMAL_README.replace(
            "<!-- UNITY-GAMES-END -->",
            "| [OldGame](https://github.com/Superkart/OldGame) | old | Unity · C# |\n"
            "<!-- UNITY-GAMES-END -->",
        )
        written = self._run_main(
            [_repo("OldGame", language="C#", description="Already there")],
            readme=readme_with_existing,
        )
        # Count must match the original (nothing new added)
        self.assertEqual(written.count("OldGame"), readme_with_existing.count("OldGame"))

    def test_featured_repo_excluded(self):
        featured = next(iter(update_readme.FEATURED_REPOS - {update_readme.USERNAME}))
        written = self._run_main([_repo(featured, language="C#", description="Featured")])
        self.assertNotIn(f"github.com/Superkart/{featured}", written)

    def test_forked_repo_excluded(self):
        written = self._run_main([_repo("ForkOfX", language="C#", fork=True)])
        self.assertNotIn("ForkOfX", written)

    def test_archived_repo_excluded(self):
        written = self._run_main([_repo("OldProject", language="TypeScript", archived=True)])
        self.assertNotIn("OldProject", written)

    def test_uncategorised_repo_goes_to_other(self):
        written = self._run_main([_repo("HaskellMisc", language="Haskell", description="Misc")])
        # Goes to Other Projects section
        other_start = written.find("<!-- OTHER-PROJECTS-START -->")
        other_end = written.find("<!-- OTHER-PROJECTS-END -->")
        self.assertGreater(other_start, -1)
        section = written[other_start:other_end]
        self.assertIn("HaskellMisc", section)

    def test_new_ml_ai_repo_appended(self):
        written = self._run_main([
            _repo("VisionLab", language="Python", description="Computer vision model training"),
        ])
        self.assertIn("VisionLab", written)

    def test_data_eng_repo_goes_to_correct_section(self):
        written = self._run_main([
            _repo("ETLJob", language="Python", description="ETL pipeline for data warehouse"),
        ])
        data_start = written.find("<!-- DATA-ENG-START -->")
        data_end = written.find("<!-- DATA-ENG-END -->")
        section = written[data_start:data_end]
        self.assertIn("ETLJob", section)

    def test_topic_override_beats_language(self):
        # Java repo with robotics topic → systems, not backend
        def topics_fn(name):
            return {"robotics"} if name == "JavaRobot" else set()

        written = self._run_main(
            [_repo("JavaRobot", language="Java", description="Robot arm")],
            topics=topics_fn,
        )
        systems_start = written.find("<!-- SYSTEMS-START -->")
        systems_end = written.find("<!-- SYSTEMS-END -->")
        self.assertIn("JavaRobot", written[systems_start:systems_end])


if __name__ == "__main__":
    unittest.main()
