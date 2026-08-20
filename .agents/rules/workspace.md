# 工作區邊界與驗證規範 (Workspace Rules)

## 模組分層與職責隔離原則

1. **核心領域邏輯層 (Domain / Business Logic)**：
   - 必須維持為無副作用純函數 (Pure Functions)。
   - 嚴禁直接依賴 UI 框架狀態、DOM 結構或全域外部變數。
   - 所有輸入必須具備確定性，並提供完整的單元測試覆蓋。
2. **數據通訊與外部介面層 (I/O / Network / Protocol)**：
   - 負責資料接收、格式轉譯、序列化與驗證。
   - 保持非同步主循環無阻塞 (Non-blocking I/O)。
   - 嚴格進行外部輸入與路徑安全性檢驗（防注入與目錄穿越）。
3. **視圖呈現與使用者介面層 (Presentation / UI / CLI)**：
   - 僅負責使用者互動與視覺化展示。
   - 嚴禁在 UI 元件內混入複雜的業務計算公式。

---

## 任務完成驗證關卡 (Verification Gate)

在完成或宣佈任何開發、重構或修復任務前，Agent 必須執行所屬專案的標準驗證指令，例如：

- **靜態分析與代碼格式化檢查**（依專案配置如 `ruff check`, `eslint`, `cargo clippy`, `golangci-lint`）。
- **單元與整合測試**（依專案配置如 `pytest`, `vitest`, `cargo test`, `go test`）。
- **型別檢查與專案建置**（如 `tsc --noEmit`, `cargo check`, `pnpm build`）。

> [!WARNING]
> 嚴禁為了使測試通過而隨意放寬測試條件、降低驗證覆蓋率或竄改斷言標準。

---

## 工具鏈標準管理

專案應於 `.agents/rules/toolchains/` 明確指定標準開發工具鏈版本與命令規範，確保所有 Agent 與 CI 環境維持一致性。
