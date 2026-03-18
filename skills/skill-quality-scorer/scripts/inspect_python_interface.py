from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from inspect_python_interface import main


if __name__ == "__main__":
    raise SystemExit(main())
