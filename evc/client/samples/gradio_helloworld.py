import gradio as gr

def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)

demo = gr.Interface(
    fn=greet,
    inputs=["text", "slider"],
    outputs=["text"],
)

demo.queue().launch(share=False,
                    debug=False,
                    server_name="0.0.0.0",
                    server_port=8001 )

'''
demo.queue().launch(share=False,
                        debug=False,
                        server_name="0.0.0.0",
                        ssl_certfile="cert.pem",
                        ssl_keyfile="key.pem")
'''
