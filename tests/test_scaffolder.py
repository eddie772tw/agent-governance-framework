"""單元測試：agent_cli/scaffolder.py

驗證：
1. scaffold_workspace 能成功將 .agents 架構注入目標目錄。
2. 支援 full / minimal / python 等不同 presets。
3. 注入後執行治理稽核 audit 能 100% 通過。
"""

from pathlib import Path

from agent_cli.auditor import audit_governance_workspace
from agent_cli.scaffolder import scaffold_workspace


def test_scaffold_full_preset(tmp_path: Path):
    target = tmp_path / "my_project"
    target.mkdir()

    success = scaffold_workspace(
        target_dir=target,
        project_name="MyProject",
        preset="full",
    )
    assert success is True

    agents_dir = target / ".agents"
    assert (agents_dir / "AGENTS.md").exists()
    assert (agents_dir / "Journal.md").exists()
    assert (agents_dir / "rules" / "workspace.md").exists()
    assert (agents_dir / "skills" / "README.md").exists()

    content = (agents_dir / "AGENTS.md").read_text(encoding="utf-8")
    assert "MyProject Agent 開發與治理守則" in content

    # 稽核生成的專案架構
    is_passed, errors, warnings = audit_governance_workspace(target)
    assert is_passed is True, f"Scaffolded workspace failed audit: {errors}"


def test_scaffold_minimal_preset(tmp_path: Path):
    target = tmp_path / "minimal_project"
    target.mkdir()

    success = scaffold_workspace(
        target_dir=target,
        project_name="MinimalApp",
        preset="minimal",
    )
    assert success is True

    skills_dir = target / ".agents" / "skills"
    assert (skills_dir / "agent-governance-audit").exists()
    assert (skills_dir / "cross-agent-collaboration").exists()
    assert (skills_dir / "modular-refactoring").exists()
    assert (skills_dir / "pr-author-maintainer").exists()
    assert not (skills_dir / "huge-component-refactoring").exists()

    # 稽核 minimal 專案架構
    is_passed, errors, _ = audit_governance_workspace(target)
    assert is_passed is True, f"Minimal scaffolded workspace failed audit: {errors}"
