from pathlib import Path
import os
import sys
import pathlib
import pytest

# 1) Força TESTING e um DATABASE_URL isolado (SQLite em memória)
os.environ.setdefault("TESTING", "1")
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")

# 2) Force imports to use the repository root so `import aurora_platform` resolves
REPO_ROOT = str(pathlib.Path(__file__).resolve().parents[1])
# Put REPO_ROOT at position 0 to override system/site packages and sibling folders
if sys.path[0] != REPO_ROOT:
    # Remove any existing occurrences
    sys.path = [p for p in sys.path if p != REPO_ROOT]
    sys.path.insert(0, REPO_ROOT)

# If there are sibling development folders like 'aurora-core/src' on sys.path, remove them
sys.path = [p for p in sys.path if 'aurora-core' not in (p or '')]

# Explicitly load the local `aurora_platform` package from REPO_ROOT/aurora_platform
try:
    import importlib.util
    pkg_path = pathlib.Path(REPO_ROOT) / "aurora_platform" / "__init__.py"
    if pkg_path.exists():
        spec = importlib.util.spec_from_file_location(
            "aurora_platform", str(pkg_path))
        module = importlib.util.module_from_spec(spec)
        # Register before executing to avoid recursive imports hitting a different package
        sys.modules["aurora_platform"] = module
        spec.loader.exec_module(module)
        # Ensure submodule imports search the local package folder
        module.__path__ = [str(pathlib.Path(REPO_ROOT) / "aurora_platform")]
except Exception:
    # best-effort: if this fails, continue and let normal import resolution happen
    pass

# 3) Variáveis que alguns módulos exigem (evita falhas na coleta)
os.environ.setdefault("KAFKA_BOOTSTRAP", "localhost:9092")
os.environ.setdefault("KAFKA_TOPIC_PILARES", "pilares.upsert")
os.environ.setdefault("KAFKA_GROUP_PILARES", "consumer-pilares-v1")
os.environ.setdefault("SKIP_NEO4J", "true")


@pytest.fixture(scope="session", autouse=True)
def _db_bootstrap():
    # Cria o schema uma vez para todos os testes
    from aurora_platform.core.db_legacy import Base, get_engine

    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    yield
    # Opcional: limpar ao final
    try:
        Base.metadata.drop_all(bind=engine)
    except Exception:
        pass


"""
Garante que 'aurora-platform/src' e 'aurora-core/src' estejam no sys.path,
independente de onde os testes são executados.
"""


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
