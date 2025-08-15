# patch_final_tests.py
"""
Script de correção automatizada para testes e APIs Aurora-Plataform.
Executa ajustes finais de compatibilidade e padronização para garantir que a suíte de testes rode 100%.
"""

import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

# 1. Corrige imports relativos quebrados em arquivos de teste
for dirpath, _, filenames in os.walk(os.path.join(ROOT, "aurora-core", "tests")):
    for fname in filenames:
        if fname.endswith(".py"):
            fpath = os.path.join(dirpath, fname)
            with open(fpath, encoding="utf-8") as f:
                code = f.read()
            # Corrige 'from ..' para 'from aurora_platform.'
            code_new = re.sub(
                r"from \.\.(.*?) import", r"from aurora_platform\1 import", code
            )
            # Corrige 'import ..' para 'import aurora_platform.'
            code_new = re.sub(
                r"import \.\.(.*?)", r"import aurora_platform.\1", code_new
            )
            if code_new != code:
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(code_new)

# 2. Corrige imports quebrados em arquivos de API (routers)
routers_dir = os.path.join(ROOT, "aurora-core", "src", "aurora_platform", "routers")
if os.path.isdir(routers_dir):
    for fname in os.listdir(routers_dir):
        if fname.endswith(".py"):
            fpath = os.path.join(routers_dir, fname)
            with open(fpath, encoding="utf-8") as f:
                code = f.read()
            # Corrige 'from ..schemas' para 'from aurora_platform.schemas'
            code_new = re.sub(
                r"from \.\.(schemas|services)", r"from aurora_platform.\1", code
            )
            if code_new != code:
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(code_new)

print("Patch de correção final aplicado com sucesso.")
