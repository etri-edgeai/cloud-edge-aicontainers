import yaml
import sys
import os
import get_prj

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from m_model import model_manager



# load default settings
sv_file = 'test.yaml'

with open(sv_file) as f:
    default_set = yaml.load(f, Loader=yaml.FullLoader)
    default_cfg = default_set['autorun']



# load user project
git_downloader = get_prj.git_downloader(
    url = "git@github.com:ethicsense/EVC_test.git"
)
git_downloader.clone()
prj_name = git_downloader.get_path()

user_cfg_file = prj_name + '/myEVCconfig.yaml'
modelfile = os.getcwd() + '/' + prj_name + '/model.tar.gz'
dockerfile = os.getcwd() + '/' + prj_name + '/Dockerfile'



# load user configurations
with open(user_cfg_file) as f:
    user_cfg = yaml.load(f, Loader=yaml.FullLoader)

owner = user_cfg['owner']
task = user_cfg['task']
version = user_cfg['version']
model_name = user_cfg['model_name']
repo = user_cfg['arch'] + '-model'


if user_cfg['arch'] == 'aarch64':
    builder = 'rpi6401'

elif user_cfg['arch'] == 'x86-64':
    builder = 'n02'



# run EVC
for run in default_cfg:
    mode = run['activation']

    for vars in run['path']:
        if vars:
            globals()[vars] = (run['path'][vars])
    
    man = model_manager(
        db_file=db,
        repo=repo,
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
        hosts_file=hosts_file
    )

    if mode == 'register':
        done = man.register()

        if done:
            man.insert_db()
            man.view()

    elif mode == 'download':
        for user in user_cfg['target']:
            man.download(registry, user)

    # elif mode == 'run':
    #     man.model_run()