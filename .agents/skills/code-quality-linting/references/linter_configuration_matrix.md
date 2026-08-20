# 多語言 Linter 與 Formatter 配置矩陣指南

本文件提供各主要程式語言主流 Linter 與 Formatter 的標準配置範本，供 Agent 在初始化新專案或配置 CI 時直接套用。

---

## 1. Python 配置標準 (pyproject.toml)

Ruff 是目前 Python 生態中最快速且整合度最高的 Linter 與 Formatter，能同時取代 Flake8, Black, isort, pyupgrade 等工具。

```toml
[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
# E: pycodestyle errors, F: Pyflakes, W: pycodestyle warnings, I: isort, BLE: blind-except
select = ["E", "F", "W", "I"]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

---

## 2. JavaScript / TypeScript 配置標準

### ESLint Flat Config (`eslint.config.js`)
```javascript
import js from "@eslint/js";
import tsPlugin from "@typescript-eslint/eslint-plugin";
import tsParser from "@typescript-eslint/parser";

export default [
  js.configs.recommended,
  {
    files: ["**/*.ts", "**/*.tsx"],
    languageOptions: {
      parser: tsParser,
    },
    plugins: {
      "@typescript-eslint": tsPlugin,
    },
    rules: {
      "no-unused-vars": "off",
      "@typescript-eslint/no-unused-vars": ["error", { argsIgnorePattern: "^_" }],
      "semi": ["error", "always"],
      "quotes": ["error", "double"],
    },
  },
];
```

### Prettier (`.prettierrc`)
```json
{
  "semi": true,
  "singleQuote": false,
  "tabWidth": 2,
  "printWidth": 100,
  "trailingComma": "es5"
}
```

---

## 3. Rust 配置標準

### Rustfmt (`rustfmt.toml`)
```toml
max_width = 100
hard_tabs = false
tab_spaces = 4
edition = "2021"
newline_style = "Auto"
use_field_init_shorthand = true
```

### Clippy (`clippy.toml`)
```toml
msrv = "1.80.0"
cognitive-complexity-threshold = 25
```

---

## 4. Go 配置標準 (`.golangci.yml`)

```yaml
run:
  timeout: 5m
  tests: true

linters:
  enable:
    - errcheck
    - gosimple
    - govet
    - ineffassign
    - staticcheck
    - unused
    - gofmt
    - goimports

linters-settings:
  govet:
    check-shadowing: true
  gofmt:
    simplify: true
```
