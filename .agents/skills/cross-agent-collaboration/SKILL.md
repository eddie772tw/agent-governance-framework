---
name: cross-agent-collaboration
description: 當多個 Agent（如 Google Antigravity、OpenAI Codex、Google Jules）或人類協作者在同一 Repository 進行非同步協作、交接任務、共享分支或避免同檔案衝突時使用。規範 ownership、handoff、狀態、驗證與 Git 同步流程。
---

# 跨 Agent 非同步協作 (Cross-Agent Collaboration)

## 核心原則

1. **統一入口規範**：以 `.agents/AGENTS.md` 為共同規則，`.agents/skills/` 為任務技能，`.agents/Journal.md` 為已驗證知識庫。
2. **單一寫入持有 (Single Writer Ownership)**：一次只允許一個 Agent 對同一組檔案持有寫入權限；其他 Agent 只能讀取、提出建議或處理不重疊之檔案範圍。
3. **客觀重現原則**：不將未經本地重現驗證的外部建議直接升級為專案全域規則，先在本地重現並記錄 evidence。
4. **文字狀態交接**：所有交接都必須留下可被下一個 Agent 讀取的結構化文字狀態，不依賴易遺失的暫時性聊天上下文。

---

## 任務狀態機 (Task Lifecycle States)

- `proposed`：只有需求範圍與目標，尚未開始修改。
- `active`：目前由單一 Agent 持有 ownership 並正在修改。
- `blocked`：有明確阻塞原因，需等待外部授權、人類決策或另一個 Agent 的產出。
- `handoff`：目前 Agent 已停止寫入，已通過局部驗證，等待下一個 Agent 接手。
- `done`：實作、完整測試驗證與文件同步均已完成。

---

## 開始任務流程 (Task Initiation)

1. 閱讀 `.agents/AGENTS.md`、`.agents/rules/workspace.md`、`.agents/Journal.md` 與 `.agents/skills/README.md`。
2. 讀取符合任務觸發條件之 `SKILL.md`。
3. 檢查 `git status --short --branch`、目前分支、最近 commit 與既有 handoff 狀態。
4. 宣告本次任務 scope、ownership、預計修改檔案與排除範圍。
5. 若發現其他 Agent 正在修改相同檔案，先停止寫入並進行協調。

---

## 標準 Handoff 格式 (Handoff Template)

任務交接時必須於日誌或 PR 留言中留下以下標準格式：

```text
Task: <任務名稱>
Status: active | blocked | handoff | done
Owner: <Agent / 人類>
Branch: <branch>
Scope: <本次負責範圍>
Changed: <已修改檔案列表>
Pending: <尚未完成項目>
Blocked by: <阻塞原因或 None>
Verification: <已執行的測試命令與結果>
Next action: <接手 Agent 應執行的第一件事>
Last updated: <YYYY-MM-DD>
```

> [!IMPORTANT]
> 嚴禁使用「已處理完成」、「應該沒問題」等模糊不可驗證之描述；必須明確列出具體檔案、測試數據與可操作的下一步。

---

## 完成與交接前檢查清單

- [ ] 執行與本次 scope 對應之全套單元測試與靜態檢查。
- [ ] 執行 `git diff --check`，確認無格式或合併衝突殘留。
- [ ] 若有值得傳承之經驗，更新 `.agents/Journal.md`。
- [ ] 留下標準 Handoff 狀態文字。
