---
name: github-security-audit
description: 當需要收集、審查或修復 GitHub 自主檢測的安全問題（Code Scanning/CodeQL、Dependabot、Secret Scanning、Security Advisories）時觸發此技能。
---

# GitHub 安全檢測與弱點審查 (GitHub Security Audit)

## 觸發條件
當需要：
1. 收集儲存庫內由 GitHub 自動檢測產生的安全警報（Code Scanning / Dependabot / Secret Scanning / Security Advisories）。
2. 針對 CodeQL 靜態掃描發現的程式碼缺陷（如 Path Injection、Bad Tag Regex 等）進行審查、評估與排定修復。
3. 檢查第三方依賴套件漏洞（Dependabot）或密鑰洩漏（Secret Scanning）狀態。
4. 匯出專案整體安全評估報告或更新安全治理方針。

---

## 安全資料收集工作流

### 1. 使用內建自動化腳本一鍵收集

```powershell
# 執行全維度收集並印出摘要
python .agents/skills/github-security-audit/scripts/collect_security_alerts.py

# 輸出 Markdown 報告至指定檔案
python .agents/skills/github-security-audit/scripts/collect_security_alerts.py --md-out security_report.md

# 輸出完整 JSON 數據供自動化分析
python .agents/skills/github-security-audit/scripts/collect_security_alerts.py --json-out security_data.json
```

---

## PR 檢查與警報生命週期規範 (PR Security Lifecycle)

在進行安全漏洞修復與驗證時，必須理解 GitHub Advanced Security 的警報生命週期：

1. **PR 階段 (Open PR)**：
   - GitHub Security Tab 顯示的是 **Base 分支 (如 `main`)** 的警報狀態。在 PR 處於開啟或分支 Commit 階段，Security Tab 上的主要警報總數不會立即減少。
   - **驗證指標 (Source of Truth)**：必須透過 **PR Checks** (`gh pr checks <pr-number>`) 或 **CodeQL CI Action 日誌** 來確認本次變更是否成功消除警告。
2. **Merge 階段 (Merged to Default Branch)**：
   - PR 正式合併至預設分支（`main`）並觸發主分支的 CodeQL 掃描後，Security Tab 上的歷史警報才會自動轉為 **`Closed (Fixed)`**。
