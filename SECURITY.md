# Security Policy / 安全性政策

[English](#english) | [繁體中文](#繁體中文)

---

<a name="english"></a>
## English

### Supported Versions

We actively provide security updates and patches for the following versions of the **Universal Agent Governance Framework**:

| Version | Supported | Status / Recommendation |
|---|---|---|
| `1.x` | :white_check_mark: | Active support and maintenance |
| `< 1.0` | :x: | Unsupported |

---

### Reporting a Vulnerability

We take the security of software development and AI agent governance seriously. If you discover a vulnerability or security flaw in this framework or its automation scripts, please disclose it responsibly.

#### How to Report
1. **GitHub Private Vulnerability Reporting (Recommended)**:
   - Go to the repository's **Security** tab.
   - Under **Advisories**, click **Report a vulnerability**.
   - Provide a detailed summary and proof-of-concept (PoC).
2. **Public Disclosure Warning**:
   - **DO NOT** report security vulnerabilities via public GitHub issues, discussions, or pull requests.

#### Response Timeline
- **Initial Acknowledgement**: Within **48 hours**.
- **Triage & Assessment**: Within **7 days**.
- **Coordinated Patch & Advisory**: A fix will be developed and released with credit in the Security Advisory.

---

### AI Agent Security Architecture & Threat Model

The Universal Agent Governance Framework is built around defensive AI engineering practices:

1. **Anti-Hallucination Package Verification Protocol**:
   - **Threat**: LLMs hallucinating nonexistent libraries or falling victim to typosquatting and dependency confusion attacks.
   - **Defense**: Mandatory 3-step verification against official registries (PyPI, npm, crates.io, Go) and strict permissive open-source license checks (MIT/Apache-2.0).
2. **Path Security & Containment**:
   - **Threat**: Unsanitized user inputs or prompt parameters leading to directory traversal (`../`) or unauthorized file overwrites.
   - **Defense**: Enforced path containment validation (`safe_resolve_path` / `safe_join_under_dir`) across all file access routines.
3. **Non-Destructive Git Worktree Invariant**:
   - **Threat**: Autonomous agents executing destructive Git commands (`git reset --hard`, `git clean -fd`) and wiping uncommitted human work.
   - **Defense**: Strict single writer ownership locking, pre-commit validation gates, and immutable worktree preservation rules.
4. **Automated Vulnerability Monitoring**:
   - Built-in `collect_security_alerts.py` tool automates continuous monitoring across CodeQL static analysis, Dependabot dependency vulnerabilities, and Secret Scanning token leaks.

---

<a name="繁體中文"></a>
## 繁體中文

### 支援版本 (Supported Versions)

我們為 **Universal Agent Governance Framework** 以下版本提供安全修補與維護支援：

| 版本 | 支援狀態 | 建議措施 |
|---|---|---|
| `1.x` | :white_check_mark: | 目前處於主動維護與安全修補支援中 |
| `< 1.0` | :x: | 不再支援 |

---

### 回報安全性弱點 (Reporting a Vulnerability)

我們極度重視 AI 代理協作與軟體工程框架之安全性。若您在框架規範或自動化腳本中發現安全漏洞，感謝您透過負責任的方式向我們通報。

#### 回報方式
1. **GitHub 私密安全性通報 (推薦)**：
   - 前往儲存庫的 **Security** 頁籤。
   - 點擊 **Advisories** -> **Report a vulnerability**。
   - 填寫詳細說明、影響範疇與重現步驟 (PoC)。
2. **禁止公開披露警告**：
   - **請勿**透過公開的 GitHub Issue、PR 或 Discussion 回報未修補的安全弱點。

#### 回應時程承諾
- **初步確認接收**：**48 小時內**。
- **評估與分級**：**7 天內**完成風險評估並回覆後續處置進度。
- **修復發布與致謝**：修復完成後將發布 GitHub Security Advisory 並致謝通報者。

---

### AI Agent 安全架構與威脅模型 (Threat Model)

本框架針對 AI Agent 開發環境建立了四大縱深防禦機制：

1. **三步驟防幻覺套件查驗協議 (Anti-Hallucination Protocol)**：
   - **威脅**：大語言模型幻覺引用不存在之套件，引發拼寫搶註 (Typosquatting) 或依賴混淆攻擊。
   - **防禦**：強制執行官方 Registry (PyPI, npm, crates.io, Go) 查驗，並嚴格審查開源授權（如 MIT / Apache-2.0），經人類確認後方可安裝。
2. **路徑安全與目錄包含性檢驗 (Path Security & Containment)**：
   - **威脅**：外部輸入或非受控 Prompt 導致目錄穿越 (`../`) 或非預期的檔案覆寫。
   - **防禦**：所有檔案讀寫必須通過目錄包含性檢驗，嚴禁直接拼接未驗證之路徑。
3. **非破壞性工作樹保護 (Non-Destructive Git Invariant)**：
   - **威脅**：多 Agent 自主執行 `git reset --hard` 或覆寫其他協作者未提交之檔案。
   - **防禦**：落實 Single Writer Ownership 鎖定、狀態機 Handoff 協議，嚴禁執行破壞性 Git 清理指令。
4. **全維度安全自動化審查 (`github-security-audit`)**：
   - 內建自動化工具 `collect_security_alerts.py`，全自動追蹤並產出 CodeQL 靜態掃描、Dependabot 依賴漏洞、Secret Scanning 密鑰洩漏之結構化審查報告。
