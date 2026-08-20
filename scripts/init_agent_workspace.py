#!/usr/bin/env python3
"""Scaffold Agent Governance into a target workspace."""

import sys
from pathlib import Path

# Add parent directory to sys.path so agent_cli can be imported
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

from agent_cli.scaffolder import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
