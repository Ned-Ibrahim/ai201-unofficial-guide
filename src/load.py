import pdfplumber, pathlib

RAW = pathlib.Path("documents/raw")
OUT = pathlib.Path("documents/raw_text")
OUT.mkdir(parents=True, exist_ok=True)

for f in sorted(RAW.iterdir()):
    if f.suffix == ".pdf":
        with pdfplumber.open(f) as pdf:
            text = "\n\n".join(p.extract_text() or "" for p in pdf.pages)
    elif f.suffix in (".txt", ".html"):
        text = f.read_text(encoding="utf-8", errors="ignore")
    else:
        continue
    (OUT / (f.stem + ".txt")).write_text(text, encoding="utf-8")
    print(f"{f.name:30s} {len(text):>8d} chars")
