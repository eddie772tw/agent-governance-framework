---
name: pr-author-maintainer
description: 當作為 PR 建立者、作者或維護者 (Author/Maintainer) 撰寫 PR、持續同步更新 PR 內文、落實 Commit 前測試驗證、維護標題穩定性，或與其他 Reviewer (如 Codex、Jules、人類) 進行身分標記 ({代號} as {Agent}) 與意見回覆互動時觸發。
---

# PR Author 與 Maintainer 開發維護規範 (PR Author & Maintainer Workflow)

## 觸發條件
當以分支開發者、PR 作者或維護者（Author / Maintainer）身分執行以下任務時觸發本技能：
1. **建立新 PR**：完成本地功能開發、通過全套驗證後撰寫並提交 PR。
2. **PR 內文持續同步**：在 PR 開發或 Review 迭代過程中，隨著每一次 commit / 重構更新 PR 頂層 Body 內文，防止內容與最新代碼脫節（Documentation Drift）。
3. **回覆 Reviewer 意見**：針對其他 Agent 或人類 Reviewer 的 Top-level Review、Inline Comments / Suggestions 進行結構化回覆與討論。
4. **維護 PR 標題與中繼資料**：依據變更範圍評估是否需要更新標題，並維護標籤與關聯 Issue。

---

## 核心規範與不變量 (Core Invariants)

### 1. 禁止自我斷言可合併 (No Self-Asserted Mergeability)
- **原則**：Author / Maintainer 在 PR 說明（Body）或回覆留言中，**絕不自我斷言或宣告「Ready to merge」、「LGTM」、「Approve」或自行下定論**。
- **作法**：必須客觀陳述「變更摘要、已完成的本地/CI 驗證數據、待 Reviewer / Maintainer 審查與回饋」，將合併與審核結論交由審查者或外部驗證流程。

### 2. 嚴格 Commit 前驗證門檻 (Strict Pre-Commit Gate)
在每一次 commit 或 push 到 PR 分支前，**必須落實執行並 100% 通過本地全套檢查**：
- 靜態語法與型別格式檢查
- 單元測試與整合測試
- 專案打包建置與相依性驗證
**嚴禁將已知測試失敗、Lint 報錯或格式未對齊的代碼推送至 PR 分支**。

### 3. PR Body 持續同步與活文件原則 (Living PR Body / Continuous Sync)
- **原則**：PR 頂層 Body 必須是**活文件 (Living Document)**。
- **作法**：隨著 Review 過程中進行的多次 commit、代碼重構、bug 修正或 scope 調整，**必須同步更新 PR 頂層 Body 內文**，確保 PR Body 永遠忠實反映該 PR 的最終完整狀態，杜絕資訊偏差。

### 4. PR 標題穩定性原則 (PR Title Stability)
- 遵循 Conventional Commits 格式（如 `feat(...)`, `fix(...)`, `refactor(...)`, `docs(...)`）。
- 避免因微小修復頻繁變更 PR 標題干擾通知與討論脈絡；唯有當 PR 核心目標、範圍或主要性質發生重大轉變時才允許修正標題。

### 5. 跨 Agent 身分標記規範 (`{代號} as {Agent}`)
- **規範**：PR Body 與所有回覆留言之**開頭與結尾**必須明確標註身分：
  - 格式範例：`Gemini as Antigravity`、`Luna as Codex`、`Gemini as Jules` 等。
  - **PR Body 結尾**：`Author / Maintainer: {代號} as {Agent}`
  - **迭代紀錄**：`- {YYYY-MM-DD} ({代號} as {Agent}): {更新摘要}`
  - **回覆留言開頭/結尾**：`### {代號} as {Agent} response` / `Author: {代號} as {Agent}`

---

## 常用工具指令

```powershell
# 1. 產生標準 PR Body 範本
python .agents/skills/pr-author-maintainer/scripts/manage_pr_author.py --generate-template --identity "Gemini as Antigravity"

# 2. 驗證 PR Body 格式與自我斷言防護
python .agents/skills/pr-author-maintainer/scripts/manage_pr_author.py --validate-body pr_body.md

# 3. 抓取並條列指定 PR 的所有原生 Inline Comments 檢核清單 (防漏盤點)
python .agents/skills/pr-author-maintainer/scripts/manage_pr_author.py --pr <PR_NUMBER> --list-comments

# 4. 同步更新 GitHub PR Body
python .agents/skills/pr-author-maintainer/scripts/manage_pr_author.py --pr <PR_NUMBER> --update-body pr_body.md

# 5. 回覆特定 Inline Comment Thread
python .agents/skills/pr-author-maintainer/scripts/manage_pr_author.py --pr <PR_NUMBER> --reply-thread <COMMENT_ID> --body "已於 commit abc1234 完成重構。" --identity "Gemini as Antigravity"
```
