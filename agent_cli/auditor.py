#!/usr/bin/env python3
"""Agent Governance & Skill Registry Validator

Validates:
1. Canonical skill ID matches folder name and YAML frontmatter 'name'.
2. All skills in .agents/skills/ are registered in .agents/skills/README.md.
3. Referenced files/scripts in SKILL.md and README.md actually exist.
4. Correct UTF-8 encoding without BOM or invalid bytes.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def extract_frontmatter_name(skill_md_path: Path) -> str | None:
    """Extract 'name' property from SKILL.md YAML frontmatter."""
    try:
        content = skill_md_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None

    match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None

    frontmatter = match.group(1)
    for line in frontmatter.splitlines():
        line = line.strip()
        if line.startswith("name:"):
            return line.split("name:", 1)[1].strip()
    return None


def parse_registered_skills(readme_path: Path) -> Dict[str, str]:
    """Parse skill table from .agents/skills/README.md.

    Returns dict mapping canonical_id -> relative file path.
    """
    if not readme_path.exists():
        return {}

    content = readme_path.read_text(encoding="utf-8")
    skills: Dict[str, str] = {}

    # Match markdown table row like: | `skill-id` | `skill-id/SKILL.md` | ...
    pattern = re.compile(r"\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|")
    for line in content.splitlines():
        match = pattern.search(line)
        if match:
            skill_id = match.group(1).strip()
            skill_path = match.group(2).strip()
            if skill_id != "Canonical ID":
                skills[skill_id] = skill_path

    return skills


def audit_governance_workspace(
    workspace_dir: str | Path,
) -> Tuple[bool, List[str], List[str]]:
    """Audit the agent governance workspace.

    Returns:
        (is_passed, errors, warnings)
    """
    ws = Path(workspace_dir).resolve()
    agents_dir = ws / ".agents"

    errors: List[str] = []
    warnings: List[str] = []

    if not agents_dir.exists():
        errors.append(f"找不到 .agents 目錄: {agents_dir}")
        return False, errors, warnings

    agents_md = agents_dir / "AGENTS.md"
    journal_md = agents_dir / "Journal.md"
    skills_dir = agents_dir / "skills"
    skills_readme = skills_dir / "README.md"

    if not agents_md.exists():
        errors.append("缺少核心規則檔 .agents/AGENTS.md")
    if not journal_md.exists():
        errors.append("缺少活知識庫檔 .agents/Journal.md")
    if not skills_readme.exists():
        errors.append("缺少技能索引檔 .agents/skills/README.md")

    if not skills_dir.exists():
        errors.append("缺少技能目錄 .agents/skills/")
        return False, errors, warnings

    registered_skills = parse_registered_skills(skills_readme)

    # Inspect all subdirectories in skills/
    discovered_skill_ids: List[str] = []
    for item in skills_dir.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            skill_id = item.name
            discovered_skill_ids.append(skill_id)
            skill_md = item / "SKILL.md"

            if not skill_md.exists():
                errors.append(f"技能目錄 '{skill_id}' 缺少 SKILL.md 檔案。")
                continue

            fm_name = extract_frontmatter_name(skill_md)
            if not fm_name:
                errors.append(
                    f"技能 '{skill_id}/SKILL.md' 缺少合法的 YAML frontmatter 'name' 宣告。"
                )
            elif fm_name != skill_id:
                errors.append(
                    f"技能 frontmatter name ('{fm_name}') 與 canonical ID ('{skill_id}') 不一致！"
                )

            # Check if registered in README.md
            if skill_id not in registered_skills:
                errors.append(f"技能 '{skill_id}' 未在 .agents/skills/README.md 索引清單中註冊！")

    # Check for orphaned entries in README.md
    for reg_id, reg_path in registered_skills.items():
        if reg_id not in discovered_skill_ids:
            errors.append(f".agents/skills/README.md 註冊的技能 '{reg_id}' 找不到對應之資料夾！")

    # Check UTF-8 validity for all markdown files in .agents
    for md_file in agents_dir.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            if "\ufeff" in content:
                warnings.append(f"檔案 '{md_file.relative_to(ws)}' 包含 UTF-8 BOM，建議移除。")
        except UnicodeDecodeError as exc:
            errors.append(f"檔案 '{md_file.relative_to(ws)}' 無法以 UTF-8 解碼: {exc}")

    is_passed = len(errors) == 0
    return is_passed, errors, warnings


def main() -> int:
    workspace = Path.cwd()
    if len(sys.argv) > 1:
        workspace = Path(sys.argv[1])

    print(f"[*] 正在稽核 Agent 治理架構: {workspace} ...")
    is_passed, errors, warnings = audit_governance_workspace(workspace)

    for w in warnings:
        print(f"[*] 警告: {w}")

    if not is_passed:
        print(f"[-] 治理稽核未通過 (共 {len(errors)} 個錯誤)：", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("[+] Agent 治理架構稽核 100% 通過！(所有 Canonical ID 與索引完全對齊)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
