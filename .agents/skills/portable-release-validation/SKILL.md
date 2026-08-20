---
name: portable-release-validation
description: 當建立發行版 (Release Artifact)、獨立執行檔、Sidecar 啟動流程、動態連接埠或跨平台發行產物驗證時觸發此技能。
---

# 發行產物與可攜式套件驗證 (Portable Release Validation)

## 發行前檢查清單 (Pre-Release Checklist)

1. **版本號與元數據一致性**：確認 Git Tag、設定檔版本號（`package.json` / `pyproject.toml` / `Cargo.toml`）與 Release Notes 一致。
2. **安全支援狀態**：檢查並更新 `SECURITY.md` 的 Supported Versions 支援版本矩陣。
3. **路徑隔離性檢驗**：檢查打包目錄只包含必要執行期檔案，**嚴禁殘留開發機本機絕對路徑**或硬編碼開發環境設定。
4. **全套測試與靜態檢查**：發行前必須在乾淨工作區 100% 通過全套自動化測試與建置指令。

---

## 啟動與執行期冒煙測試 (Runtime Smoke Testing)

- **獨立啟動測試**：在乾淨無開發相依的目標環境中啟動發行產物，確認初始化事件與日誌記錄正常。
- **動態資源與連接埠衝突處理**：若應用程式涉及網路服務，驗證埠號碰撞時的 Fallback 機制與日誌宣告。
- **進程生命週期與資源釋放**：確認應用程式關閉時能完整清理子進程、Socket、臨時檔案與鎖定檔。

---

## 驗收與完成條件

- 乾淨目標作業系統環境下能成功啟動並通過基本功能冒煙測試。
- 打包產物中無多餘的快取、測試數據或開發相依。
- 執行 `git diff --check`，並將已驗證的發行數據記錄至 `.agents/Journal.md`。
