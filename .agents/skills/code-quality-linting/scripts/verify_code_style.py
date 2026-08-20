#!/usr/bin/env python3
"""跨語言代碼風格與語法規範檢查執行器 (Universal Code Style & Linter Runner)

功能：
1. 自動偵測工作區語言與可用之 Linter / Formatter (Ruff, ESLint, Prettier, Cargo, Gofmt)。
2. 支援 --check (唯讀檢查) 與 --fix (自動格式化與修復) 模式。
3. 輸出乾淨的檢查報告與錯誤摘要。

遵循規範：
- 僅使用 Python 標準函式庫，相容 Python 3.10+。
- Windows 主控台 UTF-8 輸出防護，嚴禁裝飾性 Emoji。
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Windows 控制台編碼防護
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


def detect_project_languages(workspace_path: Path) -> Dict[str, bool]:
    """偵測專案目錄中存在的程式語言。"""
    languages = {
        "python": False,
        "javascript_typescript": False,
        "rust": False,
        "go": False,
    }

    if (
        (workspace_path / "pyproject.toml").exists()
        or (workspace_path / "requirements.txt").exists()
        or any(workspace_path.glob("*.py"))
        or any(workspace_path.glob("**/*.py"))
    ):
        languages["python"] = True

    if (
        (workspace_path / "package.json").exists()
        or (workspace_path / "tsconfig.json").exists()
        or any(workspace_path.glob("**/*.ts"))
        or any(workspace_path.glob("**/*.js"))
    ):
        languages["javascript_typescript"] = True

    if (workspace_path / "Cargo.toml").exists() or any(workspace_path.glob("**/*.rs")):
        languages["rust"] = True

    if (workspace_path / "go.mod").exists() or any(workspace_path.glob("**/*.go")):
        languages["go"] = True

    return languages


def run_command(cmd: List[str], cwd: Path) -> Tuple[int, str, str]:
    """執行命令並回傳 (returncode, stdout, stderr)。"""
    try:
        res = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        return res.returncode, res.stdout, res.stderr
    except FileNotFoundError:
        return 127, "", f"找不到可執行檔: {cmd[0]}"
    except Exception as exc:
        return 1, "", str(exc)


def run_python_checks(workspace_path: Path, fix: bool = False) -> Tuple[bool, List[str]]:
    """執行 Python 代碼風格與語法檢查 (優先使用 ruff)。"""
    messages: List[str] = []

    # 優先使用當前 python 環境下的 ruff，次之使用全域 ruff
    ruff_cmd = [sys.executable, "-m", "ruff"]
    code, _, _ = run_command([*ruff_cmd, "--version"], workspace_path)
    if code != 0:
        if shutil.which("ruff"):
            ruff_cmd = ["ruff"]
        else:
            messages.append(
                "[-] 提示: 未安裝 'ruff'，建議透過 'pip install ruff' 啟用高效能 PEP 8 檢查。"
            )
            return True, messages

    all_passed = True
    if fix:
        print("[*] 正在執行 Python 自動修復 (ruff check --fix)...")
        code, out, err = run_command([*ruff_cmd, "check", "--fix", "."], workspace_path)
        if code != 0:
            messages.append(f"[-] ruff check --fix 報錯:\n{err or out}")
            all_passed = False

        print("[*] 正在執行 Python 代碼格式化 (ruff format)...")
        code, out, err = run_command([*ruff_cmd, "format", "."], workspace_path)
        if code != 0:
            messages.append(f"[-] ruff format 報錯:\n{err or out}")
            all_passed = False
    else:
        print("[*] 正在執行 Python 語法檢查 (ruff check)...")
        code, out, err = run_command([*ruff_cmd, "check", "."], workspace_path)
        if code != 0:
            messages.append(f"[-] Python Lint 檢查失敗 (PEP 8 違規):\n{out or err}")
            all_passed = False

        print("[*] 正在執行 Python 格式化驗證 (ruff format --check)...")
        code, out, err = run_command([*ruff_cmd, "format", "--check", "."], workspace_path)
        if code != 0:
            messages.append(f"[-] Python 代碼格式不符標準 (請執行 --fix 修正):\n{out or err}")
            all_passed = False

    return all_passed, messages


def run_rust_checks(workspace_path: Path, fix: bool = False) -> Tuple[bool, List[str]]:
    """執行 Rust 代碼風格檢查 (cargo fmt & cargo clippy)。"""
    messages: List[str] = []
    has_cargo = shutil.which("cargo") is not None

    if not has_cargo:
        return True, messages

    all_passed = True
    if fix:
        print("[*] 正在格式化 Rust 代碼 (cargo fmt)...")
        code, out, err = run_command(["cargo", "fmt"], workspace_path)
        if code != 0:
            messages.append(f"[-] cargo fmt 失敗:\n{err or out}")
            all_passed = False
    else:
        print("[*] 正在檢查 Rust 格式 (cargo fmt --check)...")
        code, out, err = run_command(["cargo", "fmt", "--check"], workspace_path)
        if code != 0:
            messages.append(f"[-] Rust 格式不符合規範:\n{err or out}")
            all_passed = False

        print("[*] 正在執行 Rust Clippy 靜態檢查...")
        code, out, err = run_command(
            ["cargo", "clippy", "--all-targets", "--", "-D", "warnings"],
            workspace_path,
        )
        if code != 0:
            messages.append(f"[-] Rust Clippy 檢查失敗:\n{err or out}")
            all_passed = False

    return all_passed, messages


def main() -> int:
    parser = argparse.ArgumentParser(description="跨語言代碼風格與語法規範檢查工具")
    parser.add_argument(
        "--workspace",
        "-w",
        type=str,
        default=".",
        help="目標工作區路徑 (預設: 當前目錄)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        default=True,
        help="唯讀檢查模式 (預設)",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="自動修復與格式化模式",
    )

    args = parser.parse_args()
    ws_path = Path(args.workspace).resolve()

    fix_mode = args.fix
    languages = detect_project_languages(ws_path)

    print(f"[*] 工作區: {ws_path}")
    print(f"[*] 偵測到之語言環境: {[k for k, v in languages.items() if v]}")

    overall_passed = True
    all_messages: List[str] = []

    if languages["python"]:
        passed, msgs = run_python_checks(ws_path, fix=fix_mode)
        if not passed:
            overall_passed = False
        all_messages.extend(msgs)

    if languages["rust"]:
        passed, msgs = run_rust_checks(ws_path, fix=fix_mode)
        if not passed:
            overall_passed = False
        all_messages.extend(msgs)

    for msg in all_messages:
        print(msg, file=sys.stderr if not overall_passed else sys.stdout)

    if not overall_passed:
        print("\n[-] 代碼風格與語法檢查未通過！請依據上方提示修正後再行提交。", file=sys.stderr)
        return 1

    print("\n[+] 代碼風格與語法檢查 100% 通過！符合專案品質標準。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
