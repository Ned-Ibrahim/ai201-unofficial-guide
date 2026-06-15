from query import ask

# 5 eval questions + ground-truth (from planning.md)
EVAL = [
    {"q": "What does USCIS require for post-completion OPT eligibility?",
     "gt": "Maintained F-1 status for one full academic year, employment directly related to major, DSO recommendation entered in SEVIS, file Form I-765 within the window; 12-month OPT cap."},
    {"q": "What form is required for STEM OPT training, and who completes it?",
     "gt": "Form I-983 Training Plan, completed jointly by the student and the employer and submitted to the DSO."},
    {"q": "What are the unemployment day limits on standard OPT versus STEM OPT?",
     "gt": "90 days on standard post-completion OPT; 150 days total with the STEM OPT extension."},
    {"q": "Can I be self-employed on OPT, and does the answer differ for STEM OPT?",
     "gt": "Self-employment is allowed on standard OPT (degree-related, 20+ hrs/wk, proper licenses); on STEM OPT it is barred — a bona fide employer-employee relationship, E-Verify employer, and signed I-983 are required."},
    {"q": "Do I need an EIN to file taxes as a freelancer on OPT?",
     "gt": "No. An EIN is optional for a sole proprietor (SSN/ITIN works); obtaining one does not violate F-1 status. (NOTE: this is tax-law info not in the corpus — expected to be a coverage-gap failure / refusal.)"},
]
for i, item in enumerate(EVAL, 1):
    print("="*80)
    print(f"Q{i}: {item['q']}")
    print(f"\nGROUND TRUTH: {item['gt']}")
    r = ask(item["q"], k=5)
    print(f"\nSYSTEM ANSWER:\n{r['answer']}")
    print("\nRETRIEVED CHUNKS:")
    for j, h in enumerate(r["hits"], 1):
        print(f"  [{j}] dist={h['distance']:.3f} [{h['meta']['phase']}] "
              f"{h['meta']['source_name']}")
        print(f"      {h['text'][:160].strip().replace(chr(10),' ')}")
    print(f"\nSOURCES CITED: {r['sources']}")
    print()
