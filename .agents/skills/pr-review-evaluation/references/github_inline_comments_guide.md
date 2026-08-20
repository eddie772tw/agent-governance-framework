# GitHub PR Review 與 Inline Comments 整合參考指南

本指南詳細說明 GitHub Pull Request Review 機制、原生 Inline Review Comments 之 API 規格、Code Suggestion 語法、Diff Hunk 邊界規則以及除錯防護措施。

---

## 1. GitHub PR Review 核心概念

在 GitHub PR 審查體系中，審查分為兩個層次：
1. **頂層 Review (Top-level Review)**：包含整體的審查結論（`body`）與狀態事件（`event`: `COMMENT` | `APPROVE` | `REQUEST_CHANGES`）。必須包含 `{代號} as {Agent}` 頭尾身分標記（例如 `Gemini as Antigravity review — ...` 與 `Reviewer: Gemini as Antigravity`），以區分共用 GitHub 帳號時的發言主體。
2. **行內評論 (Inline Review Comments / Review Threads)**：直接錨定在 PR 程式碼變更 Diff 特定檔案、特定行號（或行號區間）上的具體評論與程式碼修改建議（Suggestions）。

---

## 2. GitHub REST API 規格

### 2.1 批次原子提交 Review (推薦)

- **Endpoint**：`POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews`
- **說明**：一次性原子提交頂層結論與多筆行內評論。若有任何一筆 comment 格式或行號錯誤，整筆 review 將失敗回傳 422，確保評論的一致性。

#### 請求 Payload Schema (JSON)
```json
{
  "commit_id": "0123456789abcdef0123456789abcdef01234567",
  "body": "頂層 Review 總結報告 (Markdown 格式)",
  "event": "COMMENT",
  "comments": [
    {
      "path": "src/utils/math.ts",
      "line": 45,
      "side": "RIGHT",
      "body": "此處計算建議加入防護：\n```suggestion\nconst result = divisor > 0 ? value / divisor : 0;\n```"
    }
  ]
}
```

---

## 3. Diff Hunk 邊界與自動降級防護

GitHub API 限制：`comments[].line` 必須落在目前 PR 變更的 Diff Hunk 範圍內。如果指向未變更的上下文外部行號，API 會直接報錯 422 Unprocessable Entity。

`submit_pr_review.py` 工具具備自動 Diff 解析與超界降級機制：當偵測到行號超界時，會自動將該行內評論內容整併至頂層 Review Body 中，確保提交絕不中斷。
