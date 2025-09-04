import collections
import json
import pathlib
import sys

path = pathlib.Path("artifacts/pyright-report")
if not path.exists():
    print("Nenhum diretório artifacts/pyright-report encontrado")
    sys.exit(1)

candidates = list(path.glob("*.json"))
if not candidates:
    print("Nenhum JSON encontrado em artifacts/pyright-report")
    sys.exit(1)

report_path = candidates[0]
print(f"Using report: {report_path}")

data = json.loads(report_path.read_text(encoding="utf-8"))

diags = data.get("diagnostics", [])
by_rule = collections.Counter()
by_file = collections.Counter()

for d in diags:
    rule = d.get("rule") or d.get("ruleId") or "<no-rule>"
    sev = d.get("severity") or "unknown"
    by_rule[(rule, sev)] += 1
    by_file[d.get("file") or "<unknown>"] += 1

print("\n# Pyright Report Summary\n")
print("## Top 10 by rule")
for (rule, sev), cnt in by_rule.most_common(10):
    print(f"{cnt:4d}  {sev:<7}  {rule}")

print("\n## Top 10 files")
for file, cnt in by_file.most_common(10):
    print(f"{cnt:4d}  {file}")

print("\n## Sample (first 20)")
for d in diags[:20]:
    file = d.get("file")
    message = (d.get("message", "") or "").strip().replace("\n", " ")
    rule = d.get("rule") or d.get("ruleId")
    sev = d.get("severity")
    rng = d.get("range") or {}
    start = rng.get("start") or {}
    line = start.get("line", "?")
    print(
        f"- [{sev}] {rule} @ {file}:{line} — {message[:240]}{'...' if len(message)>240 else ''}")
