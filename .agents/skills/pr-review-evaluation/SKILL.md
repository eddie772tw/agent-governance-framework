---
name: pr-review-evaluation
description: 當需要評估一個 PR、或完成一個分支的開發並提交 PR 後，針對該 PR 的狀態進行 Merge 評估或標準化發表 Review 意見 (包含頂層 Review 及原生 GitHub Inline Comments) 時觸發。
---

# PR Review 評估與意見標準化 (PR Review Evaluation & Inline Comments)

## 觸發條件
當完成分支開發提交 Pull Request (PR)，或收到評估特定 PR 的請求時，觸發此技能來檢查 PR 狀態、執行本地驗證，並以標準化格式（含頂層 Review 與原生 GitHub Inline Review Comments）發表審查意見。

---

## 評估與審查流程

### 1. 抓取狀態與 Diff
- **PR 狀態與 Checks**：使用 `gh pr view <number>` 及 `gh pr checks <number>` 抓取當前 PR 狀態與 CI 測試結果。
- **取得變更 Diff 與 HEAD SHA**：
  ```bash
  gh pr view <number> --json headRefOid -q .headRefOid
  gh pr diff <number>
  ```
- **審查 CI 錯誤**：若有 CI/CD 失敗，深入分析 Actions 日誌並於本地重現定位問題。

---

## 2. Review 結構與標準格式

### 2.1 跨 Agent 身分標記規範 (`{代號} as {Agent}`)
Review 報告的開頭標題與結尾簽名必須統一使用 `{代號} as {Agent}` 格式（例如 `Gemini as Antigravity`、`Luna as Codex` 等）。

### 2.2 頂層 Review 格式 (Top-level Review Body)
```markdown
{代號} as {Agent} review — {結論摘要, e.g., blocking findings recorded / ready to merge}.

**CI Status & Local Verification:**
簡述目前的 Actions 狀態及本地驗證的結果 (例如 checks pass, 单項單元測試通過數據等)。

**Findings & Assessment:**
- 條列式指出需要修正的具體問題 (型別錯誤、邏輯缺失、缺乏邊界驗證等)。
- 提出修改建議與處理方案。
- **CI 未涵蓋 Blocking 意見之測試代碼義務 (Mandatory Test Snippet)**：若 Reviewer 提出的 Blocking 意見涉及現有 CI 測試尚未涵蓋的情境（如極端邊界值、競態或未測試路徑），**Reviewer 必須一併提供可重現該問題的具體測試代碼**，供 Author 於本地快速重現、修復並納入測試套裝中。

**Next Steps:**
- 說明通過條件 (例如：請修正上述錯誤、納入附帶之單元測試並確保 CI 全數轉綠)。

Reviewer: {代號} as {Agent}
```

---

## 3. 原生 GitHub Inline Review Comments 工具

使用內建腳本自動驗證 Diff Hunk 邊界並提交原子 Review：

```powershell
# 1. 驗證 Review JSON 格式與行號是否超界 (Dry-Run)
python .agents/skills/pr-review-evaluation/scripts/submit_pr_review.py --pr <PR_NUMBER> --review-file review.json --dry-run

# 2. 實際提交 Review
python .agents/skills/pr-review-evaluation/scripts/submit_pr_review.py --pr <PR_NUMBER> --review-file review.json
```
