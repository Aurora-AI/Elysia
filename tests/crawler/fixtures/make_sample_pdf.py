# tests/crawler/fixtures/make_sample_pdf.py
from pathlib import Path
try:
    from reportlab.pdfgen import canvas  # pip install reportlab
except Exception:
    print("reportlab not installed; skipping pdf creation.")
    raise SystemExit(0)

out = Path(__file__).parent / "sample.pdf"
c = canvas.Canvas(str(out))
c.drawString(100, 750, "Hello Aurora Crawler (PDF).")
c.save()
print(f"Wrote {out}")
