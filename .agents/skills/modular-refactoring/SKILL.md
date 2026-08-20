---
name: modular-refactoring
description: 當需要拆分底層邏輯、建立功能模組、整理 domain/API 邊界或建立跨前後端型別契約時觸發此技能。
---

# 模組化拆分與架構重構 (Modular Architecture Refactoring)

## 與其他技能之分工
- 巨型 UI 元件、視圖結構或高頻渲染/計算 Hot-path：使用 `huge-component-refactoring`。
- 模組架構邊界、業務領域邏輯 (Domain Logic)、API 契約與可測試性：使用本技能。
- 兩者皆適用時，先以 `huge-component-refactoring` 保護高頻熱路徑，再用本技能整理契約邊界。

---

## 模組化重構 SOP

1. **確認邊界與基線**：
   - 閱讀 `AGENTS.md`、`Journal.md` 與所屬工具鏈規則。
   - 執行既有測試套件，確認重構前的測試基線（全綠燈）。
2. **定義明確契約 (Typed Contract First)**：
   - 先定義輸入/輸出的 TypeScript Interface、Python Dataclass/TypedDict 或 Rust Struct。
   - 嚴禁以內部實作細節或未具型別的隨意字典作為跨模組契約。
3. **純函數與領域邏輯抽離**：
   - 將所有核心演算法、業務規則與格式轉換抽離為無狀態純函數 (Pure Functions)。
   - 嚴禁將業務邏輯或計算公式零散雜揉於 UI 或網路層。
4. **單元測試先行 (Isolation Tests)**：
   - 抽出的純邏輯模組必須具備獨立單元測試（包含邊界值、極端值與例外處理）。
   - 確認單元測試通過後，再串接回上層模組或 UI。
5. **依賴方向與向後相容性檢驗**：
   - 檢驗模組依賴方向（高層依賴抽象，低層不逆向依賴視圖）。
   - 嚴禁引入循環依賴 (Circular Dependency) 或創造無邊界的 God Object。
6. **全套回歸測試**：
   - 執行專案全套測試與 Linter，確認零破壞性回歸。
   - 執行 `git diff --check`。

---

## 反模式 (Anti-patterns)

- 在重構過程中改變核心演算法或 API 外部語意。
- 單一模組同時處理網路通訊、業務運算、快取、狀態管理與 UI 渲染。
- 未建立單元測試基線即進行大規模目錄搬移。
