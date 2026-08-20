# Universal Agent Governance Framework

[![CI](https://github.com/eddie772tw/agent-governance-framework/actions/workflows/agent-governance-ci.yml/badge.svg)](https://github.com/eddie772tw/agent-governance-framework/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)

A highly disciplined, neutral, and self-auditing universal Agent Governance Framework designed for multi-agent AI development (Google Antigravity, OpenAI Codex, Google Jules, and human teams).

---

## Key Principles & Features

1. **Skill Discovery Gate**:
   - Single Canonical Skill Registry (`.agents/skills/README.md`).
   - Agents must inspect trigger conditions and fully read `SKILL.md` before executing tasks.
2. **Multi-Agent Collaboration & Identity Tagging (`{Code} as {Agent}`)**:
   - Strict Single Writer Ownership locking and standard Handoff state machine.
   - Distinct identity markings (e.g. `Gemini as Antigravity`, `Luna as Codex`) when sharing GitHub accounts.
3. **PR Role Separation & Invariants**:
   - **PR Author/Maintainer**: Living PR Body synchronization, strict pre-commit test gate, **no self-asserted mergeability ("ready to merge / LGTM")**.
   - **PR Reviewer**: Standard review formatting, native GitHub Inline Comments / Suggestions, **mandatory test snippets for CI-uncovered blocking findings**.
4. **Anti-Hallucination Package Verification Protocol**:
   - Strict 3-step verification against official registries (npm, PyPI, crates.io, Go) and license compatibility.
5. **Living Knowledge Base (Journal.md)**:
   - Structured learnings (`proposed` -> `adopted` -> `superseded`).
   - Lessons recurring 2+ times automatically escalate to `AGENTS.md`.

---

## Quick Start

### 1. Run Governance Audit
```bash
python scripts/run_governance_audit.py
```

### 2. Run Test Suite
```bash
pytest tests/ -v
```

### 3. Scaffold into Target Workspace
```bash
# Full preset (All 10 core skills)
python scripts/init_agent_workspace.py --target /path/to/project --preset full

# Python-optimized preset
python scripts/init_agent_workspace.py --target /path/to/project --preset python
```

---

## License

This project is licensed under the [MIT License](LICENSE).
