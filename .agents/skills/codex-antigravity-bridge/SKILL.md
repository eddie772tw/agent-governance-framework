---
name: codex-antigravity-bridge
description: 當 Codex 需要透過 Google Antigravity 或 `agy` CLI 進行跨 Agent handoff、headless prompt、回應輪詢、共享 worktree 驗證或建立 Codex ↔ Antigravity 交互測試時使用。涵蓋既有 dirty worktree 保護、sandbox 權限、固定 token handshake、CLI timeout、diff review 與 handoff 紀錄。
---

# Codex ↔ Antigravity 跨 Agent 橋接 (Codex ↔ Antigravity Bridge)

本技能用於建立可重現、可審計的跨 Agent 自動化通訊機制，避免依賴不可靠的非結構化聊天上下文。

---

## 1. 建立 Ownership 邊界與保護機制

1. 閱讀 `.agents/AGENTS.md`、`.agents/rules/workspace.md`、`.agents/Journal.md` 與 `cross-agent-collaboration/SKILL.md`。
2. 執行 `git status --short --branch` 與最近的 commit 記錄。
3. 把既有 dirty worktree 視為其他 Agent 正在進行中的工作，**嚴禁執行 `git reset --hard` 或覆寫未提交變更**。
4. 任何一組檔案同時間只能有一個寫入 owner。在發送跨代理請求時，發起方進入 `handoff` 狀態，待收到回覆並 review diff 後再重新取回 ownership。

---

## 2. Headless 工具權限與環境配置

當透過 headless 模式 (`agy --print`) 調用 Antigravity 執行工具（例如 `view_file` 讀取專案檔案）時，需確保已設定非互動式沙盒許可權限：

在 `%USERPROFILE%\.gemini\antigravity-cli\settings.json` 中配置：
```json
{
  "enableTerminalSandbox": true,
  "toolPermission": "proceed-in-sandbox"
}
```

可執行內建輔助腳本自動檢查並設定：
```powershell
powershell -ExecutionPolicy Bypass -File `
  .agents/skills/codex-antigravity-bridge/scripts/Set-AgyBridgeSettings.ps1
```

---

## 3. 執行自動化跨代理冒煙測試 (Smoke Test)

使用內建腳本發送固定 Token 握手協議：

```powershell
# 基礎握手測試
powershell -ExecutionPolicy Bypass -File `
  .agents/skills/codex-antigravity-bridge/scripts/Invoke-AgyCrossAgentSmoke.ps1

# 檔案讀取工具權限測試
powershell -ExecutionPolicy Bypass -File `
  .agents/skills/codex-antigravity-bridge/scripts/Invoke-AgyCrossAgentSmoke.ps1 -TestReadFile
```

---

## 4. 完成交接確認

- 檢查 Antigravity 或外部 Agent 返回之確切 Token 回應（例如 `AGY_HANDSHAKE_OK:<marker>`）。
- 檢驗任何檔案變更之 `git diff`，確認符合預期範疇。
- 更新 Handoff 狀態為 `done` 或移交下一個階段。
