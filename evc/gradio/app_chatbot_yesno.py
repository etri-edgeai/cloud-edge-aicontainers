import random
import gradio as gr

def random_response(message, history):
    return random.choice(["Yes", "No"])

demo = gr.ChatInterface(random_response)

demo.launch(share=False,
            debug=True,
            root_path="/chatbot",
            server_name="0.0.0.0"
)