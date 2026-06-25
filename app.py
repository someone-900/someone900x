import gradio as gr
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend", "agents"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend", "utils"))

from clarification_agent import get_clarifying_questions
from reconstruction_agent import reconstruct_prompt
from response_agent import generate_response

# ── State ─────────────────────────────────────────────────────────────────────
def initialize_state():
    return {"stage": "idle", "original_prompt": "", "questions": ""}

# ── Pipeline ──────────────────────────────────────────────────────────────────
def chat(user_message, history, state):
    if state is None:
        state = initialize_state()
    history = history or []

    if state["stage"] == "idle":
        state["original_prompt"] = user_message
        state["stage"] = "awaiting_answers"

        history.append((user_message, "_(someone900x B1 is thinking...)_"))
        yield history, state

        questions = get_clarifying_questions(user_message)
        state["questions"] = questions

        response = f"""Before I give you the best possible answer, I have a few quick questions:

{questions}

_Answer them however feels natural — you can number your answers or just write them out._"""

        history[-1] = (user_message, response)
        yield history, state

    elif state["stage"] == "awaiting_answers":
        history.append((user_message, "_(Reconstructing your prompt and generating response...)_"))
        yield history, state

        reconstructed = reconstruct_prompt(
            state["original_prompt"],
            state["questions"],
            user_message
        )
        final_response = generate_response(reconstructed)

        full_response = f"""{final_response}

---
_✦ Enhanced by someone900x B1_"""

        history[-1] = (user_message, full_response)
        state = initialize_state()
        yield history, state

    else:
        state = initialize_state()
        yield from chat(user_message, history, state)


def clear_chat():
    return [], initialize_state()


# ── CSS ───────────────────────────────────────────────────────────────────────
css = """
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

* { box-sizing: border-box; }

body, .gradio-container {
    font-family: 'Sora', sans-serif !important;
    background: #0a0a0f !important;
    color: #e8e6f0 !important;
}

.gradio-container {
    max-width: 820px !important;
    margin: 0 auto !important;
    padding: 0 !important;
}

#header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    padding: 32px 32px 0 32px;
}

#header-left h1 {
    font-size: 28px;
    font-weight: 600;
    letter-spacing: -0.5px;
    color: #ffffff;
    margin: 0 0 6px 0;
}

#header-left p {
    font-size: 13px;
    color: #6b6880;
    margin: 0;
    max-width: 420px;
    line-height: 1.6;
}

#how-btn {
    background: none !important;
    border: 1px solid #2a2838 !important;
    border-radius: 10px !important;
    padding: 8px 14px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    color: #6b6880 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    white-space: nowrap;
}

#how-btn:hover {
    border-color: #4a4560 !important;
    color: #a8a4c0 !important;
    background: #12111a !important;
}

#model-badge {
    padding: 16px 32px 12px 32px;
}

#model-badge-inner {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #12111a;
    border: 1px solid #2a2838;
    border-radius: 20px;
    padding: 4px 12px 4px 8px;
    font-size: 12px;
    color: #6b6880;
    font-family: 'JetBrains Mono', monospace;
}

#model-badge-inner::before {
    content: '';
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #4ade80;
    display: inline-block;
    box-shadow: 0 0 6px #4ade8088;
}

/* Chatbot area */
#chatbot {
    background: transparent !important;
    border: none !important;
    padding: 0 32px !important;
}

#chatbot .wrap {
    padding: 0 !important;
    gap: 12px !important;
}

/* User bubble */
#chatbot .user > div, #chatbot [data-testid="user"] {
    background: #1a1828 !important;
    border: 1px solid #2a2838 !important;
    border-radius: 18px 18px 4px 18px !important;
    color: #e8e6f0 !important;
    font-size: 14px !important;
    line-height: 1.65 !important;
    padding: 12px 16px !important;
    max-width: 75% !important;
    margin-left: auto !important;
}

/* Bot bubble */
#chatbot .bot > div, #chatbot [data-testid="bot"] {
    background: #0f0e16 !important;
    border: 1px solid #1e1c2a !important;
    border-radius: 18px 18px 18px 4px !important;
    color: #d4d0e8 !important;
    font-size: 14px !important;
    line-height: 1.75 !important;
    padding: 14px 18px !important;
    max-width: 85% !important;
}

/* Input row */
#input-row {
    padding: 12px 32px 28px 32px;
}

#msg-input textarea {
    background: #12111a !important;
    border: 1px solid #2a2838 !important;
    border-radius: 14px !important;
    color: #e8e6f0 !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 14px !important;
    padding: 14px 16px !important;
    resize: none !important;
    transition: border-color 0.2s ease !important;
}

#msg-input textarea:focus {
    border-color: #4a4560 !important;
    outline: none !important;
    box-shadow: 0 0 0 3px #2a283820 !important;
}

#msg-input textarea::placeholder { color: #3a3850 !important; }
#msg-input label { display: none !important; }

#send-btn {
    background: #e8e6f0 !important;
    border: none !important;
    border-radius: 12px !important;
    color: #0a0a0f !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 13px 22px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}

#send-btn:hover {
    background: #ffffff !important;
    transform: translateY(-1px) !important;
}

#clear-btn {
    background: none !important;
    border: 1px solid #2a2838 !important;
    border-radius: 12px !important;
    color: #4a4560 !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 13px !important;
    padding: 13px 16px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}

#clear-btn:hover {
    border-color: #4a4560 !important;
    color: #6b6880 !important;
}

/* Modal */
#instructions-modal {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(10,10,15,0.85);
    backdrop-filter: blur(8px);
    z-index: 9999;
    align-items: center;
    justify-content: center;
}

#instructions-modal.open { display: flex; }

#modal-box {
    background: #12111a;
    border: 1px solid #2a2838;
    border-radius: 20px;
    padding: 36px;
    max-width: 520px;
    width: 90%;
    position: relative;
}

#modal-box h2 {
    font-size: 20px;
    font-weight: 600;
    color: #ffffff;
    margin: 0 0 4px 0;
}

#modal-box .modal-sub {
    font-size: 12px;
    color: #4a4560;
    margin: 0 0 24px 0;
    font-family: 'JetBrains Mono', monospace;
}

#modal-box .step {
    display: flex;
    gap: 14px;
    margin-bottom: 18px;
    align-items: flex-start;
}

#modal-box .step-num {
    width: 26px;
    height: 26px;
    border-radius: 7px;
    background: #1a1828;
    border: 1px solid #2a2838;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 600;
    color: #6b6880;
    flex-shrink: 0;
    font-family: 'JetBrains Mono', monospace;
}

#modal-box .step-text {
    font-size: 13px;
    color: #a8a4c0;
    line-height: 1.65;
    padding-top: 3px;
}

#modal-box .step-text strong { color: #e8e6f0; font-weight: 500; }

#modal-close {
    position: absolute;
    top: 16px;
    right: 16px;
    background: none;
    border: 1px solid #2a2838;
    border-radius: 7px;
    color: #4a4560;
    font-size: 14px;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
    line-height: 1;
}

#modal-close:hover { border-color: #4a4560; color: #6b6880; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #2a2838; border-radius: 2px; }
"""

js_modal = """
function toggleModal() {
    const m = document.getElementById('instructions-modal');
    m.classList.toggle('open');
}
function closeModal() {
    document.getElementById('instructions-modal').classList.remove('open');
}
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeModal();
});
"""

# ── UI ────────────────────────────────────────────────────────────────────────
with gr.Blocks(title="EazyAI") as demo:

    state = gr.State(initialize_state)

    # Modal
    gr.HTML("""
    <div id="instructions-modal">
      <div id="modal-box">
        <button id="modal-close" onclick="closeModal()">✕</button>
        <h2>How to use EazyAI</h2>
        <p class="modal-sub">someone900x B1 · Beta</p>
        <div class="step">
          <div class="step-num">01</div>
          <div class="step-text"><strong>Type anything vaguely.</strong> Don't worry about writing a perfect prompt. Just say what you need — "help me write an email" is enough.</div>
        </div>
        <div class="step">
          <div class="step-num">02</div>
          <div class="step-text"><strong>Answer a few quick questions.</strong> someone900x B1 asks 3 short clarifying questions to understand exactly what you need.</div>
        </div>
        <div class="step">
          <div class="step-num">03</div>
          <div class="step-text"><strong>Get a precise response.</strong> The model reconstructs your intent into a detailed prompt and generates a response that actually matches what you meant.</div>
        </div>
        <div class="step">
          <div class="step-num">04</div>
          <div class="step-text"><strong>Start fresh anytime.</strong> Hit Clear to reset and begin a new conversation.</div>
        </div>
      </div>
    </div>
    """)

    # Header
    gr.HTML("""
    <div id="header">
      <div id="header-left">
        <h1>EazyAI</h1>
        <p>You don't need to know how to prompt. Just tell us what you need — we'll figure out the rest.</p>
      </div>
      <button id="how-btn" onclick="toggleModal()">? How it works</button>
    </div>
    """)

    # Model badge
    gr.HTML("""
    <div id="model-badge">
      <div id="model-badge-inner">someone900x B1</div>
    </div>
    """)

    # Chat
    chatbot = gr.Chatbot(
    elem_id="chatbot",
    height=480,
    show_label=False,
    avatar_images=(None, None),
)

    # Input
    with gr.Row(elem_id="input-row"):
        msg = gr.Textbox(
            elem_id="msg-input",
            placeholder="Type your prompt here...",
            lines=1,
            max_lines=6,
            scale=10,
            show_label=False,
        )
        send_btn = gr.Button("Send", elem_id="send-btn", scale=1)
        clear_btn = gr.Button("Clear", elem_id="clear-btn", scale=1)

    gr.HTML(f"<script>{js_modal}</script>")

    # Events
    def submit(message, history, state):
        if not message.strip():
            yield history, state, ""
            return
        for h, s in chat(message, history, state):
            yield h, s, ""

    send_btn.click(
        fn=submit,
        inputs=[msg, chatbot, state],
        outputs=[chatbot, state, msg],
    )
    msg.submit(
        fn=submit,
        inputs=[msg, chatbot, state],
        outputs=[chatbot, state, msg],
    )
    clear_btn.click(
        fn=clear_chat,
        outputs=[chatbot, state],
    )

if __name__ == "__main__":
    demo.launch(
        css=css,
        theme=gr.themes.Base(primary_hue="slate", neutral_hue="slate"),
    )