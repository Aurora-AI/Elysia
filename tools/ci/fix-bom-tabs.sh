#!/bin/bash
# Saneamento de workflows YAML - remove BOM, tabs e valida sintaxe

set -e

echo "🔧 Saneando workflows YAML..."

# 1. Remover tabs -> espaços
echo "  → Removendo tabs..."
find .github/workflows -type f -name "*.yml" -print0 | xargs -0 sed -i 's/\t/  /g'

# 2. Remover BOM (Byte Order Mark)
echo "  → Removendo BOM..."
python3 - <<'PY'
import pathlib
for p in pathlib.Path(".github/workflows").glob("*.yml"):
    b = p.read_bytes()
    if b.startswith(b'\xef\xbb\xbf'):
        p.write_bytes(b[len(b'\xef\xbb\xbf'):])
        print("    Removed BOM:", p)
PY

# 3. Validar YAML
echo "  → Validando YAML..."
python3 - <<'PY'
import yaml, glob, sys
errors = 0
for f in glob.glob(".github/workflows/*.yml"):
    try:
        yaml.safe_load(open(f, "rb"))
        print(f"    [OK] {f}")
    except Exception as e:
        print(f"    [ERR] {f} -> {e}")
        errors += 1
if errors > 0:
    sys.exit(1)
PY

echo "✅ Saneamento concluído!"