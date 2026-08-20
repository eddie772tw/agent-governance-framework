#!/usr/bin/env python3
"""Agent Governance Scaffolder (一鍵建立與注入工具)

This module enables scaffolding the .agents/ governance architecture into any
target project workspace with selectable presets.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import Set

FRAMEWORK_ROOT = Path(__file__).resolve().parent.parent

PRESET_SKILLS = {
    "full": {
        "agent-governance-audit",
        "cross-agent-collaboration",
        "codex-antigravity-bridge",
        "jules_coding",
        "modular-refactoring",
        "huge-component-refactoring",
        "pr-author-maintainer",
        "pr-review-evaluation",
        "code-quality-linting",
        "github-security-audit",
        "portable-release-validation",
    },
    "minimal": {
        "agent-governance-audit",
        "cross-agent-collaboration",
        "modular-refactoring",
        "code-quality-linting",
        "pr-author-maintainer",
    },
    "python": {
        "agent-governance-audit",
        "cross-agent-collaboration",
        "modular-refactoring",
        "code-quality-linting",
        "pr-author-maintainer",
        "pr-review-evaluation",
        "github-security-audit",
    },
    "node": {
        "agent-governance-audit",
        "cross-agent-collaboration",
        "modular-refactoring",
        "huge-component-refactoring",
        "code-quality-linting",
        "pr-author-maintainer",
        "pr-review-evaluation",
    },
    "rust": {
        "agent-governance-audit",
        "cross-agent-collaboration",
        "modular-refactoring",
        "code-quality-linting",
        "pr-author-maintainer",
        "pr-review-evaluation",
        "portable-release-validation",
    },
}


def scaffold_workspace(
    target_dir: str | Path,
    project_name: str | None = None,
    preset: str = "full",
    force: bool = False,
) -> bool:
    """Scaffold .agents directory and configuration into target workspace."""
    target_path = Path(target_dir).resolve()
    target_agents = target_path / ".agents"

    if target_agents.exists() and not force:
        print(
            f"[-] 錯誤: 目標目錄已存在 .agents: {target_agents} (使用 --force 覆寫)",
            file=sys.stderr,
        )
        return False

    resolved_name = project_name or target_path.name
    print(f"[*] 正在為專案 '{resolved_name}' 初始化 Agent 治理架構 (預設集: {preset})...")

    src_agents = FRAMEWORK_ROOT / ".agents"
    if not src_agents.exists():
        print(f"[-] 框架來源 .agents 目錄不存在: {src_agents}", file=sys.stderr)
        return False

    os.makedirs(target_agents, exist_ok=True)

    # 1. 複製與客製化 AGENTS.md
    src_agents_md = src_agents / "AGENTS.md"
    if src_agents_md.exists():
        content = src_agents_md.read_text(encoding="utf-8")
        customized_agents_md = content.replace(
            "通用 Agent 開發與治理守則", f"{resolved_name} Agent 開發與治理守則"
        )
        (target_agents / "AGENTS.md").write_text(customized_agents_md, encoding="utf-8")

    # 2. 建立專案 Journal.md
    src_journal = src_agents / "Journal.md"
    if src_journal.exists():
        content = src_journal.read_text(encoding="utf-8")
        customized_journal = content.replace(
            "Agent 開發經驗日誌 (Journal)",
            f"Agent 開發經驗日誌 (Journal) - {resolved_name}",
        )
        (target_agents / "Journal.md").write_text(customized_journal, encoding="utf-8")

    # 3. 複製 rules
    src_rules = src_agents / "rules"
    target_rules = target_agents / "rules"
    if src_rules.exists():
        shutil.copytree(src_rules, target_rules, dirs_exist_ok=True)

    # 4. 複製選定的 skills
    target_skills_dir = target_agents / "skills"
    os.makedirs(target_skills_dir, exist_ok=True)

    allowed_skills: Set[str] = PRESET_SKILLS.get(preset, PRESET_SKILLS["full"])
    src_skills_dir = src_agents / "skills"

    for skill_name in allowed_skills:
        src_skill = src_skills_dir / skill_name
        if src_skill.exists() and src_skill.is_dir():
            shutil.copytree(src_skill, target_skills_dir / skill_name, dirs_exist_ok=True)

    # 5. 複製與過濾 skills/README.md
    src_skills_readme = src_skills_dir / "README.md"
    if src_skills_readme.exists():
        lines = src_skills_readme.read_text(encoding="utf-8").splitlines()
        filtered_lines = []
        in_table = False

        for line in lines:
            if line.startswith("| Canonical ID"):
                in_table = True
                filtered_lines.append(line)
            elif in_table and line.startswith("|---"):
                filtered_lines.append(line)
            elif in_table and line.startswith("|"):
                parts = [p.strip().strip("`") for p in line.split("|")]
                if len(parts) >= 2 and parts[1] in allowed_skills:
                    filtered_lines.append(line)
            elif in_table and not line.startswith("|"):
                in_table = False
                filtered_lines.append(line)
            else:
                filtered_lines.append(line)

        (target_skills_dir / "README.md").write_text("\n".join(filtered_lines), encoding="utf-8")

    print(f"[+] 成功為專案 '{resolved_name}' 初始化 Agent 治理架構！(路徑: {target_agents})")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Agent Governance 架構腳手架工具")
    parser.add_argument(
        "--target", "-t", type=str, default=".", help="目標專案目錄 (預設: 當前目錄)"
    )
    parser.add_argument(
        "--project-name",
        "-n",
        type=str,
        default=None,
        help="專案名稱 (預設自目錄名稱推斷)",
    )
    parser.add_argument(
        "--preset",
        "-p",
        choices=["full", "minimal", "python", "node", "rust"],
        default="full",
        help="技能與規則預設集 (預設: full)",
    )
    parser.add_argument("--force", "-f", action="store_true", help="強制覆寫既有 .agents 目錄")

    args = parser.parse_args()
    success = scaffold_workspace(
        target_dir=args.target,
        project_name=args.project_name,
        preset=args.preset,
        force=args.force,
    )
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
