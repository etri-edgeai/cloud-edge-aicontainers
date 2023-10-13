import yaml
import sys
import os
import get_prj
import argparse
import sqlite3
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from m_model import model_manager
from m_device import device_manager

def get_myprj():
    # load default settings
    sv_file = 'ServerConfig.yaml'

    with open(sv_file) as f:
        default_set = yaml.load(f, Loader=yaml.FullLoader)
        default_cfg = default_set['autorun']

    # set variables
    for vars in default_cfg[0]['path']:
        if vars:
            globals()[vars] = (default_cfg[0]['path'][vars])
            print(vars)

    # load user project
    git_downloader = get_prj.git_downloader(
        url = "https://github.com/ethicsense/esp-python.git",
        account = "ethicsense"
    )
    git_downloader.clone()
    prj_name = git_downloader.get_path()

    user_cfg_file = prj_name + '/myEVCconfig.yaml'
    modelfile = os.getcwd() + '/' + prj_name + '/model.tar.gz'
    dockerfile = os.getcwd() + '/' + prj_name + '/Dockerfile'



    # load user configurations
    with open(user_cfg_file) as f:
        user_cfg = yaml.load(f, Loader=yaml.FullLoader)

    mode = user_cfg['activation']
    owner = user_cfg['owner']
    task = user_cfg['task']
    version = user_cfg['version']
    model_name = user_cfg['model_name']
    # repo = user_cfg['arch'] + '-model'
    data = user_cfg['data']

    return default_set, default_cfg, user_cfg, modelfile, dockerfile, mode, owner, task, version, model_name, data


## db manipulation codes for bypassing exception during experiments & demonstrations
def clean_db():
        con = sqlite3.connect(db)
        cur = con.cursor()
        query = 'delete from modelinfo_detail where model_name="{model_name}" and version="{version}"'.format(model_name=model_name, version=version)
        cur.execute(query)
        con.commit()

        query = "select DATETIME(time, 'unixepoch') as date, owner_name, repo, model_name, size_GB, task, version from modelinfo_detail"
        print(pd.read_sql_query(query, con))


def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


class device_control:

    def host_config():
        # insert builders
        builders = []

        for nodes in default_set['builder']:

            builders.append(nodes['name'])

            dman = device_manager(
                db_file=db,
                affiliation='builder',
                name=nodes['name'],
                ip=nodes['ip'],
                port=nodes['port'],
                type='builder',
                owner='keti',
                hw=nodes['hw'],
                op_sys=nodes['os'],
                gpu=nodes['gpu']
                )
            dman.config(cert_playbook, registry)
            dman.insert(hub=dockerhub)


        # host configuration (build inventory)
        for group in user_cfg['group']:
            for node in user_cfg['target'][group]:

                dman = device_manager(
                    db_file=db,
                    affiliation=group,
                    name=node['name'],
                    ip=node['ip'],
                    port=node['port'],
                    type='user',
                    owner='keti',
                    hw=node['hw'],
                    op_sys=node['os'],
                    gpu=node['gpu']
                    )
                dman.config(cert_playbook, registry)
                dman.insert(hub=dockerhub)

            dman.file_config()
            dman.view()

        return builders



class model_control:

    def build(builders):
        for builder in builders:
            man = model_manager(
                db_file=db,
                # repo=repo,
                owner=owner,
                model_name=model_name,
                task=task,
                version=version,
                model_file=modelfile,
                dockerfile=dockerfile,
                builder=builder
            )
            man.config(
                copy_playbook=copy_playbook,
                build_playbook=build_playbook,
                distrb_playbook=distrb_playbook,
                idx_playbook=idx_playbook,
                hosts_file=hosts_file,
                registry=registry
            )

            done = man.register()

            if done:
                man.insert_db()
                man.view()

    def download(server_port):
        man = model_manager(
            db_file=db,
            owner=owner,
            model_name=model_name,
            task=task,
            version=version,
            model_file=modelfile,
            dockerfile=dockerfile,
        )
        man.config(
            copy_playbook=copy_playbook,
            build_playbook=build_playbook,
            distrb_playbook=distrb_playbook,
            idx_playbook=idx_playbook,
            hosts_file=hosts_file,
            registry=registry
        )
        
        for group in user_cfg['group']:
            man.download(registry, group, server_port)
        # for user in user_cfg['target']:
        #     man.download(registry, user)


    def run(mode, server_name, server_port):
        
        man = model_manager(
            db_file=db,
            owner=owner,
            model_name=model_name,
            task=task,
            version=version,
            model_file=modelfile,
            dockerfile=dockerfile,
        )
        man.config(
            copy_playbook=copy_playbook,
            build_playbook=build_playbook,
            distrb_playbook=distrb_playbook,
            idx_playbook=idx_playbook,
            hosts_file=hosts_file,
            registry=registry
        )

        for group in user_cfg['group']:
            man.download_weights(node=group, file=weight_files)
            man.run(mode=mode, node=group, server_name=server_name, server_port=server_port)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--mode',
        type=str,
        default='flask'
    )
    parser.add_argument(
        '--server_name',
        type=str,
        default="0.0.0.0"
    )
    parser.add_argument(
        '--server_port',
        type=int,
        default=7860
    )
    parser.add_argument(
        '--clean_db',
        type=str2bool,
        default=False
    )
    args = parser.parse_args()

    default_set, default_cfg, user_cfg, modelfile, dockerfile, mode, owner, task, version, model_name, data = get_myprj()

    for run in default_cfg:
        sequence = run['activation']

        if sequence == 'register':
            builders = device_control.host_config()
        
        elif sequence == 'build':
            if args.clean_db:
                print()
                print()
                clean_db()

            model_control.build(builders)

        elif sequence == 'download':
            model_control.download(args.server_port)

        elif sequence == 'run':
            model_control.run(args.mode, args.server_name, args.server_port)