---
name: template-stream-protocol
description: (範本技能) 處理二進位封包解析、高頻串流通訊 (UDP/WebSocket/gRPC)、位元組偏移量校驗與非同步零阻塞保護時參考本範本。
---

# 高頻串流與二進位通訊協議技能範本 (High-Frequency Stream & Protocol)

> [!NOTE]
> 本文件為範本技能。若專案涉及二進位通訊協定、UDP/TCP 封包解析或高頻數據串流，可將本範本複製至 `.agents/skills/<your-protocol>/SKILL.md` 並客製化。

---

## 核心通訊原則

1. **高頻主循環零同步阻塞**：在高頻數據接收回調（如 60Hz+ UDP / WebSocket）內，**絕不可執行同步檔案寫入、DNS 解析或資料庫查詢**。
2. **二進位結構嚴格解碼**：二進位封包解析必須使用精確的 Struct 佈局（如 Python `struct.unpack`、Rust `nom` / `bincode`），並提供封包長度與校驗和檢查。
3. **防止自轉風暴 (Loopback Storm Prevention)**：若具備封包轉發 (Passthrough) 功能，必須在設定層級主動防範轉發目標與本機監聽地址碰撞，避免引發死循環風暴。

---

## 測試與驗證

1. **模擬封包回放測試**：建立 Mock 封包產生器與二進位 fixture 檔案，驗證在各版本封包格式下的解碼正確性。
2. **壓力與異常封包測試**：注入截斷封包、超長封包與畸形位元組，驗證系統能優雅丟棄而不崩潰。
