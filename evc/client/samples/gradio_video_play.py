import gradio as gr

def video_identity(video):
    return video

demo = gr.Interface(video_identity, 
                    gr.Video(), 
                    "playable_video", 
                    )

demo.queue().launch(share=False,
                    debug=False,
                    server_name="0.0.0.0",
                    server_port=8001
                    )