# Node.js / pnpm 工具鏈標準規範

## 核心要求
1. **Node.js 版本**：Node.js 20+ LTS 或 22+。
2. **套件管理器**：強制使用 `pnpm`，維持鎖定檔 `pnpm-lock.yaml` 一致性。
3. **測試與建置**：單元測試推薦 Vitest，建置使用 Vite 或 TypeScript Compiler。

## 標準命令
```bash
# 安裝相依
pnpm install --frozen-lockfile

# 靜態檢查與型別驗證
pnpm lint
pnpm exec tsc --noEmit

# 單元測試
pnpm test

# 生產建置
pnpm build
```
