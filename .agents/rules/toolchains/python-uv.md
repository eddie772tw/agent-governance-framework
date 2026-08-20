# Python / uv 工具鏈標準規範

## 核心要求
1. **Python 版本**：標準使用 Python 3.12+ (推薦 Python 3.13)。
2. **虛擬環境管理**：統一使用專案根目錄之 `.venv`，透過 `uv` 高速管理。
3. **依賴管理**：
   - 使用 `uv pip install -r requirements.txt` 或 `uv sync` / `pyproject.toml`。
   - 引入新依賴前必須執行防幻覺查驗協議。

## 標準命令
```powershell
# 虛擬環境建立
uv venv --python 3.13

# 靜態代碼檢查與格式化
uv run --no-project --python .venv\Scripts\python.exe ruff check .
uv run --no-project --python .venv\Scripts\python.exe ruff format --check .

# 單元測試執行
uv run --no-project --python .venv\Scripts\python.exe python -m pytest tests/
```
