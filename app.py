import gradio as gr
from agent_app import ask_agent
import spaces

@spaces.GPU
def respond(question):
    if not question.strip():
        return "Please enter a question."

    try:
        return ask_agent(question)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Agent error: {type(e).__name__}: {e}"


demo = gr.Interface(
    fn=respond,
    inputs=gr.Textbox(
        label="Customer Question",
        placeholder="Where is my order 1001?"
    ),
    outputs=gr.Textbox(label="Agent Response"),
    title="Customer Support Agent",
    description="Ask about orders, returns, refunds and shipping."
)

demo.launch(ssr_mode=False)