# Universal Agent Governance Framework

<p align="center">
  <strong>An Open-Source AI Software Engineering Governance System designed for Multi-Agent Collaboration (Google Antigravity, OpenAI Codex, Google Jules) and Human Teams</strong>
</p>

<p align="center">
  <a href="https://github.com/eddie772tw/agent-governance-framework/actions"><img src="https://github.com/eddie772tw/agent-governance-framework/actions/workflows/agent-governance-ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python&logoColor=white" alt="Python 3.10+"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/Language-繁體中文-blue" alt="Traditional Chinese Documentation"></a>
</p>

---

## Why Agent Governance?

In the era of LLM-assisted software development, AI agents generate code at unprecedented speeds, yet frequently introduce **critical engineering chaos and security vulnerabilities**:
- **Code Style Drift**: Inconsistent code formatting that violates PEP 8, introduces lint warnings, or pollutes git diffs.
- **Hallucinated & Malicious Dependencies**: LLMs hallucinating nonexistent packages or falling prey to dependency confusion and typosquatting attacks.
- **Multi-Agent State Collisions**: Multiple autonomous agents (e.g., Antigravity and Codex) simultaneously mutating the same files on a shared branch.
- **Flawed PR Reviews & False Approvals**: Agents self-proclaiming "Ready to merge / LGTM" on their own PRs or missing line-anchored GitHub Inline Comments.
- **Knowledge Evaporation**: Architecture lessons and debugging insights disappearing once chat sessions terminate.

The **Universal Agent Governance Framework** provides a battle-tested, neutral, and self-auditing **Master Constitution and Automation Suite** that endows AI agents with the discipline, rigor, and safety standards of senior staff engineers.

---

## The Four Pillars of Governance

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                  Universal Agent Governance Framework                       │
├──────────────────────┬──────────────────────┬───────────────────────────────┤
│ 1. Syntax & Struct   │ 2. Security Defense  │ 3. Multi-Agent Collab         │
│ • PEP 8 / Zero Lint  │ • Anti-Hallucination │ • Single Writer Ownership     │
│ • Pure Logic Truth   │ • CodeQL / Dependabot│ • {Code} as {Agent} Tagging   │
│ • 250-line Refactor  │ • Path Containment   │ • Headless CLI Handshake      │
├──────────────────────┴──────────────────────┴───────────────────────────────┤
│ 4. Structured Review & Living PR Workflow                                   │
│ • Living PR Body Sync          • No Self-Asserted Mergeability (No LGTM)    │
│ • Native GitHub Inline Comments• Mandatory Test Snippet for Blocking Issues  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1. Syntax & Structural Standardization
- **PEP 8 & Strict Linter Compliance (`code-quality-linting`)**: Zero-tolerance policy for syntax errors and warnings across Python (PEP 8/PEP 257), TypeScript (Strict Mode), and Rust (Clippy). Unjustified `# noqa` / `eslint-disable` comments are strictly prohibited.
- **Deterministic Code Formatting**: Integrated `verify_code_style.py` runner supporting multi-language automated checks and formatting.
- **Single Source of Truth & Pure Functions**: Business algorithms and mathematical formulas are isolated into stateless pure functions, strictly decoupled from UI and transport layers.
- **250-Line Component Refactoring (`huge-component-refactoring`)**: Established threshold and SOP for state machine extraction, modular decomposition, and 60Hz hot-path performance protection (zero allocations in frame loops).

### 2. Enterprise-Grade Security & Supply Chain Defense
- **3-Step Anti-Hallucination Package Verification Protocol**:
  1. Never write unverified packages directly into configuration files from memory.
  2. Execute official registry CLI verification (PyPI, npm, crates.io, Go).
  3. Validate permissive open-source licenses (MIT / Apache-2.0) with human confirmation.
- **Automated Security Auditing (`github-security-audit`)**: Integrated `collect_security_alerts.py` to aggregate CodeQL code scanning, Dependabot vulnerabilities, Secret Scanning alerts, and Security Advisories into structured Markdown reports.
- **Path Security & Containment (`safe_resolve_path`)**: Mandatory directory containment checks to eliminate path traversal (`../`) vulnerabilities.

### 3. Multi-Agent & Cross-Agent Collaboration
- **Single Writer Ownership Locking**: Standard state machine (`active`, `blocked`, `handoff`, `done`) and structured handoff logs via `cross-agent-collaboration` to prevent worktree overwrite collisions.
- **Identity Tagging (`{Code} as {Agent}`)**: Mandatory identity marking (e.g., `Gemini as Antigravity`, `Luna as Codex`, `Gemini as Jules`) in PR bodies, reviews, and comments when sharing GitHub credentials.
- **Headless CLI Bridge & Sandbox (`codex-antigravity-bridge`)**: Automated cross-agent communication with headless non-interactive sandbox setup and deterministic token handshake smoke testing.
- **Cloud Agent Delegation Boundary (`jules_coding`)**: Clear protocols for asynchronous remote task delegation, permission prerequisites, and full local diff verification.

### 4. Structured Review & Living PR Workflow
- **PR Role Separation & Invariants**:
  - **PR Author / Maintainer (`pr-author-maintainer`)**:
    - **No Self-Asserted Mergeability**: Authors never declare "Ready to merge" or "LGTM" on their own PRs.
    - **Living PR Body**: Real-time synchronization of the PR description with every commit to eliminate documentation drift.
    - **Dual-Track Review & Inline Comments Checklist**: Automated extraction of GitHub inline comments into actionable Markdown checklists (`manage_pr_author.py`).
  - **PR Reviewer (`pr-review-evaluation`)**:
    - Native GitHub Inline Review Comments and Code Suggestions batch submission (`submit_pr_review.py`).
    - **Mandatory Test Snippet for Blocking Findings**: Reviewers reporting edge cases or untested execution paths must provide reproducible unit test code snippets.
- **Living Knowledge Base (`Journal.md`)**: Structured accumulation of architecture learnings (`proposed` -> `adopted` -> `superseded`). Any lesson recurring **2+ times** is automatically escalated to `AGENTS.md`.

---

## Repository Structure

```text
.
├── .agents/                                # Core Agent Governance Root
│   ├── AGENTS.md                           # Master Agent Constitution
│   ├── Journal.md                          # Living Knowledge Base & Escalation Log
│   ├── rules/
│   │   ├── workspace.md                    # Workspace Boundaries & Verification Gate
│   │   └── toolchains/                     # Deterministic Toolchain Standards (Python, Node, Rust, Go)
│   └── skills/
│       ├── README.md                       # Canonical Skill Registry Index
│       ├── agent-governance-audit/         # Governance & ID Consistency Audit
│       ├── cross-agent-collaboration/      # Multi-Agent Async Handoff & Ownership
│       ├── codex-antigravity-bridge/       # Cross-Agent CLI Bridge & Sandbox Config
│       ├── jules_coding/                   # Cloud Agent Delegation Boundary
│       ├── modular-refactoring/            # Modularity & Typed Contract First
│       ├── huge-component-refactoring/     # 250-Line Code Splitting & Hot-Path Protection
│       ├── code-quality-linting/           # PEP 8 Syntax & Linter Standards
│       ├── pr-author-maintainer/           # Living PR Body & Pre-Commit Verification
│       ├── pr-review-evaluation/           # Native Inline Comments & Review Standards
│       ├── github-security-audit/          # GitHub CodeQL / Dependabot Audit
│       └── portable-release-validation/    # Release Packaging & Runtime Smoke Tests
├── templates/                              # Domain Skill Templates (Math, Stream, Design System)
├── agent_cli/                              # Scaffolder & Auditor CLI (Zero External Dependencies)
├── tests/                                  # 100% Test Suite (25 passed)
├── scripts/                                # Scaffolding and Audit Helper Scripts
├── pyproject.toml                          # Project Metadata & Tooling Config
├── SECURITY.md                             # Bilingual Security Policy & Threat Model
├── README.md                               # Traditional Chinese Documentation
└── README.en.md                            # English Documentation
```

---

## Quick Start

### 1. Run Governance Self-Audit
```bash
python scripts/run_governance_audit.py
```

### 2. Run Test Suite
```bash
pytest tests/ -v
```

### 3. Scaffold Governance into Any Project
```bash
# Full preset (All 11 core skills)
python scripts/init_agent_workspace.py --target /path/to/project --project-name "MyProject" --preset full

# Python-optimized preset
python scripts/init_agent_workspace.py --target /path/to/python-app --preset python

# TypeScript/Node-optimized preset
python scripts/init_agent_workspace.py --target /path/to/web-app --preset node
```

---

## Canonical Skill Matrix

| Skill ID | Core Responsibility | Automation & References |
|---|---|---|
| `code-quality-linting` | Syntax standardization & style compliance | PEP 8 / TypeScript Strict / `verify_code_style.py` |
| `agent-governance-audit` | Audits rules, skill ID drift, and broken links | `auditor.py` / `run_governance_audit.py` |
| `cross-agent-collaboration` | Multi-agent task handoff and ownership locking | Single Writer Invariant & Markdown Handoff Template |
| `codex-antigravity-bridge` | Headless CLI automation & token handshake | `Set-AgyBridgeSettings.ps1`, `Invoke-AgyCrossAgentSmoke.ps1` |
| `jules_coding` | Remote cloud agent delegation safety boundaries | Permission prerequisites & local diff verification |
| `modular-refactoring` | High cohesion, low coupling, and pure domain logic | Typed Contract First & Isolation Tests SOP |
| `huge-component-refactoring` | Splits >250-line files, protects 60Hz hot-paths | State machine separation & zero allocation rules |
| `pr-author-maintainer` | Living PR body sync, no self-asserted mergeability | `manage_pr_author.py` |
| `pr-review-evaluation` | Structured review, native inline comments | `submit_pr_review.py` & Mandatory Test Snippet rule |
| `github-security-audit` | Aggregates CodeQL, Dependabot, Secret Scanning | `collect_security_alerts.py` |
| `portable-release-validation` | Release artifact bundling & runtime smoke testing | Clean environment checklist & port collision fallback |

---

## Contributing

Contributions, issues, and feature requests are welcome! Please check out [CONTRIBUTING.md](CONTRIBUTING.md) for details on pre-commit testing gates and identity tagging guidelines.

---

## License

This project is licensed under the [MIT License](LICENSE).
