"""單元測試：collect_security_alerts.py

驗證：
1. generate_markdown_report 正確轉換安全檢測數據為結構化報告。
2. 包含各嚴重程度統計與 Code Scanning / Dependabot 清單。
"""

import sys
from pathlib import Path

# 加入腳本目錄至 sys.path
scripts_dir = (
    Path(__file__).resolve().parent.parent
    / ".agents"
    / "skills"
    / "github-security-audit"
    / "scripts"
)
sys.path.insert(0, str(scripts_dir))

from collect_security_alerts import generate_markdown_report  # noqa: E402


def test_generate_markdown_report_empty():
    data = {
        "repository": "test-org/test-repo",
        "collected_at": "2026-08-20T10:00:00Z",
        "code_scanning_alerts": [],
        "dependabot_alerts": [],
        "secret_scanning_alerts": [],
        "security_advisories": [],
    }

    report = generate_markdown_report(data)
    assert "# GitHub 安全檢測審計報告 — `test-org/test-repo`" in report
    assert "無任何未修復之 Code Scanning 警報" in report
    assert "無任何未修復之 Dependabot 警報" in report


def test_generate_markdown_report_with_alerts():
    data = {
        "repository": "test-org/test-repo",
        "collected_at": "2026-08-20T10:00:00Z",
        "code_scanning_alerts": [
            {
                "rule": {
                    "id": "py/path-injection",
                    "severity": "error",
                    "security_severity_level": "high",
                    "description": "Unsanitized path used in file operation",
                },
                "most_recent_instance": {
                    "location": {
                        "path": "server/file_handler.py",
                        "start_line": 42,
                    }
                },
                "html_url": "https://github.com/test-org/test-repo/security/code-scanning/1",
            }
        ],
        "dependabot_alerts": [
            {
                "dependency": {"package": {"name": "requests"}},
                "security_advisory": {
                    "severity": "medium",
                    "summary": "Cookie leak in requests",
                },
                "state": "open",
            }
        ],
        "secret_scanning_alerts": [],
        "security_advisories": [],
    }

    report = generate_markdown_report(data)
    assert "HIGH: 1 件" in report
    assert "py/path-injection" in report
    assert "`server/file_handler.py:42`" in report
    assert "`requests`" in report
    assert "Cookie leak in requests" in report
