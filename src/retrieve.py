import chromadb
from sentence_transformers import SentenceTransformer

DB_DIR = "documents/chroma"
_model = SentenceTransformer("all-MiniLM-L6-v2")
_col = chromadb.PersistentClient(path=DB_DIR).get_collection("opt_cpt")

def retrieve(query, k=5):
    emb = _model.encode([query], normalize_embeddings=True)[0].tolist()
    res = _col.query(query_embeddings=[emb], n_results=k)
    out = []
    for doc, meta, dist in zip(res["documents"][0],
                               res["metadatas"][0],
                               res["distances"][0]):
        out.append({"text": doc, "meta": meta, "distance": dist})
    return out

if __name__ == "__main__":
    queries = [
        "Can I be self-employed or run my own business on standard OPT?",
        "Can I work for my own startup on the STEM OPT extension?",
        "How many days of unemployment am I allowed on STEM OPT?",
    ]
    for q in queries:
        print("#"*70)
        print("QUERY:", q)
        for r in retrieve(q, k=5):
            print(f"\n  dist={r['distance']:.3f}  [{r['meta']['phase']}]  {r['meta']['source_name']}")
            print("   ", r["text"][:280].replace("\n", " "))
        print()
