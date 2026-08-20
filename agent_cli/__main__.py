#!/usr/bin/env python3
"""Universal Agent Governance Framework CLI Entry Point

Usage:
  python -m agent_cli init [--target <dir>] [--preset <preset>]
  python -m agent_cli audit [<workspace_dir>]
  python -m agent_cli pr-author ...
  python -m agent_cli pr-review ...
  python -m agent_cli security ...
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from agent_cli import auditor, scaffolder


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="agent-cli",
        description="Universal Agent Governance Framework CLI & Automation Suite",
    )
    subparsers = parser.add_subparsers(dest="command", help="可用指令")

    # 1. init
    init_parser = subparsers.add_parser("init", help="在目標專案初始化 Agent 治理結構")
    init_parser.add_argument("--target", "-t", type=str, default=".", help="目標目錄")
    init_parser.add_argument("--project-name", "-n", type=str, default=None, help="專案名稱")
    init_parser.add_argument(
        "--preset",
        "-p",
        choices=["full", "minimal", "python", "node", "rust"],
        default="full",
        help="預設集",
    )
    init_parser.add_argument("--force", "-f", action="store_true", help="強制覆寫")

    # 2. audit
    audit_parser = subparsers.add_parser("audit", help="稽核工作區中的 Agent 規範一致性")
    audit_parser.add_argument("workspace", nargs="?", default=".", help="目標工作區路徑")

    args, remaining = parser.parse_known_args()

    if args.command == "init":
        ok = scaffolder.scaffold_workspace(
            target_dir=args.target,
            project_name=args.project_name,
            preset=args.preset,
            force=args.force,
        )
        return 0 if ok else 1

    if args.command == "audit":
        ws = Path(args.workspace).resolve()
        is_passed, errors, warnings = auditor.audit_governance_workspace(ws)
        for w in warnings:
            print(f"[*] 警告: {w}")
        if not is_passed:
            print(f"[-] 治理稽核未通過 (共 {len(errors)} 個錯誤)：", file=sys.stderr)
            for err in errors:
                print(f"  - {err}", file=sys.stderr)
            return 1
        print("[+] Agent 治理架構稽核 100% 通過！")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
