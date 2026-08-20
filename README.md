# Universal Agent Governance Framework (通用 Agent 治理架構)

<p align="center">
  <strong>專為多 Agent (Google Antigravity, OpenAI Codex, Google Jules) 與人類工程師協同開發打造的開源 AI 軟體工程治理體系</strong>
</p>

<p align="center">
  <a href="https://github.com/eddie772tw/agent-governance-framework/actions"><img src="https://github.com/eddie772tw/agent-governance-framework/actions/workflows/agent-governance-ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT%20OR%20Apache--2.0-blue.svg" alt="License: MIT OR Apache-2.0"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python&logoColor=white" alt="Python 3.10+"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="README.en.md"><img src="https://img.shields.io/badge/Language-English-blue" alt="English Documentation"></a>
</p>

---

## 為什麼需要 Agent 治理架構？ (Why Agent Governance?)

在大語言模型 (LLM) 深度介入日常編程的時代，AI Agent 往往具備強大的代碼產出能力，卻也帶來常見的**工程混亂與安全隱患**：
- **代碼風格漂移**：不同 Agent 產出風格不一的代碼，破壞 PEP 8 或專案靜態檢查標準。
- **幻覺套件引入**：Agent 憑記憶隨意引用不存在或已被黑客搶註 (Typosquatting) 的惡意依賴。
- **多 Agent 狀態衝突**：多個 Agent（如 Antigravity 與 Codex）在同一儲存庫同時修改檔案，互相覆寫工作樹。
- **PR 審查失序與虛假核准**：Agent 自我宣稱「Ready to merge / LGTM」，或遺漏 GitHub 行內程式碼評論 (Inline Comments)。
- **經驗遺失**：每次踩坑的架構邊界隨對話視窗關閉而煙消雲散，無法沉澱為專案的長效知識。

**Universal Agent Governance Framework** 提供一套完整、中性化且具自我稽核能力的**憲法級治理標準與自動化工具鏈**，讓 AI Agent 具備資深工程師等級的自律性與協作紀律。

---

## 四大核心治理支柱 (The Four Pillars of Governance)

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                  Universal Agent Governance Framework                       │
├──────────────────────┬──────────────────────┬───────────────────────────────┤
│ 1. 語法與結構標準化   │ 2. 企業級安全與合規  │ 3. 多代理與跨代理協作          │
│ • PEP 8 / 0 容忍 Lint│ • 防幻覺套件驗證協議 │ • Single Writer Ownership     │
│ • 純函數單一真理原則 │ • CodeQL / Dependabot│ • {代號} as {Agent} 身分標記   │
│ • 250 行模組拆分原則 │ • 路徑安全包含性檢驗 │ • Headless CLI Token 握手協議 │
├──────────────────────┴──────────────────────┴───────────────────────────────┤
│ 4. 結構化審查與動態 PR 活文件工作流 (Automated Review & Living PR Workflow)     │
│ • Living PR Body 動態同步    • 禁止自我宣告可合併 (No Self-Asserted Merge)      │
│ • 原生 GitHub Inline Comments  • CI 未涵蓋 Blocking 意見強制附帶測試代碼       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1. 語法與代碼結構標準化 (Syntax & Structural Standardization)
- **PEP 8 與嚴格 Linter 合規 (`code-quality-linting`)**：強制執行語言原生規範（Python PEP 8/PEP 257、TypeScript Strict、Rust Clippy 等），實踐 **0 錯誤、0 警告**，嚴禁無理由之 `# noqa` / `eslint-disable` 遮蔽。
- **確定性代碼風格**：內建 `verify_code_style.py`，支援自動偵測多語言並執行 Formatter/Linter。
- **純函數單一真理 (Single Source of Truth)**：核心業務與計算邏輯強制收攏為無副作用純函數 (Pure Functions)，嚴禁雜揉於 UI 或網路層。
- **250 行巨型代碼拆分 (`huge-component-refactoring`)**：提供模組化解耦、狀態機抽離與高頻熱路徑（Hot-Path 零物件配置）標準 SOP。

### 2. 企業級安全與供應鏈完整性 (Security & Supply Chain Defense)
- **三步驟防幻覺套件查驗協議 (Anti-Hallucination Protocol)**：
  1. 嚴禁憑 LLM 記憶直接寫入相依檔案。
  2. 強制執行 npm / PyPI / crates.io / Go 官方 Registry CLI 查驗。
  3. 審查開源授權相容性（MIT / Apache-2.0），經人類確認後方可安裝。
- **GitHub Advanced Security 自動化審查 (`github-security-audit`)**：內建 `collect_security_alerts.py`，一鍵自動抓取並整合 CodeQL 漏洞、Dependabot 套件告警、Secret Scanning 密鑰洩漏與安全性通報。
- **路徑安全與防注入 (`safe_resolve_path`)**：嚴格目錄包含性檢驗，杜絕目錄穿越 (`../`) 攻擊。

### 3. 多代理與跨代理非同步協作 (Multi-Agent & Cross-Agent Collaboration)
- **單一寫入權持有 (Single Writer Ownership)**：透過 `cross-agent-collaboration` 的標準狀態機 (`active`, `blocked`, `handoff`, `done`) 與結構化 Handoff 文本，杜絕同檔案衝突。
- **跨 Agent 身分標記 (`{代號} as {Agent}`)**：所有 Agent 在共用 GitHub 帳號時，強制於 PR、Review 與留言中標記身分（如 `Gemini as Antigravity`、`Luna as Codex`、`Gemini as Jules`）。
- **跨代理 CLI 橋接與沙盒 (`codex-antigravity-bridge`)**：提供非互動沙盒配置與固定 Token 冒煙測試握手腳本。
- **雲端 Agent 委派邊界 (`jules_coding`)**：規範非同步雲端 Agent 的委派條件、權限前置檢查與本地完整 Diff 驗收。

### 4. 結構化審查與動態 PR 活文件工作流 (Automated Review & Living PR Workflow)
- **PR 職責分化與嚴格邊界**：
  - **PR Author / Maintainer (`pr-author-maintainer`)**：
    - **禁止自我斷言可合併 (No Self-Asserted Mergeability)**：嚴禁自我宣告「Ready to merge / LGTM」，將合併結論交由獨立審查者。
    - **Living PR Body 動態同步**：隨著每次 commit 即時迭代 PR 頂層 Body，杜絕文件漂移。
    - **雙軌檢視與 Inline Comments 防漏盤點**：條列式 Markdown 檢核表逐條處置行內評論。
  - **PR Reviewer (`pr-review-evaluation`)**：
    - 原生 GitHub Inline Review Comments & Suggestions 批次提交 (`submit_pr_review.py`)。
    - **CI 未涵蓋 Blocking 意見附帶測試義務**：Reviewer 指出邊界或例外問題時，**必須一併提供可重現問題的單元測試代碼**。
- **活知識庫與規則昇華機制 (`Journal.md`)**：記錄架構避坑經驗；當同一問題出現 **2 次以上**，自動升格寫入憲法 `AGENTS.md`。

---

## 目錄結構概覽

```text
.
├── .agents/                                # 核心 Agent 治理目錄
│   ├── AGENTS.md                           # 通用 Agent 憲法與行為守則 (Master Constitution)
│   ├── Journal.md                          # 活知識庫範本與累積指南
│   ├── rules/
│   │   ├── workspace.md                    # 通用工作區邊界與驗證關卡規範
│   │   └── toolchains/                     # 各語言工具鏈規範模板 (Python, Node, Rust, Go)
│   └── skills/
│       ├── README.md                       # Canonical Skill Registry 索引
│       ├── agent-governance-audit/         # 治理規範一致性稽核
│       ├── cross-agent-collaboration/      # 跨代理協作與 Handoff 狀態機
│       ├── codex-antigravity-bridge/       # Codex ↔ Antigravity 橋接與沙盒
│       ├── jules_coding/                   # Jules 雲端委派與驗收邊界
│       ├── modular-refactoring/            # 模組化解耦與型別契約優先
│       ├── huge-component-refactoring/     # 250 行巨型代碼拆分與熱路徑保護
│       ├── code-quality-linting/           # PEP 8 語法規範、Linter 與 Formatter
│       ├── pr-author-maintainer/           # PR 作者工作流 (Living Body & 防自我宣告)
│       ├── pr-review-evaluation/           # PR 審查 (原生 Inline Comments & 測試代碼義務)
│       ├── github-security-audit/          # GitHub 安全審查 (CodeQL/Dependabot)
│       └── portable-release-validation/    # 發行產物打包與執行期冒煙測試
├── templates/                              # 領域技能範本庫 (Pure Math, Protocol, Design System)
├── agent_cli/                              # 治理與腳手架 CLI 套件 (Zero External Dependencies)
├── tests/                                  # 100% 覆蓋之單元測試套件 (25 passed)
├── scripts/                                # 便利執行入口腳本
├── pyproject.toml                          # 專案標準設定
├── SECURITY.md                             # 雙語安全性政策與威脅模型
├── README.md                               # 繁體中文說明文件
└── README.en.md                            # 英文說明文件
```

---

## 快速上手 (Quick Start)

### 步驟 1：執行自我治理稽核
```bash
python scripts/run_governance_audit.py
```

### 步驟 2：執行全套單元測試
```bash
pytest tests/ -v
```

### 步驟 3：一鍵將治理架構注入任意專案
使用框架內建的腳手架工具，可在數秒內為任何現有或全新專案導入完整的 `.agents` 治理體系：

```bash
# 1. 完整版 (包含全部 11 個核心技能)
python scripts/init_agent_workspace.py --target /path/to/my-project --project-name "MyProject" --preset full

# 2. Python 專案精簡版 (包含 Linter、PR 管理、安全稽核與模組化重構)
python scripts/init_agent_workspace.py --target /path/to/python-app --preset python

# 3. TypeScript / Node 專案精簡版
python scripts/init_agent_workspace.py --target /path/to/web-app --preset node
```

---

## 11 大核心技能矩陣 (Canonical Skills)

| 技能 ID | 核心職責 | 關鍵規範與工具 |
|---|---|---|
| `code-quality-linting` | 語法標準化、代碼風格合規 | PEP 8 / PEP 257 / TypeScript Strict / `verify_code_style.py` |
| `agent-governance-audit` | 治理規範稽核、Skill ID 檢驗 | 檢查 canonical ID、Frontmatter、死連結 / `auditor.py` |
| `cross-agent-collaboration` | 多 Agent 非同步協作 | Single Writer Ownership、文字狀態機 (`active`/`handoff`) |
| `codex-antigravity-bridge` | 跨代理 CLI 與自動化通訊 | 非互動沙盒配置、固定 Token 冒煙測試 / `Invoke-AgyCrossAgentSmoke.ps1` |
| `jules_coding` | 雲端 Agent 委派安全邊界 | 前置授權、無憑證不猜測、本地全套 Diff 驗收 |
| `modular-refactoring` | 架構模組化與解耦 | 純函數抽離、型別契約優先 (Typed Contract)、測試先行 |
| `huge-component-refactoring` | 巨型代碼拆分與熱路徑防護 | 250 行拆分原則、狀態機抽離、Hot-Path 零物件分配 |
| `pr-author-maintainer` | PR 作者與維護者工作流程 | 禁止自我斷言 Mergeable、Living PR Body 同步 / `manage_pr_author.py` |
| `pr-review-evaluation` | 標準化 Review 與建議代碼 | 原生 GitHub Inline Comments、Blocking 附帶測試義務 / `submit_pr_review.py` |
| `github-security-audit` | 全維度安全弱點收集與審查 | CodeQL、Dependabot、Secret Scanning 報告匯出 / `collect_security_alerts.py` |
| `portable-release-validation` | 發行產物打包與驗證 | 乾淨環境啟動測試、路徑隔離性檢驗、連接埠防撞 |

---

## 貢獻與開發 (Contributing)

歡迎提交 Issue、討論與 Pull Request！請參閱 [CONTRIBUTING.md](CONTRIBUTING.md) 瞭解詳細分支規範、Commit 前驗證門檻與身分標記格式。

---

## 授權條款 (License)
 
本專案採用 [MIT](LICENSE-MIT) OR [Apache-2.0](LICENSE-APACHE) 雙授權模式，使用者可依自身法務政策自由選用。詳細條款請參閱 [LICENSE](LICENSE)、[LICENSE-MIT](LICENSE-MIT) 與 [LICENSE-APACHE](LICENSE-APACHE)。
