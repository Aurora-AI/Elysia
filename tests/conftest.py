"""
Garante que 'aurora-platform/src' e 'aurora-core/src' estejam no sys.path,
independente de onde os testes são executados.
"""
import sys
from pathlib import Path


def _add_path(p: Path):
    s = str(p)
    if s not in sys.path:
        sys.path.insert(0, s)


HERE = Path(__file__).resolve()
for parent in [HERE] + list(HERE.parents):
    ap_src = parent / "aurora-platform" / "src"
    if ap_src.exists():
        _add_path(ap_src)
    ac_src = parent / "aurora-core" / "src"
    if ac_src.exists():
        _add_path(ac_src)
    only_src = parent / "src"
    if only_src.exists():
        _add_path(only_src)
