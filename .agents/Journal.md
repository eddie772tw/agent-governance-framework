# Agent 開發經驗日誌 (Journal)

## 日誌定位與同步規則

本檔是專案的「已採納、已驗證活知識庫 (Living Knowledge Base)」，旨在累積跨 Agent（Google Antigravity, OpenAI Codex, Google Jules）與人類協作過程中的避坑指南、架構決策與實踐經驗。

### 記錄格式規範
每筆新紀錄應包含以下結構化欄位：

- **日期與領域**：例如 `YYYY-MM-DD / Architecture`、`YYYY-MM-DD / Agent Workflow`。
- **來源**：`local` 或外部委派/協作記錄。
- **狀態**：
  - `proposed`：已觀察到並提出，尚待廣泛驗證。
  - `adopted`：已在本地重現驗證並正式納入專案慣例。
  - `superseded`：已被更新的架構或規則取代（標註取代者）。
- **Learning**：觀察到的核心問題、失敗經驗或可重複利用的架構思考。
- **Action**：已落實的程式碼修改或要求後續開發採取的具體防護。
- **Evidence**：單元測試結果、覆蓋率數據、驗證命令輸出或可重現步驟。

### 規則昇華機制 (Escalation Rule)
- 技能索引 `.agents/skills/README.md` 是技能名稱的唯一真理來源，日誌中不得任意創造別名。
- 若同類型的陷阱、避坑措施或最佳實踐在日誌中累積出現 **2 次以上**，代表已屬全域通用邊界，應主動提煉並升格寫入 `.agents/AGENTS.md` 或 `.agents/rules/`。

---

## 範例記錄 (Seed Examples)

### 2026-08-18 / PR 角色分化、禁止自我斷言可合併與跨 Agent 身分標記

- **來源**：`local`，針對多 Agent 協作 PR 流程進行職責分化與防護規範化。
- **狀態**：`adopted`。
- **Learning**：
  1. **PR 角色職責分化**：審查者（Reviewer）專注於客觀評估變更、檢查 CI、發表 Suggestions 與提供重現測試；作者/維護者（Author/Maintainer）專注於本地全套驗證、Living PR Body 動態同步、標題穩定性與客觀回覆。
  2. **禁止自我斷言可合併原則 (No Self-Asserted Mergeability)**：Author/Maintainer 嚴禁在 PR Body 或回覆中自我宣告「Ready to merge」、「LGTM」或可直接合併，必須客觀陳述驗證數據，由審查者做出合併結論。
  3. **跨 Agent 身分標記規範 (`{代號} as {Agent}`)**：所有 Agent 在共用 GitHub 帳號時，必須在 PR Body、Review 與回覆留言頭尾明確標記 `{代號} as {Agent}`（例如 `Gemini as Antigravity`、`Luna as Codex`），確保發言主體可追溯。
  4. **雙軌檢視與 Inline Comments 防漏盤點**：GitHub CLI `gh pr view` 容易忽略行內原生評論；Author 需搭配工具產出條列式 Markdown 檢核表逐條處置行內建議。
- **Action**：
  1. 建立 `pr-author-maintainer` 與 `pr-review-evaluation` 技能。
  2. 實作 `manage_pr_author.py` 與 `submit_pr_review.py` 輔助工具。
  3. 將身分標記與禁止自我斷言規則升格納入 `AGENTS.md`。
- **Evidence**：自動化腳本單元測試 100% 通過；PR 審查流程標準化。

---

### 2026-08-15 / 高頻非同步主迴圈零阻塞 I/O 防護

- **來源**：`local`，針對高頻事件迴圈、數據接收與串流通訊之效能防護。
- **狀態**：`adopted`。
- **Learning**：
  1. **零阻塞非同步通訊**：在 60Hz+ 或高頻事件循環中，同步的檔案讀寫、DNS 解析或 HTTP 請求會導致事件循環卡頓並累積延遲。
  2. **預先解析與快取**：所有主機名稱解析、設定檔載入與重開銷操作必須在初始化或設定變更時預先處理，不得置於主回調函式中。
- **Action**：
  1. 確保所有高頻處理器僅執行記憶體內資料轉譯與非同步分發。
  2. 將「高頻效能保護」納入 `AGENTS.md` 核心規範。
- **Evidence**：高頻負載測試無掉封包、CPU 佔用率維持低水位。

---

### 2026-08-20 / CI 建置修復、PEP 639 授權與 Setuptools Flat-Layout 套件發現防護

- **來源**：`local`，針對線上 GitHub Actions CI 建置失敗與 Setuptools 套件發現機制進行修復與防護。
- **狀態**：`adopted`。
- **Learning**：
  1. **Setuptools Flat-Layout 多目錄衝突**：在無 `src/` layout 的扁平架構下，若專案根目錄同時存在多個資料夾（例如 `agent_cli` 與 `templates`），Setuptools 為防範非預期套件打包會直接終止 build 並報錯 `Multiple top-level packages discovered in a flat-layout`。必須在 `pyproject.toml` 明確配置 `[tool.setuptools.packages.find]` 指定 include/exclude 範圍。
  2. **PEP 639 授權標記演進**：Setuptools 77.0+ 棄用 `project.license = { text = "MIT" }` table 寫法，改為直接使用 SPDX 字串表達式 `license = "MIT"`，消除 CI 建置過程中的棄用告警。
  3. **建置產物工作區隔離**：執行 `pip install -e .` 或 wheel 建置產生的 `*.egg-info/` 與 `*.whl` 必須納入 `.gitignore` 排除，防止污染 Git 工作區。
- **Action**：
  1. 於 `pyproject.toml` 加入 `[tool.setuptools.packages.find] include = ["agent_cli*"]`。
  2. 將 `project.license` 改為標準 SPDX 字串 `"MIT"`。
  3. 於 `.gitignore` 排除 `*.egg-info/`、`*.egg` 與 `*.whl`。
- **Evidence**：本地 `pip install -e .` 與 wheel 打包全數成功；25 項單元測試、Ruff 靜態檢查與治理稽核 100% 通過。
