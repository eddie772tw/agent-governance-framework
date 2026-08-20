#!/usr/bin/env python3
"""GitHub PR Review & Inline Comments 提交與驗證工具

功能：
1. 支援批次提交頂層 Review 及多個原生的 GitHub Inline Review Comments。
2. 自動校驗 PR 的最新 HEAD Commit SHA。
3. 自動解析 PR Diff Hunk，檢驗行內評論 (Inline Comments) 之行號是否落在有效 Diff 範圍內。
4. 具備超界行號自動降級 (Graceful Fallback) 機制，防止 GitHub API 422 錯誤。
5. 支援 Dry-Run 模式與純 JSON 驗證。

遵循規範：
- 僅使用 Python 標準函式庫，相容 Python 3.10+。
- Windows 主控台 UTF-8 輸出防護，嚴禁裝飾性 Emoji。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from typing import Any, Dict, List, Set, Tuple

# Windows 控制台編碼防護
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


IDENTITY_PATTERN = re.compile(r"\b[\w\.\-]+\s+as\s+[\w\.\-]+\b", re.IGNORECASE)


def check_review_identity_tag(body_text: str) -> bool:
    """檢查 Review Body 是否包含 '{代號} as {Agent}' 身分標記。"""
    return bool(IDENTITY_PATTERN.search(body_text))


def parse_unified_diff(diff_text: str) -> Dict[str, Dict[str, Set[int]]]:
    """解析 git unified diff 文本，提取每個檔案在 LEFT (舊) 與 RIGHT (新) 的有效行號集合。"""
    result: Dict[str, Dict[str, Set[int]]] = {}
    current_file: str | None = None
    hunk_regex = re.compile(r"^@@\s+-(\d+)(?:,(\d+))?\s+\+(\d+)(?:,(\d+))?\s+@@")

    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:].strip()
            if current_file not in result:
                result[current_file] = {"LEFT": set(), "RIGHT": set()}
        elif line.startswith("@@ ") and current_file:
            match = hunk_regex.match(line)
            if match:
                old_start = int(match.group(1))
                old_len = int(match.group(2)) if match.group(2) is not None else 1
                new_start = int(match.group(3))
                new_len = int(match.group(4)) if match.group(4) is not None else 1

                for line_idx in range(old_start, old_start + old_len):
                    result[current_file]["LEFT"].add(line_idx)
                for line_idx in range(new_start, new_start + new_len):
                    result[current_file]["RIGHT"].add(line_idx)

    return result


def fetch_pr_diff(pr_number: int, repo: str | None = None) -> str:
    """透過 gh CLI 抓取 PR 的 diff 文本。"""
    cmd = ["gh", "pr", "diff", str(pr_number)]
    if repo:
        cmd.extend(["-R", repo])
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        raise RuntimeError(f"無法取得 PR #{pr_number} 的 diff: {res.stderr.strip()}")
    return res.stdout


def fetch_head_sha(pr_number: int, repo: str | None = None) -> str:
    """透過 gh CLI 抓取 PR 的最新 HEAD Commit SHA。"""
    cmd = [
        "gh",
        "pr",
        "view",
        str(pr_number),
        "--json",
        "headRefOid",
        "-q",
        ".headRefOid",
    ]
    if repo:
        cmd.extend(["-R", repo])
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        raise RuntimeError(f"無法取得 PR #{pr_number} 的 HEAD SHA: {res.stderr.strip()}")
    return res.stdout.strip()


def validate_and_filter_comments(
    comments: List[Dict[str, Any]],
    diff_map: Dict[str, Dict[str, Set[int]]],
    fallback_to_body: bool = True,
) -> Tuple[List[Dict[str, Any]], List[str], List[str]]:
    """驗證行內評論行號是否落在有效 diff 區間內。

    Returns:
        (valid_comments, fallback_markdown_blocks, warnings)
    """
    valid_comments: List[Dict[str, Any]] = []
    fallback_blocks: List[str] = []
    warnings: List[str] = []

    for idx, c in enumerate(comments):
        path = c.get("path")
        line = c.get("line")
        side = c.get("side", "RIGHT").upper()
        body = c.get("body", "")

        if not path or line is None:
            warnings.append(f"Comment #{idx} 缺少 path 或 line 欄位，已跳過。")
            continue

        normalized_path = path.replace("\\", "/")
        file_diff = diff_map.get(normalized_path)

        if not file_diff:
            msg = f"檔案 '{normalized_path}' 不在 PR 變更範圍內。"
            if fallback_to_body:
                warnings.append(f"{msg} 已自動轉移至頂層 Review Body。")
                fallback_blocks.append(
                    f"### [Fallback Comment] `{normalized_path}` (Line {line})\n{body}"
                )
            else:
                warnings.append(f"錯誤: {msg}")
            continue

        valid_lines = file_diff.get(side, set())
        if line not in valid_lines:
            msg = f"行號 {line} (side: {side}) 不在 '{normalized_path}' 的有效 Diff Hunk 內。"
            if fallback_to_body:
                warnings.append(f"{msg} 已自動轉移至頂層 Review Body。")
                fallback_blocks.append(
                    f"### [Fallback Comment] `{normalized_path}` (Line {line})\n{body}"
                )
            else:
                warnings.append(f"錯誤: {msg}")
            continue

        valid_comments.append(c)

    return valid_comments, fallback_blocks, warnings


def validate_and_sanitize_payload(
    payload: Dict[str, Any], diff_text: str, auto_fallback: bool = True
) -> Tuple[Dict[str, Any], List[str]]:
    """驗證並淨化 Review Payload。

    Args:
        payload: Review JSON 物件 (包含 body, comments 等)
        diff_text: Git Unified Diff 文本
        auto_fallback: 是否自動將超界行號降級至 Review Body

    Returns:
        (sanitized_payload, warnings)
    """
    diff_map = parse_unified_diff(diff_text)
    comments = payload.get("comments", [])
    body_text = payload.get("body", "")

    if not auto_fallback:
        for c in comments:
            path = c.get("path", "").replace("\\", "/")
            line = c.get("line")
            side = c.get("side", "RIGHT").upper()
            if path not in diff_map or line not in diff_map[path].get(side, set()):
                raise ValueError(
                    f"行號 {line} (side: {side}) 不在檔案 '{path}' 的 Diff Hunk 範圍內。"
                )

    valid_comments, fallback_blocks, warnings = validate_and_filter_comments(
        comments=comments, diff_map=diff_map, fallback_to_body=auto_fallback
    )

    final_body = body_text
    if fallback_blocks:
        fallback_section = "\n\n### Out-of-Diff / General Comments (Fallback):\n" + "\n\n".join(
            fallback_blocks
        )
        final_body = (final_body + fallback_section).strip()

    sanitized = dict(payload)
    sanitized["body"] = final_body
    sanitized["comments"] = valid_comments
    return sanitized, warnings


def submit_review_api(
    pr_number: int,
    payload: Dict[str, Any],
    repo: str | None = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """透過 gh api 提交 PR Review。"""
    if dry_run:
        print("[*] [Dry-Run] 模擬提交 Review Payload：")
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return {"status": "dry_run", "payload": payload}

    endpoint = f"repos/{{owner}}/{{repo}}/pulls/{pr_number}/reviews"
    if repo:
        endpoint = f"repos/{repo}/pulls/{pr_number}/reviews"

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as tf:
        json.dump(payload, tf, ensure_ascii=False)
        temp_path = tf.name

    try:
        cmd = [
            "gh",
            "api",
            "--method",
            "POST",
            endpoint,
            "--input",
            temp_path,
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if res.returncode != 0:
            raise RuntimeError(f"提交 Review 失敗 (HTTP 錯誤): {res.stderr.strip()}")

        return json.loads(res.stdout)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="GitHub PR Review & Inline Comments 提交與驗證工具"
    )
    parser.add_argument("--pr", type=int, required=True, help="目標 Pull Request 編號")
    parser.add_argument(
        "--review-file",
        type=str,
        required=True,
        help="包含 Review Body 與 Inline Comments 的 JSON 檔案路徑",
    )
    parser.add_argument(
        "--repo",
        "-R",
        type=str,
        help="目標 GitHub Repository (格式: OWNER/REPO，預設依據目前 git repo)",
    )
    parser.add_argument(
        "--event",
        type=str,
        choices=["COMMENT", "APPROVE", "REQUEST_CHANGES"],
        default="COMMENT",
        help="Review 動作 (預設: COMMENT)",
    )
    parser.add_argument(
        "--strict-identity",
        action="store_true",
        help="強制要求 Review Body 必須包含 '{代號} as {Agent}' 身分標記",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="僅進行本地 Diff Hunk 驗證與 Payload 預覽，不實際發送 API",
    )

    args = parser.parse_args()

    if not os.path.exists(args.review_file):
        print(f"[-] 錯誤: 找不到檔案 '{args.review_file}'", file=sys.stderr)
        return 1

    with open(args.review_file, "r", encoding="utf-8") as f:
        try:
            review_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"[-] 錯誤: Review JSON 解析失敗: {e}", file=sys.stderr)
            return 1

    body_text = review_data.get("body", "").strip()
    comments = review_data.get("comments", [])

    if not body_text and not comments:
        print("[-] 錯誤: Review 必須至少包含 body 或 comments 之一。", file=sys.stderr)
        return 1

    if args.strict_identity and not check_review_identity_tag(body_text):
        print(
            "[-] 錯誤: Review Body 未包含有效的 '{代號} as {Agent}' 身分標記\n"
            "    (例如: 'Gemini as Antigravity review — ...')",
            file=sys.stderr,
        )
        return 1

    print(f"[*] 正在抓取 PR #{args.pr} 的 HEAD SHA 與 Diff 資訊...")
    try:
        head_sha = fetch_head_sha(args.pr, args.repo)
        diff_text = fetch_pr_diff(args.pr, args.repo)
    except Exception as e:
        print(f"[-] 取得 PR 資訊失敗: {e}", file=sys.stderr)
        return 1

    diff_map = parse_unified_diff(diff_text)
    print(f"[+] 成功解析 {len(diff_map)} 個變更檔案的 Diff Hunk。")

    valid_comments, fallback_blocks, warnings = validate_and_filter_comments(
        comments=comments, diff_map=diff_map, fallback_to_body=True
    )

    for w in warnings:
        print(f"[*] 警告: {w}")

    final_body = body_text
    if fallback_blocks:
        final_body += "\n\n---\n## ⚠️ 超界評論自動轉移 (Fallback Comments)\n" + "\n\n".join(
            fallback_blocks
        )

    payload: Dict[str, Any] = {
        "commit_id": head_sha,
        "body": final_body,
        "event": review_data.get("event", args.event),
    }

    if valid_comments:
        payload["comments"] = valid_comments

    print(f"[*] 準備提交 Review (包含 {len(valid_comments)} 則有效行內評論)...")
    try:
        res = submit_review_api(
            pr_number=args.pr,
            payload=payload,
            repo=args.repo,
            dry_run=args.dry_run,
        )
        if not args.dry_run:
            review_url = res.get("html_url", "")
            print("[+] 成功提交 PR Review！")
            if review_url:
                print(f"    網址: {review_url}")
        return 0
    except Exception as e:
        print(f"[-] 提交 Review 失敗: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
