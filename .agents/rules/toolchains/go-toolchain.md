# Go 工具鏈標準規範

## 核心要求
1. **Go 版本**：Go 1.22+。
2. **依賴管理**：透過 `go.mod` 與 `go.sum` 管理，執行 `go mod tidy`。
3. **品質與安全**：使用 `golangci-lint` 或 `go vet`。

## 標準命令
```bash
# 依賴整理
go mod tidy

# 靜態檢查
go vet ./...

# 執行測試
go test -v -race ./...

# 格式化檢查
gofmt -l .
```
