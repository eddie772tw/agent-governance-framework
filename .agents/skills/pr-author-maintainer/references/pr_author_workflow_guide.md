# PR Author 與 Maintainer 完整工作流程指南

本指南為 PR 建立者、作者或維護者（Author / Maintainer）提供詳細的工作流規範，涵蓋 PR 結構、嚴格驗證門檻、禁止自我宣告 Mergeable 規範、PR Body 活文件同步迭代、標題穩定性維護，以及跨 Agent 身分標記與審查互動實務。

---

## 1. 職責與定位邊界

在多 Agent 與人類協作的開發體系中，職責劃分如下：
- **PR Reviewer (`pr-review-evaluation`)**：由獨立審查者評估 PR 變更、CI 狀態，提出審查見解、Inline Comments / Suggestions，並評定是否符合合併標準。
- **PR Author / Maintainer (`pr-author-maintainer`)**：由 PR 提案者負責本地完整驗證、撰寫 PR、隨每次 commit 迭代更新 PR Body、維護標題穩定性，並客觀回覆 Reviewer 提出的問題。

---

## 2. 核心規範與邊界防護

### 2.1 禁止自我斷言可合併 (No Self-Asserted Mergeability)

**核心精神**：Author 不應扮演自己 PR 的法官。無論本地測試多麼完整，Author / Maintainer 均不得在 PR 說明、更新或回覆中自我斷言「Ready to merge」、「LGTM」或宣告可直接合併。

#### 合規對照表

| 違規模式 (Disallowed) | 合規模式 (Required) |
|---|---|
| ❌ "This PR is ready to merge now." | ✅ "All local and CI checks have passed. Awaiting review from Reviewers / Maintainers." |
| ❌ "LGTM, everything is tested, merging approved." | ✅ "Pre-commit tests and static checks verified locally." |
| ❌ "No issues found, this should be merged immediately." | ✅ "Changes summarized below. Please review the updated logic." |

---

### 2.2 嚴格 Commit 前驗證門檻 (Pre-Commit Gate)

在每次執行 `git commit` 或 `git push` 到 PR 分支前，必須依序執行：
1. 靜態分析與格式化檢查
2. 完整單元測試與整合測試
3. 型別檢查與打包建置

**零容忍原則**：若有任何一項檢查未過，必須在本地修正完成後方能 commit。絕不得帶著已知的紅燈推送至遠端。

---

### 2.3 PR Body 持續同步 (Living PR Body)

PR Body 是整個 PR 的唯一事實來源 (Single Source of Truth)，不能停留在最初建立時的草稿狀態。每次修改代碼或修正 Reviewer 指出之問題後，必須同步更新 PR 頂層 Body 中的變更摘要與 Living Changelog。

---

### 2.4 雙軌檢視與 Inline Comments 防漏盤點機制

GitHub CLI `gh pr view` 容易忽略行內原生評論；Author / Maintainer 必須採取雙軌審查消費流程，利用 `manage_pr_author.py --list-comments` 產出條列式 Markdown 檢核表，逐條盤點並處置行內評論，徹底消弭審查盲區。
