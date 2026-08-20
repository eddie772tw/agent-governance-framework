---
name: code-quality-linting
description: 當撰寫、修改或重構程式碼、配置專案 Linter/Formatter 工具、落實 PEP 8 等語法與代碼風格規範，或於 Commit/PR 前執行靜態語法檢查時觸發此技能。
---

# 代碼品質與語法規範檢查 (Code Quality & Linting Standards)

## 觸發條件
1. **編寫或修改代碼**：任何 Python, TypeScript/JavaScript, Rust, Go 等原始碼變更。
2. **專案工具鏈配置**：設定或調整 Linter、Formatter 與靜態分析工具配置（如 `pyproject.toml` 中的 Ruff/mypy 設定、`eslint.config.js`、`rustfmt.toml` 等）。
3. **Commit 前合規驗證**：在提交任何 commit 或發起 PR 前，落實執行代碼風格與語法檢查。
4. **清理 Lint 警告**：修復既有專案中的代碼異味 (Code Smells)、未使用的 Import 或 PEP 8 違規。

---

## 各語言語法與代碼風格規範矩陣

| 語言 | 語法與風格規範 | 推薦 Linter / 靜態分析 | 推薦 Formatter |
|---|---|---|---|
| **Python** | **PEP 8** (代碼風格)、**PEP 257** (Docstring)、型別標註 | **Ruff** (`ruff check`)、**mypy** / **pyright** | **Ruff** (`ruff format`) 或 **Black** + **isort** |
| **TypeScript / JS** | Airbnb / Standard Style、TypeScript Strict | **ESLint** 或 **Biome** | **Prettier** 或 **Biome** |
| **Rust** | Rust API Guidelines、2021/2024 Edition 慣例 | **Clippy** (`cargo clippy -- -D warnings`) | **Rustfmt** (`cargo fmt --check`) |
| **Go** | Effective Go、Go Code Review Comments | **golangci-lint**、`go vet` | **gofmt** / **goimports** |

---

## 核心規範與不變量 (Core Invariants)

### 1. 零容忍與無遮蔽原則 (Zero-Tolerance & No Blind Suppression)
- **原則**：代碼提交前必須達到 **0 錯誤、0 警告**。
- **嚴格限制**：嚴禁為求快速通過檢查而濫用廣泛的規則忽略註解（例如單行 `# noqa` 或 `eslint-disable` 必須附帶具體錯誤代碼與充分註解理由，如 `# noqa: E402 (延遲導入以動態配置路徑)`）。

### 2. 確定性格式化 (Deterministic Formatting)
- 專案必須具備統一的格式化設定檔（如 `line-length = 100`、縮排標準、換行規則與 Import 排序）。
- 所有 Agent 必須在儲存檔案後執行專案指定的 Formatter，杜絕因編輯器或作業系統差異造成的 Whitespace 雜訊。

### 3. 語法檢查融入 Pre-Commit 流程
在執行 `git commit` 前，必須落實執行所屬語言的語法檢查命令。

---

## 常用工具指令與操作 SOP

### 1. Python 專案 (以 Ruff 為例)
```bash
# 檢查語法與 PEP 8 風格違規
ruff check .

# 自動修復可安全修正之違規 (如未使用的 Import、排序等)
ruff check --fix .

# 檢查代碼格式化狀態
ruff format --check .

# 執行自動格式化
ruff format .
```

### 2. TypeScript / Node 專案
```bash
# 執行 ESLint 靜態檢查
pnpm lint

# 執行 Prettier 格式化驗證
pnpm exec prettier --check .
```

### 3. Rust 專案
```bash
# 格式化檢查
cargo fmt --check

# Clippy 嚴格檢查 (將警告視為錯誤)
cargo clippy --all-targets -- -D warnings
```

### 4. 內建通用檢查腳本
框架提供跨語言自動偵測與檢查工具：
```bash
# 檢查工作區代碼風格
python .agents/skills/code-quality-linting/scripts/verify_code_style.py --check

# 自動格式化與安全修復
python .agents/skills/code-quality-linting/scripts/verify_code_style.py --fix
```
