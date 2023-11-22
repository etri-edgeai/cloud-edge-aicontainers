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


def evc_group(url, account, node_list, owner):

    global default_cfg, modelfile, dockerfile

    default_set, default_cfg, modelfile, dockerfile = evc.get_myprj(url, account)

    builders = evc.device_control.builder_config(default_set)

    for node in node_list:
        evc.device_control.node_config(node[0], node[1], node[2], node[3], owner)

    return builders


def evc_deploy(url, account, builders, group, owner, model_name, task, version, mode, server_port, sv_ip=None):

    default_set, default_cfg, modelfile, dockerfile = evc.get_myprj(url, account)

    for run in default_cfg:
        sequence = run['activation']

        print()
        print(sequence)
        print()
        
        if sequence == 'build':
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

        # elif sequence == 'run':

        #     if mode == 'flower' or 'flwrsim':
        #         evc.model_control.run(
        #             group, owner, model_name, task, version, modelfile, dockerfile,
        #             mode, server_port, sv_ip
        #         )

        #     else:
        #         evc.model_control.run(
        #             group, owner, model_name, task, version, modelfile, dockerfile,
        #             mode, server_port
        #         )

def evc_run(url, account, builders, group, owner, model_name, task, version, mode, server_port, sv_ip=None,
            num_clients=None, num_rounds=None, tb_port=None):

    default_set, default_cfg, modelfile, dockerfile = evc.get_myprj(url, account)

    if mode == 'flower' or 'flwrsim':
        evc.model_control.run(
            group, owner, model_name, task, version, modelfile, dockerfile,
            mode, server_port, sv_ip, num_clients, num_rounds, tb_port
        )

    else:
        evc.model_control.run(
            group, owner, model_name, task, version, modelfile, dockerfile,
            mode, server_port
        )

def read_logs():
        with open("/home/keti/ethicsense/flwr_logs/fl_log.txt", "r") as f:
            return f.read()


with gr.Blocks() as demo:
    '''
    추가된 부분 (시작)
    '''
    with gr.Row():

        with gr.Column():
            markdown = gr.Markdown("# <strong> Face Detection Service </strong>")
            sample1 = gr.Video(value="./sample_imgs/face_sample.mp4", autoplay=True)  
            face_btn = gr.Button("Deploy")

        with gr.Column():
            markdown = gr.Markdown("# <strong> Fashion Detection Service </strong>")
            sample2 = gr.Video(value="./sample_imgs/fashion_sample.mp4", autoplay=True)  
            fashion_btn = gr.Button("Deploy")

    with gr.Row():

        with gr.Column():
            markdown = gr.Markdown("# <strong> HardHat Detection Service </strong>")
            sample3 = gr.Video(value="./sample_imgs/hardhat_sample.mp4", autoplay=True)  
            hardhat_btn = gr.Button("Deploy")

        with gr.Column():
            markdown = gr.Markdown("# <strong> Wind Mills Detection Service </strong>")
            sample4 = gr.Video(value="./sample_imgs/windmills_sample.mp4", autoplay=True)  
            windmill_btn = gr.Button("Deploy")

    '''
    추가된 부분 (끝)
    # 밑에 Accordion도 추가됨. (열고 닫기 기능)
    '''

    with gr.Accordion("EVC Deployment System", open=True):
        title1 = gr.Markdown(
                """
                # <center> EVC Deployment System </center>
                """
            )

        with gr.Row(): 

            with gr.Column():

                with gr.Row():
                    account = gr.Textbox(label="Github Account", scale=0, value="ethicsense")
                    url = gr.Textbox(label="Project URL")
                
                with gr.Row():
                    model_name = gr.Textbox(label="Model Name", value="fl-test")
                    version = gr.Textbox(label="Model Version", value="0.1")
                    task = gr.Textbox(label="Model Task", value="fed_learn")
                    mode = gr.Textbox(label="Activation Mode", value="flower")
                    server_port = gr.Textbox(label="Model Application Port", value=8083)

        with gr.Row():
            db_btn = gr.Button("Clean DB", scale=0)
            title2 = gr.Markdown(
                """
                ## <center> Target Node Information </center>
                """
            )

        with gr.Row():
            with gr.Column(scale=0, min_width=170):
                group = gr.Textbox(label="Group Name", value="fl_test")
                owner = gr.Textbox(label="Admin", value="keti")
                target = gr.Textbox(label="Target", placeholder='"user" if all')

            with gr.Column():

                with gr.Row():
                    node = gr.Textbox(label="Node Name", value="", interactive=True)
                    ip = gr.Textbox(label="IP Address", value="", interactive=True)
                    port = gr.Textbox(label="Port Number", value=None, interactive=True)

                    with gr.Row():
                        add_btn = gr.Button("add node", scale=0)
                        reset_btn = gr.Button("Reset list", scale=0)

                output_box = gr.Textbox(label="Nodes List")

                markdown = gr.Markdown("## <strong> Federated Learning Settings </strong>")
                with gr.Row():
                    sv_ip = gr.Textbox(label="Server Node IP", value="192.168.1.7")
                    num_clients = gr.Textbox(label="Number of Clients")
                    num_rounds = gr.Textbox(label="Number of Rounds")
                    tb_port = gr.Textbox(label="Tensorboard Service Port")

        with gr.Row():
            group_btn = gr.Button("Hosts Configuration")
            deploy_btn = gr.Button("Start Deployment")
            run_btn = gr.Button("Start App")
        
        markdown = gr.Markdown("# <strong> Show Result Output </strong>")
        run_logs = gr.Textbox(label="output")


    builders = gr.State(["p02"])

    node_list = []
    node_list_var = gr.State([])

    def add_node(group, node, ip, port):

        n = [group, node, ip, port]
        node_list.append(n)

        return {
            node_list_var: node_list,
            output_box: '\n'.join(str(n) for n in node_list)
        }
    
    def reset_node_list():

        global node_list

        node_list = []

        return {
            node_list_var: node_list,
            output_box: '\n'.join(str(n) for n in node_list)
        }
    
    def reset_node_db(url, account, group, node, ip, port, owner):

        global default_cfg, modelfile, dockerfile

        default_set, default_cfg, modelfile, dockerfile = evc.get_myprj(url, account)

        evc.device_control.node_delete(group, node, ip, port, owner)
    
    db_btn.click(
        reset_node_db,
        [url, account, group, node, ip, port, owner]
    )
    add_btn.click(
        add_node,
        [group, node, ip, port],
        [node_list_var, output_box]
    )
    reset_btn.click(
        fn=reset_node_list,
        outputs=[node_list_var, output_box]
    )
    group_btn.click(
        fn=evc_group,
        inputs=[url, account, node_list_var, owner],
        outputs=builders,
        show_progress='full'
    )
    deploy_btn.click(
        fn=evc_deploy,
        inputs=[url, account, builders, target, owner, model_name, task, version, mode, server_port, sv_ip],
        show_progress='full'
    )
    run_btn.click(
        fn=evc_run,
        inputs=[url, account, builders, target, owner, model_name, task, version, mode, server_port, sv_ip,
                num_clients, num_rounds, tb_port],
        show_progress='full'
    )
    demo.load(read_logs, None, run_logs, every=1, trigger_mode='always_last')

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

    fashion_url = gr.Text(visible=False, value="https://github.com/hibobo98/Fashion.git")
    fashion_model_name = gr.Text(visible=False, value="fashion-test")
    fashion_version = gr.Text(visible=False, value="0.1")
    fashion_task = gr.Text(visible=False, value="detection")
    fashion_mode = gr.Text(visible=False, value="gradio")
    fashion_port = gr.Text(visible=False, value=8779)

    hardhat_url = gr.Text(visible=False, value="https://github.com/hibobo98/Hardhat.git")
    hardhat_model_name = gr.Text(visible=False, value="hardhat-test")
    hardhat_version = gr.Text(visible=False, value="0.2")
    hardhat_task = gr.Text(visible=False, value="detection")
    hardhat_mode = gr.Text(visible=False, value="gradio")
    hardhat_port = gr.Text(visible=False, value=8778)

    windmill_url = gr.Text(visible=False, value="https://github.com/hibobo98/Windmill.git")
    windmill_model_name = gr.Text(visible=False, value="windmill")
    windmill_version = gr.Text(visible=False, value="0.1")
    windmill_task = gr.Text(visible=False, value="detection")
    windmill_mode = gr.Text(visible=False, value="gradio")
    windmill_port = gr.Text(visible=False, value=8776)

    def same(a, b, c, d, e, f):
        return a, b, c, d, e, f
    
    face_btn.click(
        fn=same,
        inputs=[
            face_url,
            face_model_name,
            face_version,
            face_task,
            face_mode,
            face_port,
        ],
        outputs=[
            url,
            model_name,
            version,
            task,
            mode,
            server_port,
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
            fashion_port
        ],
        outputs=[
            url,
            model_name,
            version,
            task,
            mode,
            server_port,
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
        ],
        outputs=[
            url,
            model_name,
            version,
            task,
            mode,
            server_port,
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
        ],
        outputs=[
            url,
            model_name,
            version,
            task,
            mode,
            server_port,
        ]
    )



demo.queue().launch(
    server_name=args.server_name,
    server_port=args.server_port,
    debug=True
)