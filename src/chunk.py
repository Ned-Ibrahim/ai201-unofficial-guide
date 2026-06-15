import pathlib, csv, json
from transformers import AutoTokenizer
from langchain_text_splitters import RecursiveCharacterTextSplitter

tok = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# load metadata manifest keyed by file stem
meta = {}
with open("documents/sources.csv", newline="", encoding="utf-8") as fh:
    for row in csv.DictReader(fh):
        meta[pathlib.Path(row["original_filename"]).stem] = row

splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
    tok, chunk_size=250, chunk_overlap=64,
    separators=["\n\n", "\n", ". ", " ", ""],
)

chunks = []
for f in sorted(pathlib.Path("documents/clean").iterdir()):
    text = f.read_text(encoding="utf-8")
    md = meta.get(f.stem, {"original_filename": f.name})
    for i, c in enumerate(splitter.split_text(text)):
        c = c.strip()
        if not c:                       # drop empties
            continue
        chunks.append({"id": f"{f.stem}_{i}", "text": c, **md})

out = pathlib.Path("documents/chunks.jsonl")
out.write_text("\n".join(json.dumps(c, ensure_ascii=False) for c in chunks),
               encoding="utf-8")
print(f"TOTAL CHUNKS: {len(chunks)}")
