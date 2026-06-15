import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent / "src"))

import gradio as gr
from query import ask

def handle_query(question):
    if not question.strip():
        return "Enter a question.", ""
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"]) or "—"
    return result["answer"], sources

with gr.Blocks(title="Unofficial Guide: OPT/CPT") as demo:
    gr.Markdown("# Unofficial Guide — F-1 OPT/CPT\n"
                "Ask about OPT/CPT eligibility, self-employment, STEM OPT, and "
                "work authorization. Answers come only from official sources.")
    inp = gr.Textbox(label="Your question",
                     placeholder="e.g. Can I freelance on OPT?")
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch()
