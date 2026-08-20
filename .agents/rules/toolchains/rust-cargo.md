# Rust / Cargo 工具鏈標準規範

## 核心要求
1. **Rust 版本**：Rust 1.80+ (Stable Edition 2021+)。
2. **依賴管理**：透過 `Cargo.toml` 與 `Cargo.lock` 精確管理。
3. **品質與安全**：強制執行 `cargo clippy` 與 `cargo fmt`。

## 標準命令
```bash
# 格式化檢查
cargo fmt --check

# Linter 靜態分析
cargo clippy --all-targets -- -D warnings

# 單元與整合測試
cargo test --all

# 建置檢查
cargo check --all
```
