# 快速上手指南 (Quickstart Guide)

只需 3 分鐘，即可為任何全新或既有專案導入完整的 Agent 治理體系！

---

## 步驟 1：使用腳手架初始化目標專案

在 `agent-governance-framework` 目錄下執行：

```bash
# 完整導入
python scripts/init_agent_workspace.py --target ../my-awesome-app --project-name "MyAwesomeApp" --preset full
```

系統將在目標專案目錄自動產生：
- `.agents/AGENTS.md`（已自訂專案名稱）
- `.agents/Journal.md`（空白活知識庫）
- `.agents/rules/`（工作區規範與工具鏈標準）
- `.agents/skills/`（選定的核心技能與自動化腳本）

---

## 步驟 2：設定專案驗證指令

開啟目標專案的 `.agents/rules/workspace.md`，將【任務完成驗證關卡】段落修改為您專案的測試指令，例如：

```markdown
## 任務完成驗證關卡 (Verification Gate)
- 靜態檢查：`pnpm lint`
- 單元測試：`pnpm test`
- 建置檢查：`pnpm build`
```

---

## 步驟 3：執行治理稽核

在目標專案中執行稽核，確認所有 Skill ID 與索引對齊：

```bash
# 若已安裝 agent-cli 套件
agent-cli audit

# 或直接執行腳本
python scripts/run_governance_audit.py
```

---

## 步驟 4：開始與 Agent 協同開發

您現在可以告訴任何 AI Assistant（Antigravity、Codex、Claude、Jules 等）：
> "請先閱讀 `.agents/AGENTS.md` 與 `.agents/skills/README.md`，依照規範開始開發本專案。"
