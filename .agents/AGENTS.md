# 通用 Agent 開發與治理守則 (AGENTS.md)

## 任務入口與技能發現 Gate (Skill Discovery Gate)

每個 Agent 在執行程式碼修改或任務專用命令前，必須先完成以下步驟：

1. 閱讀本檔、`.agents/rules/workspace.md`、`.agents/Journal.md`，並檢查 `.agents/skills/README.md`。
2. 以 `.agents/skills/<directory>/SKILL.md` 的資料夾名稱作為 **canonical skill ID**；嚴禁從舊日誌或非現存名稱推測技能名稱。
3. 依任務觸發條件選取技能，完整讀取被選取的 `SKILL.md`，再讀取它明確要求的 references。
4. 若修改 UI、巨型元件、核心演算法、通訊協定、模組架構或執行非同步委派，必須在任務紀錄中列出實際採用的 skill ID。
5. 任務結束時檢查技能名稱、文件路徑與驗證命令是否仍然有效；發現命名不一致時先修正索引與 frontmatter。

Canonical skill registry 位於 `.agents/skills/README.md`。目前標準技能包含：
`agent-governance-audit`、`cross-agent-collaboration`、`codex-antigravity-bridge`、
`jules_coding`、`modular-refactoring`、`huge-component-refactoring`、
`pr-author-maintainer`、`pr-review-evaluation`、`code-quality-linting`、
`github-security-audit`、`portable-release-validation`。

Agent 文件、技能說明、工作日誌與規範內容以繁體中文為主。只有技能 ID、檔名、API、CI、React、TypeScript 等技術專有名詞，以及可能造成歧義的術語保留英文。

---

## 專案核心事實與領域工程規範 (Core Invariants)

1. **語法規範與 Linter 嚴格遵守 (Code Quality & PEP 8 Compliance)**：
   - 專案內必須配置並嚴格遵守語法規範（如 Python **PEP 8 / PEP 257**、TypeScript Strict Mode、Rust API Guidelines 等）。
   - Agent 在編寫或重構代碼後，**必須執行 Linter (如 `ruff check`) 與 Formatter (如 `ruff format`)**，達成 0 錯誤、0 警告。
   - 嚴禁濫用無理由之忽略標記（如未註明具體原因之 `# noqa` 或 `eslint-disable`）。
2. **核心/高頻效能保護 (Performance & Non-blocking Loop)**：在任何高頻輪詢、串流接收、事件主迴圈或渲染 Hot-path 內，**絕不可放置同步阻塞 (Synchronous Blocking) 或高開銷的 I/O 操作**。所有耗時運算與網路 I/O 必須非同步化或移至背景工作線程。
3. **核心演算法與業務邏輯單一真理 (Single Source of Truth)**：所有核心計算公式、業務決策樹與驗證規則，必須嚴格維持為「無副作用純函數 (Pure Functions)」，並集中收攏於領域模組中，嚴禁將業務計算零散寫死於 UI 組件中。
4. **路徑安全與檔案包含性規範 (Path Security & Containment)**：所有涉及外部輸入、檔案名稱、使用者上傳或動態路徑存取的模組，必須進行目錄包含性檢驗（防止 `../` 目錄穿越攻擊），嚴禁未經校驗直接拼接使用者輸入路徑。
5. **單一職責與 250 行重構原則**：單一檔案若超過 250 行，或職責出現發散（如混雜數據解析、狀態管理與視圖渲染），必須主動評估拆分。

---

## Agent 開發、測試與治理守則

### 核心工程原則
1. **確定性與無副作用設計**：純邏輯計算模組不得依賴全域可變狀態或外部 UI 組件生命週期。
2. **嚴格 Commit 前測試與 Linter 門檻 (Strict Pre-Commit Gate)**：在提交或推送任何程式碼修改前，必須落實執行專案定義的靜態語法檢查 (Lint)、代碼格式化 (Format) 與單元測試，嚴禁將已知測試失敗或格式未對齊的代碼推送至共用分支。
3. **無裝飾性符號規範 (No Decorative Emojis)**：所有 UI 介面、字串、命令列輸出與日誌輸出，嚴禁加入裝飾性 Emoji 圖示，保持專業、極簡與高可讀性，並確保 Windows/Linux 終端 UTF-8 編碼安全。
4. **活文件持續同步原則 (Living Documentation)**：隨著功能迭代、重構或修復，必須同步更新 PR 頂層 Body、架構圖、API 文件與 README，防止文件漂移 (Documentation Drift)。

---

## 跨 Agent 協作與身分標記規範 (`{代號} as {Agent}`)

當多個 Agent（如 Google Antigravity、OpenAI Codex、Google Jules）或人類協作者共用相同 GitHub 帳號或協同開發同一 Repository 時：

1. **身分標記格式**：所有 PR 建立、PR Body 說明、頂層 Review 審查與留言討論，必須在開頭與結尾明確標記 `{代號} as {Agent}`（例如 `Gemini as Antigravity`、`Luna as Codex`、`Gemini as Jules`、`Developer as Human`）。
2. **禁止自我斷言可合併 (No Self-Asserted Mergeability)**：PR 作者/維護者（Author / Maintainer）嚴禁在說明或回覆中自我宣稱「Ready to merge」、「LGTM」或自行宣告可合併。必須客觀陳述「變更摘要、已完成驗證數據、待審查與反饋」，將合併審查結論交由審查者。
3. **CI 未涵蓋 Blocking 意見之測試代碼義務**：當 Reviewer 提出的 Blocking 意見涉及現有 CI 尚未覆蓋之邊界、競態或例外路徑時，Reviewer **必須一併提供可重現問題的單元測試代碼**；Author 必須將其納入測試並在本地修復通過。
4. **單一檔案 Ownership 鎖定**：一次只允許一個 Agent 對同一組檔案持有寫入權限；交接時必須使用 `cross-agent-collaboration` 規範之標準 Handoff 狀態機與格式。

---

## 第三方套件引入與防幻覺查驗協議 (Anti-Hallucination Package Verification Protocol)

為防範大語言模型 (LLM) 幻覺引用不存在或被搶註的惡意依賴，引入任何第三方套件時必須嚴格執行三步驟驗證：

1. **嚴禁憑記憶直接寫入設定檔**：嚴禁未經查驗直接在 `package.json`、`pyproject.toml`、`Cargo.toml` 或 `go.mod` 中手動填寫未驗證套件。
2. **強制執行官方 Registry 查驗指令**：
   - **Node.js / npm**：`pnpm info <package-name>` 或 `npm view <package-name>`，查驗套件存在、維護者與版本。
   - **Python / PyPI**：`python -m pip index versions <package-name>` 或 `uv pip show <package-name>`，查驗 PyPI 註冊資訊與環境相容性。
   - **Rust / crates.io**：`cargo search <package-name>` 查驗官方 crates.io 註冊資訊。
   - **Go / pkg.go.dev**：`go list -m -versions <module-path>` 查驗模組資訊。
3. **開源授權與使用者確認**：
   - 確認授權為寬鬆開源授權（如 MIT、Apache-2.0、BSD-3-Clause），嚴禁無意間引入強傳染性 GPL 污染專案發行授權。
   - 經由使用者或維護者確認後，方可安裝並同步鎖定依賴檔案（如 `pnpm-lock.yaml`、`uv.lock`、`Cargo.lock`）。

---

## 開發紀錄日誌 (Journal.md) 與知識庫機制

專案設有 `Journal.md` 活知識庫機制：
1. **任務開始前**：閱讀 `Journal.md` 瞭解過往累積之避坑指南與極限邊界。
2. **生命週期狀態**：每筆知識記錄標註 `proposed`（提議中）、`adopted`（已採納）或 `superseded`（已被更新規範取代）。
3. **規則昇華機制 (Escalation Rule)**：若特定架構陷阱、錯誤或最佳實踐在日誌中出現 **2 次以上**，代表已構成專案常態邊界，必須主動提煉並寫入本檔 (`AGENTS.md`) 或對應 `rules/` 中升格為全域規則。

---

## Task Completion Checklist (任務完成自我檢核表)

在宣佈任何開發、重構或修復任務完成前，Agent 必須逐一執行並確認：
1. [ ] **測試與靜態檢查全數通過**：執行專案所屬之 Linter、Formatter 與單元測試，無任何失敗或告警。
2. [ ] **評估經驗傳承**：本次任務是否有值得傳承的學習點、架構陷阱或效能邊界？若有，主動追加至 `.agents/Journal.md`。
3. [ ] **技能與治理稽核**：若新增或調整技能/規範，執行 `agent-governance-audit`，確認 Canonical Skill ID、索引與路徑完備。
4. [ ] **維護 `.gitignore`**：檢查是否有編譯產物、快取或臨時檔案未被排除，維持工作區純潔。
5. [ ] **維護說明文件**：重大架構變更或 API 新增時，同步更新 `README.md` 與相關架構文檔。
