import pathlib, html, re
from bs4 import BeautifulSoup

IN = pathlib.Path("documents/raw_text")
OUT = pathlib.Path("documents/clean")
OUT.mkdir(parents=True, exist_ok=True)

NAV_NOISE = [
    "skip to content", "was this page helpful", "share this page",
    "book a consultation", "related posts", "cookie", "read more",
    "back to top", "print this page", "subscribe", "follow us",
    "©", "all rights reserved", "privacy policy", "terms of use",
]

for f in sorted(IN.iterdir()):
    text = f.read_text(encoding="utf-8", errors="ignore")
    if "<" in text and ">" in text:                       # strip HTML if any
        text = BeautifulSoup(text, "html.parser").get_text(separator="\n")
    text = html.unescape(text)                            # &amp; &nbsp; &#39;
    kept = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        if any(n in s.lower() for n in NAV_NOISE):        # drop boilerplate
            continue
        kept.append(s)
    text = "\n".join(kept)
    text = re.sub(r"\n{3,}", "\n\n", text)                # collapse blank runs
    (OUT / f.name).write_text(text, encoding="utf-8")
    print(f"{f.name:30s} {len(text):>8d} chars cleaned")
