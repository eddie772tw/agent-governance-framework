# Universal Agent Governance Framework (通用 Agent 治理架構)

[![CI](https://github.com/eddie772tw/agent-governance-framework/actions/workflows/agent-governance-ci.yml/badge.svg)](https://github.com/eddie772tw/agent-governance-framework/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)

專為現代 AI 輔助軟體開發與多代理協作（Google Antigravity、OpenAI Codex、Google Jules 與人類團隊）設計的**高紀律、中性化、具自我稽核能力之通用 Agent 治理框架**。

---

## 核心設計理念與架構特色

1. **技能發現關卡 (Skill Discovery Gate)**：
   - 強制建立唯一的 Canonical Skill Registry (`.agents/skills/README.md`)。
   - Agent 在執行任何任務前必須依觸發條件精準探索、完整閱讀 `SKILL.md`，防止上下文混淆。
2. **多代理非同步協作與身分標記 (`{代號} as {Agent}`)**：
   - 建立嚴格的 Single Writer Ownership 鎖定與標準化 Handoff 狀態機。
   - 共用 GitHub 帳號時，強制標註身分（例如 `Gemini as Antigravity`、`Luna as Codex`），消除審查歸屬歧義。
3. **PR 職責分化與嚴格邊界**：
   - **PR Author/Maintainer**：動態維護 Living PR Body、強制執行 Pre-Commit 測試門檻，**嚴禁自我斷言「Ready to merge / LGTM」**。
   - **PR Reviewer**：發表標準化 Review，原生 GitHub Inline Comments / Suggestions 支援，**CI 未涵蓋之 Blocking 意見強制附帶可重現測試代碼**。
4. **防幻覺套件查驗協議 (Anti-Hallucination Protocol)**：
   - 嚴禁憑 LLM 記憶直接寫入相依檔案；強制執行 npm / PyPI / crates.io / Go 官方 Registry 查驗與寬鬆授權審查。
5. **活知識庫與規則昇華機制 (Living Journal)**：
   - 結構化沉澱避坑經驗（`proposed` -> `adopted` -> `superseded`）。
   - 當同一問題出現 **2 次以上**，自動升格納入全域憲法 `AGENTS.md`。

---

## 目錄結構概覽

```text
.
├── .agents/                                # 核心 Agent 治理目錄
│   ├── AGENTS.md                           # 通用 Agent 憲法與行為守則 (Master Constitution)
│   ├── Journal.md                          # 活知識庫範本與累積指南
│   ├── rules/
│   │   ├── workspace.md                    # 通用工作區邊界與驗證關卡規範
│   │   └── toolchains/                     # 各語言工具鏈規範模板
│   │       ├── python-uv.md                # Python 3.13 + uv 規範
│   │       ├── node-pnpm.md                # Node.js + pnpm + Vitest 規範
│   │       ├── rust-cargo.md               # Rust + Cargo 規範
│   │       └── go-toolchain.md             # Go 規範
│   └── skills/
│       ├── README.md                       # Canonical Skill Registry 索引
│       ├── agent-governance-audit/         # 治理稽核技能
│       ├── cross-agent-collaboration/      # 跨代理協作與 Handoff 技能
│       ├── codex-antigravity-bridge/       # Codex ↔ Antigravity 橋接技能
│       ├── jules_coding/                   # Jules 委派技能
│       ├── modular-refactoring/            # 模組化與架構解耦技能
│       ├── huge-component-refactoring/     # 巨型元件與熱路徑重構技能
│       ├── pr-author-maintainer/           # PR 作者與維護者工作流技能 (含 manage_pr_author.py)
│       ├── pr-review-evaluation/           # PR 審查與建議技能 (含 submit_pr_review.py)
│       ├── github-security-audit/          # GitHub 安全審查技能 (含 collect_security_alerts.py)
│       └── portable-release-validation/    # 發行驗證技能
├── templates/                              # 領域技能範本庫 (Math, Protocol, Design System)
├── agent_cli/                              # 治理與腳手架 CLI 套件 (Zero External Dependencies)
│   ├── scaffolder.py                       # 專案一鍵初始化注入
│   └── auditor.py                          # 治理規範一致性稽核
├── tests/                                  # 100% 覆蓋之單元測試套件
└── scripts/                                # 便利執行入口腳本
```

---

## 快速上手 (Quick Start)

### 1. 執行專案自我治理稽核
```bash
python scripts/run_governance_audit.py
```

### 2. 執行全套單元測試
```bash
pytest tests/ -v
```

### 3. 一鍵注入治理架構至任意目標專案
```bash
# 完整版 (包含所有 10 大核心技能)
python scripts/init_agent_workspace.py --target /path/to/my-project --preset full

# 針對 Python 專案之精簡版
python scripts/init_agent_workspace.py --target /path/to/my-project --preset python
```

---

## 11 大核心技能矩陣

| 技能 ID | 職責與範疇 | 自動化工具支援 |
|---|---|---|
| `agent-governance-audit` | 稽核規範、Skill ID 漂移、死連結與語言邊界 | `agent_cli/auditor.py` |
| `cross-agent-collaboration` | 多代理任務狀態機、Ownership 鎖定與 Handoff 協議 | 標準 Markdown 狀態範本 |
| `codex-antigravity-bridge` | 跨代理 CLI 呼叫、沙盒配置與固定 Token 冒煙測試 | `Invoke-AgyCrossAgentSmoke.ps1` |
| `jules_coding` | 雲端/非同步代理委派安全邊界與結果驗收 | 授權審查與 Diff 檢查清單 |
| `modular-refactoring` | 高內聚低耦合、純函數抽離與型別契約優先 | 測試先行 SOP |
| `huge-component-refactoring` | 250 行代碼拆分原則、狀態機抽離與高頻熱路徑保護 | 零物件分配與資源清理規範 |
| `code-quality-linting` | 靜態語法檢查、PEP 8/代碼風格合規與 Formatter 配置 | `verify_code_style.py` |
| `pr-author-maintainer` | PR 作者工作流、Living PR Body 同步與身分標記 | `manage_pr_author.py` |
| `pr-review-evaluation` | 標準化 Review、原生 Inline Comments 與建議代碼提交 | `submit_pr_review.py` |
| `github-security-audit` | CodeQL、Dependabot、Secret Scanning 自動收集 | `collect_security_alerts.py` |
| `portable-release-validation` | 獨立產物打包、執行期相依隔離與啟動冒煙測試 | 發行前檢核表 |

---

## 授權條款

本專案採用 [MIT License](LICENSE) 授權。
