import json, pathlib
import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS = pathlib.Path("documents/chunks.jsonl")
DB_DIR = "documents/chroma"

chunks = [json.loads(l) for l in open(CHUNKS, encoding="utf-8")]
print(f"loaded {len(chunks)} chunks")

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode([c["text"] for c in chunks],
                          show_progress_bar=True, normalize_embeddings=True)

client = chromadb.PersistentClient(path=DB_DIR)
try:
    client.delete_collection("opt_cpt")
except Exception:
    pass
col = client.create_collection("opt_cpt", metadata={"hnsw:space": "cosine"})

META_KEYS = ["source_type","source_subtype","source_name",
             "source_url","source_date","phase","original_filename"]

col.add(
    ids=[c["id"] for c in chunks],
    embeddings=[e.tolist() for e in embeddings],
    documents=[c["text"] for c in chunks],
    metadatas=[{k: c.get(k, "") for k in META_KEYS} | {"chunk_id": c["id"]}
               for c in chunks],
)
print(f"indexed {col.count()} chunks into {DB_DIR}")
