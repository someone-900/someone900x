import gradio as gr
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from agents.clarification_agent import get_clarifying_questions
from agents.reconstruction_agent import reconstruct_prompt
from agents.response_agent import generate_response

# ── State ──────────────────────────────────────────────────────────────────
current_questions = []
current_original_prompt = ""

def step1_get_questions(user_prompt):
    """Takes vague prompt, returns clarifying questions."""
    global current_questions, current_original_prompt

    if not user_prompt.strip():
        return "Please enter a prompt first.", gr.update(visible=False), gr.update(visible=False)

    current_original_prompt = user_prompt
    raw_questions = get_clarifying_questions(user_prompt)
    current_questions = [
        q.strip() for q in raw_questions.strip().split("\n") if q.strip()
    ]

    questions_display = "\n".join(current_questions)

    return (
        questions_display,
        gr.update(visible=True),   # show answers box
        gr.update(visible=True),   # show submit button
    )

def step2_get_response(user_answers):
    """Takes answers, reconstructs prompt, returns final response."""
    if not user_answers.strip():
        return "Please answer the questions above first.", ""

    reconstructed = reconstruct_prompt(
        current_original_prompt,
        "\n".join(current_questions),
        user_answers
    )

    response = generate_response(reconstructed)

    return reconstructed, response

# ── UI Layout ───────────────────────────────────────────────────────────────
with gr.Blocks(title="someone900x", theme=gr.themes.Soft()) as demo:

    gr.Markdown("""
    # someone900x
    **Type anything. We'll ask the right questions. You get the right answer.**
    """)

    with gr.Row():
        with gr.Column():

            # Step 1
            gr.Markdown("### Step 1 — What do you need help with?")
            user_prompt_input = gr.Textbox(
                label="Your prompt",
                placeholder="e.g. help me write something for college...",
                lines=3
            )
            ask_btn = gr.Button("Generate Clarifying Questions →", variant="primary")

            # Questions output
            questions_output = gr.Textbox(
                label="Clarifying questions",
                lines=5,
                interactive=False
            )

            # Step 2 — hidden until questions appear
            answers_input = gr.Textbox(
                label="Your answers (answer each question, one per line)",
                placeholder="1. Email\n2. My professor\n3. Requesting an extension",
                lines=5,
                visible=False
            )
            submit_btn = gr.Button("Generate Response →", variant="primary", visible=False)

        with gr.Column():
            # Results
            gr.Markdown("### Result")
            reconstructed_output = gr.Textbox(
                label="Reconstructed prompt (what we actually sent)",
                lines=6,
                interactive=False
            )
            response_output = gr.Textbox(
                label="Final response",
                lines=12,
                interactive=False
            )

    # ── Event handlers ───────────────────────────────────────────────────────
    ask_btn.click(
        fn=step1_get_questions,
        inputs=[user_prompt_input],
        outputs=[questions_output, answers_input, submit_btn]
    )

    submit_btn.click(
        fn=step2_get_response,
        inputs=[answers_input],
        outputs=[reconstructed_output, response_output]
    )

if __name__ == "__main__":
    demo.launch()