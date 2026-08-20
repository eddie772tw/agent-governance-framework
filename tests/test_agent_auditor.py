"""單元測試：agent_cli/auditor.py

驗證：
1. audit_governance_workspace 對於標準工作區回傳 True 且無 errors。
2. 當缺少必要檔案、frontmatter 不匹配或缺少註冊時正確攔截。
"""

from pathlib import Path

from agent_cli.auditor import (
    audit_governance_workspace,
    extract_frontmatter_name,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_audit_current_framework_passes():
    is_passed, errors, warnings = audit_governance_workspace(REPO_ROOT)
    assert is_passed is True, f"治理稽核未通過: {errors}"
    assert len(errors) == 0


def test_extract_frontmatter_name(tmp_path: Path):
    skill_md = tmp_path / "SKILL.md"
    skill_md.write_text(
        "---\nname: my-cool-skill\ndescription: Test skill\n---\n# Title\n",
        encoding="utf-8",
    )
    assert extract_frontmatter_name(skill_md) == "my-cool-skill"

    invalid_md = tmp_path / "INVALID.md"
    invalid_md.write_text("# No frontmatter", encoding="utf-8")
    assert extract_frontmatter_name(invalid_md) is None


def test_audit_detects_missing_agents_dir(tmp_path: Path):
    is_passed, errors, _ = audit_governance_workspace(tmp_path)
    assert is_passed is False
    assert any("找不到 .agents 目錄" in err for err in errors)


def test_audit_detects_skill_id_mismatch(tmp_path: Path):
    agents_dir = tmp_path / ".agents"
    agents_dir.mkdir()
    (agents_dir / "AGENTS.md").write_text("# Agents", encoding="utf-8")
    (agents_dir / "Journal.md").write_text("# Journal", encoding="utf-8")

    skills_dir = agents_dir / "skills"
    skills_dir.mkdir()
    (skills_dir / "README.md").write_text(
        "| Canonical ID | 檔案路徑 |\n|---|---|\n| `foo-skill` | `foo-skill/SKILL.md` |\n",
        encoding="utf-8",
    )

    skill_folder = skills_dir / "foo-skill"
    skill_folder.mkdir()
    (skill_folder / "SKILL.md").write_text(
        "---\nname: wrong-skill-name\ndescription: test\n---\n# Foo",
        encoding="utf-8",
    )

    is_passed, errors, _ = audit_governance_workspace(tmp_path)
    assert is_passed is False
    assert any("不一致" in err for err in errors)
