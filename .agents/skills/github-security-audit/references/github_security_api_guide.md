# GitHub 安全檢測 API 與權限參考指南

本指南說明如何透過 GitHub REST API 與 GitHub CLI (`gh`) 查詢、彙整並處置專案的安全警報。

---

## 1. 支援的安全維度與 API 端點

| 檢測維度 | 查詢端點 | 說明 |
|---|---|---|
| **Code Scanning** | `GET /repos/{owner}/{repo}/code-scanning/alerts` | CodeQL 與第三方靜態掃描發現的程式碼缺陷 |
| **Dependabot** | `GET /repos/{owner}/{repo}/dependabot/alerts` | 專案相依套件弱點與 CVE 告警 |
| **Secret Scanning** | `GET /repos/{owner}/{repo}/secret-scanning/alerts` | 意外提交至代碼庫的 Token 或私鑰洩漏 |
| **Security Advisories** | `GET /repos/{owner}/{repo}/security-advisories` | 儲存庫層級之安全性通報與發布紀錄 |

---

## 2. 權限需求

執行安全 API 查詢前，確認 GitHub Token 具備以下權限範圍：
- `security_events`: 讀寫 Code Scanning 警報
- `repo` 或 `read:org`: 讀取私有儲存庫之 Dependabot / Secret Scanning 警報
