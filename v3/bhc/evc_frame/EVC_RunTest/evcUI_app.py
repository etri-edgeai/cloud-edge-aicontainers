import gradio as gr
import sys
import argparse
import os
import runEVCgradio as evc


parser = argparse.ArgumentParser()
parser.add_argument(
    "--server_name",
    type=str,
    default="0.0.0.0"
)
parser.add_argument(
    "--server_port",
    type=int,
    default=7989
)
args=parser.parse_args()

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def test(url, account, group, node, ip, port, owner, model_name, task, version, mode, app, server_port):
    default_set, default_cfg, modelfile, dockerfile = evc.get_myprj(url, account)

    for run in default_cfg:
        sequence = run['activation']

        if sequence == 'register':
            builders = evc.device_control.host_config(default_set, group, node, ip, port, owner)
        
        elif sequence == 'build':
            # if str2bool(clean_db):
            #     print()
            #     print()
            #     evc.clean_db()
            evc.clean_db(model_name, version)
            evc.model_control.build(
                builders, owner, model_name, task, version, modelfile, dockerfile
            )

        elif sequence == 'download':
            evc.model_control.download(
                group, owner, model_name, task, version, modelfile, dockerfile,
                server_port
            )

        elif sequence == 'run':
            out = evc.model_control.run(
                group, owner, model_name, task, version, modelfile, dockerfile,
                mode, app, server_port
            )

    return out


with gr.Blocks() as demo:
    '''
    추가된 부분 (시작)
    '''
    with gr.Row():

        with gr.Column():
            markdown = gr.Markdown("<strong> This is a Face Detection Service. </strong>")
            sample1 = gr.Video(value="./sample_imgs/face_sample.mp4", autoplay=True)  
            face_btn = gr.Button("Deploy")

        with gr.Column():
            markdown = gr.Markdown("<strong> This is a Fashion Detection Service. </strong>")
            sample2 = gr.Video(value="./sample_imgs/fashion_sample.mp4", autoplay=True)  
            fashion_btn = gr.Button("Deploy")

    with gr.Row():

        with gr.Column():
            markdown = gr.Markdown("<strong> This is a HardHat Detection Service. </strong>")
            sample3 = gr.Video(value="./sample_imgs/hardhat_sample.mp4", autoplay=True)  
            hardhat_btn = gr.Button("Deploy")

        with gr.Column():
            markdown = gr.Markdown("<strong> This is a Wind Mills Detection Service. </strong>")
            sample4 = gr.Video(value="./sample_imgs/windmills_sample.mp4", autoplay=True)  
            windmill_btn = gr.Button("Deploy")

    '''
    추가된 부분 (끝)
    # 밑에 Accordion도 추가됨. (열고 닫기 기능)
    '''

    with gr.Accordion("EVC Deployment System", open=False):
        title1 = gr.Markdown(
                """
                # <center> EVC Deployment System </center>
                """
            )

        with gr.Row(): 

            with gr.Column():

                with gr.Row():
                    account = gr.Textbox(label="Github Account", scale=0, value="hibobo98")
                    url = gr.Textbox(label="Project URL")
                
                with gr.Row():
                    model_name = gr.Textbox(label="Model Name", value="esp-test")
                    version = gr.Textbox(label="Model Version", value="0.6")
                    task = gr.Textbox(label="Model Task", value="detection")
                    mode = gr.Textbox(label="Activation Mode", value="flask")
                    server_port = gr.Textbox(label="Model Application Port", value=7999)

        with gr.Row():
            title2 = gr.Markdown(
                """
                ## <center> Target Node Information </center>
                """
            )
            btn2 = gr.Button("Start Deployment", scale=0)

        with gr.Row():
            with gr.Column(scale=0, min_width=170):
                group = gr.Textbox(label="Group Name", value="keti_test_nuc")
                owner = gr.Textbox(label="Admin", value="keti")

            with gr.Row():
                node = gr.Textbox(label="Node Name", value="n02")
                ip = gr.Textbox(label="IP Address", value="evc.re.kr")
                port = gr.Textbox(label="Port Number", value=33322)
                app = gr.Textbox(label="Model App URL", value="192.168.0.5:7999")


    output = gr.Textbox(label="Result")
    btn2.click(
        test,
        [url, account, group, node, ip, port, owner, model_name, task, version, mode, app, server_port],
        output
    )

    '''
    deploy_btn을 click하면 
    "EVC Deployment System"의 url(gr.Textbox)에 지정된 깃허브 주소가 들어가도록 하는 부분입니다.
    혹시 필요하시면 참고하세요 !!

    * url = gr.Textbox(label="Project URL", value="https://github.com/ethicsense/esp-python.git") 의 value부분 지우고 사용하시면 됩니다!
    '''
    face_url = gr.Text(visible=False, value="https://github.com/hibobo98/Face.git")
    face_model_name = gr.Text(visible=False, value="face-test")
    face_version = gr.Text(visible=False, value="0.1")
    face_task = gr.Text(visible=False, value="detection")
    face_mode = gr.Text(visible=False, value="gradio")
    face_port = gr.Text(visible=False, value=8777)
    face_app = gr.Text(visible=False, value="192.168.0.5:8777")

    fashion_url = gr.Text(visible=False, value="https://github.com/hibobo98/Fashion.git")
    fashion_model_name = gr.Text(visible=False, value="fashion-test")
    fashion_version = gr.Text(visible=False, value="0.1")
    fashion_task = gr.Text(visible=False, value="detection")
    fashion_mode = gr.Text(visible=False, value="gradio")
    fashion_port = gr.Text(visible=False, value=8779)
    fashion_app = gr.Text(visible=False, value="192.168.0.5:8779")

    hardhat_url = gr.Text(visible=False, value="https://github.com/hibobo98/Hardhat.git")
    hardhat_model_name = gr.Text(visible=False, value="hardhat-test")
    hardhat_version = gr.Text(visible=False, value="0.2")
    hardhat_task = gr.Text(visible=False, value="detection")
    hardhat_mode = gr.Text(visible=False, value="gradio")
    hardhat_port = gr.Text(visible=False, value=8778)
    hardhat_app = gr.Text(visible=False, value="192.168.0.5:8778")

    windmill_url = gr.Text(visible=False, value="https://github.com/hibobo98/Windmill.git")
    windmill_model_name = gr.Text(visible=False, value="windmill")
    windmill_version = gr.Text(visible=False, value="0.1")
    windmill_task = gr.Text(visible=False, value="detection")
    windmill_mode = gr.Text(visible=False, value="gradio")
    windmill_port = gr.Text(visible=False, value=8776)
    windmill_app = gr.Text(visible=False, value="192.168.0.5:8776")

    def same(a, b, c, d, e, f, g):
        return a, b, c, d, e, f, g
    
    face_btn.click(
        fn=same,
        inputs=[
            face_url,
            face_model_name,
            face_version,
            face_task,
            face_mode,
            face_port,
            face_app
        ],
        outputs=[
            url,
            model_name,
            version,
            task,
            mode,
            server_port,
            app
        ]
    )

    fashion_btn.click(
        fn=same,
        inputs=[
            fashion_url,
            fashion_model_name,
            fashion_version,
            fashion_task,
            fashion_mode,
            fashion_port,
            fashion_app
        ],
        outputs=[
            url,
            model_name,
            version,
            task,
            mode,
            server_port,
            app
        ]
    )

    hardhat_btn.click(
        fn=same,
        inputs=[
            hardhat_url,
            hardhat_model_name,
            hardhat_version,
            hardhat_task,
            hardhat_mode,
            hardhat_port,
            hardhat_app
        ],
        outputs=[
            url,
            model_name,
            version,
            task,
            mode,
            server_port,
            app
        ]
    )

    windmill_btn.click(
        fn=same,
        inputs=[
            windmill_url,
            windmill_model_name,
            windmill_version,
            windmill_task,
            windmill_mode,
            windmill_port,
            windmill_app
        ],
        outputs=[
            url,
            model_name,
            version,
            task,
            mode,
            server_port,
            app
        ]
    )



demo.queue().launch(
    server_name=args.server_name,
    server_port=args.server_port,
    debug=True
)