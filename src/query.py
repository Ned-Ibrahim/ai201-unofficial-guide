import os
from dotenv import load_dotenv
from groq import Groq
from retrieve import retrieve   # same dir

load_dotenv()
_client = Groq(api_key=os.environ["GROQ_API_KEY"])
MODEL = "llama-3.3-70b-versatile"

SYSTEM = (
    "You are an assistant for international students on F-1 OPT/CPT. "
    "Answer ONLY using the numbered context passages provided. "
    "Do NOT use any outside knowledge. "
    "If the context does not contain enough information to answer, reply EXACTLY: "
    "\"I don't have enough information on that.\" "
    "Cite the passages you used by their [n] number inline."
)

def ask(question, k=5):
    hits = retrieve(question, k=k)
    # build numbered context block
    blocks = []
    for i, h in enumerate(hits, 1):
        blocks.append(f"[{i}] (source: {h['meta']['source_name']})\n{h['text']}")
    context = "\n\n".join(blocks)

    user = f"Context passages:\n\n{context}\n\nQuestion: {question}"
    resp = _client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[{"role": "system", "content": SYSTEM},
                  {"role": "user", "content": user}],
    )
    answer = resp.choices[0].message.content.strip()

    # programmatic source attribution — from metadata, not the LLM.
    # suppress sources when the model declined to answer.
    REFUSAL = "I don't have enough information on that."
    if REFUSAL in answer:
        return {"answer": answer, "sources": [], "hits": hits}
    seen, sources = set(), []
    for h in hits:
        name = h["meta"]["source_name"]
        url = h["meta"].get("source_url", "")
        if name not in seen:
            seen.add(name)
            sources.append(f"{name} — {url}" if url else name)
    return {"answer": answer, "sources": sources, "hits": hits}

if __name__ == "__main__":
    for q in ["Can I be self-employed on standard OPT?",
              "Can I run my own startup on the STEM OPT extension?",
              "What is the best pizza place near campus?"]:   # out-of-scope test
        print("#"*70)
        print("Q:", q)
        r = ask(q)
        print("\nANSWER:\n", r["answer"])
        print("\nSOURCES:")
        for s in r["sources"]:
            print("  •", s)
        print()
