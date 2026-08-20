# Agent Skills 索引 (Skill Registry)

本文件是專案內建技能的唯一索引。技能資料夾名稱即為 **canonical skill ID**。嚴禁從舊日誌、顯示名稱或過時路徑推測技能名稱。

## 技能發現 Gate (Skill Discovery Gate)

執行任何任務前，必須依序完成：

1. 檢查 `.agents/skills/*/SKILL.md` 與本索引。
2. 依照下方的觸發條件比對目前任務。
3. 完整讀取所有被選取的 `SKILL.md`，再開始修改程式碼或執行任務專用命令。
4. 只有在選取的技能明確要求時，才讀取其 references。
5. 如果技能資料夾名稱與 frontmatter 的 `name` 不一致，以資料夾名稱為 canonical ID，先修正不一致再使用該技能。

---

## Canonical 技能清單

| Canonical ID | 檔案路徑 | 觸發條件 | 必要的搭配資料 |
|---|---|---|---|
| `agent-governance-audit` | `agent-governance-audit/SKILL.md` | 調整 `.agents/`、Journal、rules 或發現 skill ID/路徑/語言漂移 | 依賴完整性、YAML frontmatter 與 references 有效性 |
| `cross-agent-collaboration` | `cross-agent-collaboration/SKILL.md` | 多 Agent（Antigravity、Codex、Jules、人類）非同步協作、Ownership 鎖定與任務交接 | `.agents/AGENTS.md`、`.agents/Journal.md` 與 Handoff 狀態 |
| `codex-antigravity-bridge` | `codex-antigravity-bridge/SKILL.md` | 跨 Agent 自動化 CLI 呼叫、固定 Token Handshake、Headless Prompt 與環境配置 | `scripts/Invoke-AgyCrossAgentSmoke.ps1`、`scripts/Set-AgyBridgeSettings.ps1` |
| `jules_coding` | `jules_coding/SKILL.md` | 雲端/非同步代理委派高風險重構、大型升級或資源密集型任務 | 使用者明確授權、API 金鑰與遠端 repository 綁定 |
| `modular-refactoring` | `modular-refactoring/SKILL.md` | 系統架構重構、新增模組、領域模型與 UI 解耦或建立型別契約 | 隔離性單元測試與純函數型別契約 |
| `huge-component-refactoring` | `huge-component-refactoring/SKILL.md` | 拆分超過 250 行之程式碼/UI 元件，或優化高頻運算/渲染 Hot-path | 狀態機抽離與對應的單元測試 |
| `pr-author-maintainer` | `pr-author-maintainer/SKILL.md` | 作為 PR 作者/維護者撰寫 PR、Living PR Body 動態同步、Pre-Commit 測試門檻與身分標記 | `references/pr_author_workflow_guide.md` 與 `scripts/manage_pr_author.py` |
| `pr-review-evaluation` | `pr-review-evaluation/SKILL.md` | 評估 PR 狀態、CI 結果並標準化發表 Review 意見（含原生 Inline Comments / Suggestions） | `references/github_inline_comments_guide.md` 與 `scripts/submit_pr_review.py` |
| `github-security-audit` | `github-security-audit/SKILL.md` | 收集、審查或修復 GitHub Code Scanning/CodeQL、Dependabot、Secret Scanning 弱點 | `references/github_security_api_guide.md` 與 `scripts/collect_security_alerts.py` |
| `portable-release-validation` | `portable-release-validation/SKILL.md` | 跨平台發行打包、獨立執行檔驗證、執行期相依隔離與煙霧測試 | 發行配置、打包腳本與環境診斷 |

---

## 命名與語言規則

- 計畫、Journal 與任務摘要中必須使用上方表格列出之精確 Canonical ID。
- Agent 文件、技能說明、工作日誌與規範內容以繁體中文為主。只有技術專有名詞、API、CLI 命令與代碼保留英文。
