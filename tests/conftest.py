import os
import sys

# Ensure aurora-core/src is on sys.path for imports
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)
SRC = os.path.join(REPO, "aurora-core", "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)
