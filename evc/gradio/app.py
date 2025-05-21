import gradio as gr

def greet(name):
    return "Hello " + name + "! (KETI)"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")
    
demo.launch(debug=True, 
            #root_path="/chatbot",
            server_name="0.0.0.0")