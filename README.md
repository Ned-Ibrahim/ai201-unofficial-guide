# The Unofficial Guide — Project 1

> **F-1 OPT / STEM OPT RAG guide** — official USCIS/DHS policy plus university ISS pages and attorney commentary, with every answer tagged Official vs Unofficial.

Benjamin, saw the PSVIEW post. Spent a year shipping production AI at Ameritas, daily user calls included. Just finished CS, free 6 months, ready for SF. Let's talk?

---

## Domain

International students navigating CPT, OPT, STEM OPT, and related paperwork face dense official policy that doesn't explain real-world timing, common mistakes, or what peers did when their situation didn't match the FAQ. University ISS pages and government sites state the rules but leave gaps on filing workflow, processing times, and edge cases.

This system combines two layers:

1. **Official** — USCIS, DHS/SEVIS, ICE, NAFSA, and university ISS pages for policy and requirements.
2. **Unofficial** — immigration attorney commentary (and eventually student forums) for edge cases official pages omit.

Every answer must identify which layer each claim comes from. Unofficial sources inform practical orientation only; official sources take precedence when they conflict. This guide is informational, not legal or immigration advice.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | USCIS — OPT for F-1 Students | Official (government) | `documents/clean/uscis_opt_f1.txt` · [uscis.gov](https://www.uscis.gov/working-in-the-united-states/students-and-exchange-visitors/optional-practical-training-opt-for-f-1-students) |
| 2 | USCIS — STEM OPT Extension | Official (government) | `documents/clean/uscis_stem_opt.txt` · [uscis.gov](https://www.uscis.gov/working-in-the-united-states/students-and-exchange-visitors/optional-practical-training-extension-for-stem-students-stem-opt) |
| 3 | DHS — International Students & Entrepreneurship | Official (government) | `documents/clean/dhs_entrepreneurship.txt` · [studyinthestates.dhs.gov](https://studyinthestates.dhs.gov/international-students-and-entrepreneurship) |
| 4 | NAFSA — 8 CFR 214.2(f) | Official (government) | `documents/clean/nafsa_8cfr.txt` · [nafsa.org](https://www.nafsa.org/regulatory-information/8cfr2142f) |
| 5 | Form I-765 Instructions (PDF) | Official (government) | `documents/clean/i-765instr.txt` · [uscis.gov](https://www.uscis.gov/sites/default/files/document/forms/i-765instr.pdf) |
| 6 | Form I-983 Instructions (PDF) | Official (government) | `documents/clean/i983_instructions.txt` · [ice.gov](https://www.ice.gov/doclib/sevis/pdf/i983Instructions.pdf) |
| 7 | ICE — OPT Directly Related to Major (PDF) | Official (government) | `documents/clean/opt_directly_related.txt` · [ice.gov](https://www.ice.gov/doclib/sevis/pdf/optDirectlyRelatedGuidance.pdf) |
| 8 | USC OIS — Post-Completion OPT | Official (university ISS) | `documents/clean/usc_postopt.txt` · [ois.usc.edu](https://ois.usc.edu/employment/employment-f1/opt/post-completion-opt/) |
| 9 | BU ISSO — 24-Month STEM OPT Employment Types | Official (university ISS) | `documents/clean/bu_stem_types.txt` · [bu.edu](https://www.bu.edu/isso/employment-internships/student-off-campus-work-and-training/24-month-stem-opt/employment-types/) |
| 10 | RJ Immigration Law — Self-Employment on OPT/STEM OPT | Unofficial (attorney) | `documents/clean/rj_selfemployed.txt` · [rjimmigrationlaw.com](https://rjimmigrationlaw.com/resources/can-i-be-self-employed-on-opt-or-stem-opt/) |

Metadata for all sources is in `documents/sources.csv`.

---

## Chunking Strategy

**Chunk size:** 250 tokens (~1,000 characters) — leaves room for the tokenizer's 2 special tokens within MiniLM's 256-token limit.

**Overlap:** 64 tokens (~25% overlap).

**Why these choices fit your documents:**

The corpus mixes dense USCIS/8 CFR legal text, university advising FAQs, and law-firm articles. Rules are conditional — e.g. "X is allowed provided that A, B, and C." Splitting a rule from its conditions can return misleading partial context, which is especially harmful in immigration guidance. A recursive, structure-aware splitter breaks on headings → paragraphs → sentences → characters. Higher overlap (25% vs the usual 10–15%) carries trailing conditions across chunk boundaries. Each chunk carries full source metadata (`source_type`, `phase`, `source_url`, etc.) from `documents/sources.csv`.

**Preprocessing:** `src/load.py` extracts text from PDFs via `pdfplumber`; `src/clean.py` strips HTML, navigation boilerplate, and collapses excess whitespace into `documents/clean/`.

**Final chunk count:** 362 chunks across 10 documents (`documents/chunks.jsonl`).

---

## Embedding Model

**Model used:** `sentence-transformers/all-MiniLM-L6-v2` (planned; chunking tokenizer already uses this model).

**Production tradeoff reflection:**

If cost were not a constraint, I would weigh: (1) **domain jargon** — CPT, OPT, STEM, I-765, and SEVIS abbreviations may embed poorly in a general-purpose model; a legal or immigration-fine-tuned embedder could improve retrieval on dense 8 CFR text; (2) **context length** — longer-context embedders (e.g. `e5-large`) could use larger chunks and reduce conditional-split risk; (3) **latency** — MiniLM is fast and runs locally; heavier models add seconds per query; (4) **multilingual support** — not critical for this English-only corpus, but would matter if student forum sources include non-English posts. For this project, MiniLM + small chunks + high overlap is the right cost/accuracy tradeoff.

---

## Grounded Generation

**System prompt grounding instruction:**

*(Milestone 5 — in progress.)* The system prompt will require the model to:

1. Label every claim as **Official guidance** vs **Student-reported experience** / **Professional commentary**.
2. Prefer official sources for eligibility, required documents, and policy deadlines.
3. Use unofficial sources only for timing estimates and edge-case workflows — framed as anecdotal, not policy.
4. Flag conflicts: state the official rule first, then note any conflicting anecdote and its source.
5. Refuse to invent — if retrieved context lacks support, say so.
6. Include a disclaimer that responses are informational, not legal or immigration advice.

Retrieved chunks are prefixed before generation, e.g. `[OFFICIAL — USCIS OPT for F-1]` or `[UNOFFICIAL — RJ Immigration Law]`.

**How source attribution is surfaced in the response:**

Each answer will include separate headings for Official / Unofficial layers plus a **Sources** line tagging `[OFFICIAL]` vs `[UNOFFICIAL]` with clickable URLs from chunk metadata.

---

## Evaluation Report

*(Run after Milestone 5 — retrieval + generation are wired up.)*

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What does USCIS require for post-completion OPT eligibility? | Valid F-1, one academic year enrolled, employment related to major, DSO SEVIS recommendation, I-765 within filing window, 12-month OPT cap | | | |
| 2 | What training plan form is required for STEM OPT, and when must it be submitted? | Form I-983; student + employer; submitted to DSO within 60 days of STEM OPT start | | | |
| 3 | When should I apply for post-completion OPT relative to my program end date? | Up to 90 days before program end; no later than 60 days after | | | |
| 4 | What are the unemployment day limits on standard OPT vs STEM OPT? | 90 days standard OPT; 150 days combined (initial + STEM) | | | |
| 5 | Can I be self-employed on OPT, and does the answer differ for STEM OPT? | DHS allows self-employment on standard OPT under conditions; STEM OPT requires bona fide employer-employee relationship; attorney blogs note higher scrutiny | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

*(To complete after eval run.)*

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

**One way the spec helped you during implementation:**

`planning.md` defined the source taxonomy (official vs unofficial), the metadata fields on every chunk, and the 256-token chunk ceiling tied to MiniLM — so ingestion and chunking (`src/load.py`, `src/clean.py`, `src/chunk.py`) could be built against a concrete contract instead of ad hoc splits.

**One way your implementation diverged from the spec, and why:**

The spec planned a nested folder layout (`documents/official/government/`, etc.) and 256-token chunks; the implementation uses a flat `documents/raw` → `raw_text` → `clean` pipeline with metadata in `sources.csv`, and `chunk_size=250` tokens to stay safely under the embedder's 256-token hard limit.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* The Chunking Strategy and Documents table from `planning.md`, plus `requirements.txt`.
- *What it produced:* `src/load.py` (PDF/text ingestion), `src/clean.py` (HTML and nav stripping), and `src/chunk.py` (recursive splitter with `sources.csv` metadata).
- *What I changed or overrode:* Used a flat `documents/` layout with `sources.csv` instead of path-derived metadata; set chunk size to 250 tokens (not 256) to avoid embedder truncation.

**Instance 2**

- *What I gave the AI:* The full Domain, Source Taxonomy, and Evaluation Plan sections from `planning.md`.
- *What it produced:* The initial `planning.md` spec including architecture diagram, retrieval approach, and five eval questions with expected answers.
- *What I changed or overrode:* Trimmed the document list to the 10 sources actually collected so far; deferred student forum sources and UNL ISS pages to a later milestone.

---

## Pipeline (current)

```bash
python src/load.py    # documents/raw → documents/raw_text
python src/clean.py   # documents/raw_text → documents/clean
python src/chunk.py   # documents/clean → documents/chunks.jsonl (362 chunks)
# Next: embed → ChromaDB → Groq generation → Gradio UI
```
