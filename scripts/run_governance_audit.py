#!/usr/bin/env python3
"""Run Agent Governance Audit for current repository."""

import sys
from pathlib import Path

# Add parent directory to sys.path so agent_cli can be imported
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

from agent_cli.auditor import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
