import gradio as gr
import torch
from transformers import pipeline, AutoModelForCausalLM

MODEL = "beomi/KoAlpaca-Polyglot-12.8B"
model = AutoModelForCausalLM.from_pretrained(
    MODEL,
    device_map="auto",
    load_in_8bit=True,
    revision="8bit",
    # max_memory=f'{int(torch.cuda.mem_get_info()[0]/1024**3)-2}GB'
)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=MODEL,
    # device=2,
)


def answer(state, state_chatbot, text):
    messages = state + [{"role": "질문", "content": text}]

    conversation_history = "\n".join(
        [f"### {msg['role']}:\n{msg['content']}" for msg in messages]
    )

    ans = pipe(
        conversation_history + "\n\n### 답변:",
        do_sample=True,
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.9,
        return_full_text=False,
        eos_token_id=2,
    )

    msg = ans[0]["generated_text"]

    if "###" in msg:
        msg = msg.split("###")[0]

    new_state = [{"role": "이전 질문", "content": text}, {"role": "이전 답변", "content": msg}]

    state = state + new_state
    state_chatbot = state_chatbot + [(text, msg)]

    print(state)
    print(state_chatbot)

    return state, state_chatbot, state_chatbot


with gr.Blocks(css="#chatbot .overflow-y-auto{height:750px}") as demo:
    state = gr.State(
        [
            {
                "role": "인사",
                "content": "안녕하세요. 한국전자전을 위해 배포된 LLM 서비스입니다.",
            },
            {
                "role": "맥락",
                "content": "KoAlpaca(코알파카)는 EleutherAI에서 개발한 Polyglot-ko 라는 한국어 모델을 기반으로, 자연어 처리 연구자 Beomi가 개발한 모델입니다.",
            },
            {
                "role": "맥락",
                "content": "ChatKoAlpaca(챗코알파카)는 KoAlpaca를 채팅형으로 만든 것입니다.",
            },
            {"role": "명령어", "content": "친절한 AI 챗봇인 ChatKoAlpaca 로서 답변을 합니다."},
            {
                "role": "명령어",
                "content": "인사에는 짧고 간단한 친절한 인사로 답하고, 아래 대화에 간단하고 짧게 답해주세요.",
            },
        ]
    )
    state_chatbot = gr.State([])

    with gr.Row():
        gr.HTML(
            """<div style="text-align: center; max-width: 500px; margin: 0 auto;">
            <div>
                <h1> EVC를 통한 LLM 모델의 배포 및 실행 </h1>
                <!--
                <h1>ChatKoAlpaca 12.8B (v1.1b-chat-8bit)</h1>
                -->
                
            </div>
            <div>
                KETI 추론 서비스 서버 p01 (GPU : RTX 3090 (24GB), Model : 8bit quantized LLM)
            </div>
        </div>"""
        )

    with gr.Row():
        chatbot = gr.Chatbot(elem_id="chatbot")

    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Send a message...").style(
            container=False
        )

    txt.submit(answer, [state, state_chatbot, txt], [state, state_chatbot, chatbot])
    txt.submit(lambda: "", None, txt)

demo.launch(debug=True, 
            root_path="/chatbot",
            server_name="0.0.0.0")