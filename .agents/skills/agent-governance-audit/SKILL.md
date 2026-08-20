---
name: agent-governance-audit
description: 當調整 Agent 治理規範、Journal 知識庫、rules 或發現 skill ID、路徑、語言與多代理治理規則漂移時觸發此技能。
---

# Agent 治理與規範稽核 (Agent Governance Audit)

## 觸發條件
1. 修改 `.agents/AGENTS.md`、`.agents/rules/` 或 `.agents/Journal.md`。
2. 新增、修改或重新命名 `.agents/skills/` 下的技能。
3. 跨 Agent 協作交接前後或定期稽核 Agent 文件與規範一致性。

---

## 稽核流程 (Audit Workflow)

1. **工作區狀態檢查**：
   - 執行 `git status --short --branch`，確認無未提交的 dirty worktree 衝突。
2. **Canonical Skill ID 一致性檢驗**：
   - 列出所有 `.agents/skills/*/SKILL.md`。
   - 確認「資料夾名稱」、「YAML frontmatter 的 `name`」與「`.agents/skills/README.md` 表格」三者 100% 精確一致。
3. **路徑與死連結檢驗**：
   - 搜尋所有 markdown 檔案，確認引用的 references、scripts 與內部連結真實存在。
   - 檢查是否存在硬編碼的過時本機絕對路徑或大小寫不一致問題。
4. **語言與符號邊界檢驗**：
   - Agent 文件與工作日誌以繁體中文為主，技術名詞與命令保留英文。
   - 嚴禁在 UI 或輸出中夾帶裝飾性 Emoji 圖示。
5. **知識庫升格審查**：
   - 檢查 `Journal.md` 中被標記為 `adopted` 的經驗。
   - 若特定問題或解法出現 2 次以上，審查是否已升格寫入 `AGENTS.md` 或 `rules/`。
6. **自動化工具驗證**：
   - 執行治理稽核腳本（如 `python scripts/run_governance_audit.py`）。
   - 執行 `git diff --check`，確認無格式或合併殘留。

---

## 治理邊界準則

- `AGENTS.md`：不可違背的全域共通原則與憲法級規範。
- `rules/`：穩定的專案架構邊界、驗證關卡與語言工具鏈標準。
- `skills/`：可執行的任務工作流程、操作指南與觸發條件。
- `Journal.md`：經本地重現驗證的活知識庫。
- 交接流程必須使用 `cross-agent-collaboration` 規範之標準 Handoff 狀態機與格式。
