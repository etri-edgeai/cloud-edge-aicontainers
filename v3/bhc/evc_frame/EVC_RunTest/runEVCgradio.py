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

def get_myprj(url, account):
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
        url = url,
        account = account
    )
    git_downloader.clone()
    prj_name = git_downloader.get_path()

    modelfile = os.getcwd() + '/' + prj_name + '/model.tar.gz'
    dockerfile = os.getcwd() + '/' + prj_name + '/Dockerfile'


    return default_set, default_cfg, modelfile, dockerfile


## db manipulation codes for bypassing exception during experiments & demonstrations
def clean_db(model_name, version):
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

    def builder_config(default_set):

        builders = []

        for nodes in default_set['builder']:

            builders.append(nodes['name'])

            dman = device_manager(
                db_file=db,
                affiliation='builder',
                name=nodes['name'],
                ip=nodes['ip'],
                port=nodes['port'],
                role='builder',
                owner='keti',
                hw=nodes['hw'],
                op_sys=nodes['os'],
                gpu=nodes['gpu']
                )
            dman.config(cert_playbook, registry)
            dman.insert(hub=dockerhub)

        return builders

    def node_config(group, node, ip, port, owner):

        # host configuration (build inventory)
        dman = device_manager(
            db_file=db,
            affiliation=group,
            name=node,
            ip=ip,
            port=port,
            role='user',
            owner=owner
            )
        dman.config(cert_playbook, registry)
        dman.insert(hub=dockerhub)

        dman.file_config()
        dman.view()

    def node_delete(group, node, ip, port, owner):

        # host configuration (build inventory)
        dman = device_manager(
            db_file=db,
            affiliation=group,
            name=node,
            ip=ip,
            port=port,
            role='user',
            owner=owner
            )
        dman.config(cert_playbook, registry)
        dman.delete_users()
        dman.view()



class model_control:

    def build(builders, owner, model_name, task, version, modelfile, dockerfile):
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

    def download(group, owner, model_name, task, version, modelfile, dockerfile, server_port):
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
        
        man.download(registry, group, server_port)


    def run(group, owner, model_name, task, version, modelfile, dockerfile, mode, server_port, sv_ip=None):
        
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

        man.run(mode=mode, node=group, server_port=server_port, sv_ip=sv_ip)




















if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prj_url",
        type=str
    )
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

    default_set, default_cfg, user_cfg, modelfile, dockerfile, mode, owner, task, version, model_name, data = get_myprj(args.prj_url)

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
            out = model_control.run(args.mode, args.server_name, args.server_port)