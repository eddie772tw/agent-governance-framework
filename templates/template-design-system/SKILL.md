---
name: template-design-system
description: (範本技能) 當開發或重構前端 UI 元件庫、維護樣式變數規範、主題切換防閃爍與視覺行為標準時參考本範本。
---

# UI 設計系統與視覺規範技能範本 (Design System Standards)

> [!NOTE]
> 本文件為範本技能。若專案具備自訂 UI 元件庫或設計系統，可將本範本複製至 `.agents/skills/<your-design-system>/SKILL.md` 並客製化。

---

## 核心設計原則

1. **分層樣式架構**：
   - **Layer 1 (核心佈局與語意標籤)**：底層 CSS 框架與響應式格線系統。
   - **Layer 2 (主題與視覺面板)**：自訂調色盤、玻璃擬態 (Glassmorphism)、暗色/亮色主題與霓虹變數。
2. **主題防閃爍 (Anti-FOUC)**：確保頁面首幀載入時依據使用者的主題設定（如 `data-theme` 屬性）立即正確渲染，避免出現白屏閃爍。
3. **禁用硬編碼顏色與字體**：所有組件內部一律引用 CSS 自訂屬性 (CSS Variables)，嚴禁在組件內寫死 HEX 色碼或像素字級。
4. **無裝飾性符號規範 (No Decorative Emojis)**：UI 介面字串保持極簡與專業，使用向量圖示庫 (SVG / Icon font) 取代 Emoji。

---

## 佈局與彈窗規範

1. **版型零擠壓原則**：嚴禁在頁面內容區域動態插入會推擠現有 DOM 高度的大型 Alert 區塊。
2. **懸浮與 Popover 規範**：狀態提醒與詳細資訊一律採用懸浮 Popover 或全域 Toast 視窗，保持主要視覺佈局穩定。
