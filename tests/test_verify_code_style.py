"""單元測試：verify_code_style.py

驗證：
1. detect_project_languages 能正確辨識 Python, Rust, Node 等專案類型。
2. run_python_checks 執行邏輯正確。
"""

import sys
from pathlib import Path

# 加入腳本目錄至 sys.path
scripts_dir = (
    Path(__file__).resolve().parent.parent
    / ".agents"
    / "skills"
    / "code-quality-linting"
    / "scripts"
)
sys.path.insert(0, str(scripts_dir))

from verify_code_style import (  # noqa: E402
    detect_project_languages,
    run_python_checks,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_detect_project_languages():
    languages = detect_project_languages(REPO_ROOT)
    assert languages["python"] is True


def test_detect_project_languages_empty_dir(tmp_path: Path):
    languages = detect_project_languages(tmp_path)
    assert languages["python"] is False
    assert languages["rust"] is False
    assert languages["javascript_typescript"] is False
    assert languages["go"] is False


def test_run_python_checks_on_valid_workspace():
    passed, msgs = run_python_checks(REPO_ROOT, fix=False)
    assert passed is True
