# 貢獻指南 (Contributing Guide)

感謝您對 Universal Agent Governance Framework 的關注與貢獻！

---

## 開發與測試流程

1. **分支規範**：請自 `main` 分支建立特性分支（例如 `feat/new-skill` 或 `fix/auditor-regex`）。
2. **Commit 前測試**：
   ```bash
   ruff check .
   ruff format --check .
   python scripts/run_governance_audit.py
   pytest tests/ -v
   ```
3. **身分標記**：請於 PR Body 與留言中標註 `{代號} as {Agent}` 或 `{代號} as Human`。
4. **禁止自我斷言**：PR 內文禁止包含「Ready to merge」、「LGTM」等自我斷言詞句。
