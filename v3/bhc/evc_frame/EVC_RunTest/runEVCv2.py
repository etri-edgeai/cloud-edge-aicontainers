import yaml
import sys
import os
import get_prj

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from m_model import model_manager
from m_device import device_manager


# load default settings
sv_file = 'ServerConfig.yaml'

with open(sv_file) as f:
    default_set = yaml.load(f, Loader=yaml.FullLoader)
    default_cfg = default_set['autorun']

# set variables
for vars in default_cfg[0]['path']:
    if vars:
        globals()[vars] = (default_cfg[0]['path'][vars])

# load user project
git_downloader = get_prj.git_downloader(
    url = "git@github.com:ethicsense/EVC_test2.git"
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
repo = user_cfg['arch'] + '-model'
data = user_cfg['data']



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
    dman.config(cert_playbook)
    dman.insert()


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
        dman.config(cert_playbook)
        dman.insert()

    dman.file_config()
    dman.view()

    # set builder
    if 'rpi' in group:
        builder = 'rpi6401'
    elif 'nuc' in group:
        builder = 'n01'

# run EVC
for run in default_cfg:
    sequence = run['activation']
    
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

    if sequence == 'register':
        done = man.register()

        if done:
            man.insert_db()
            man.view()

    elif sequence == 'download':
        for group in user_cfg['group']:
            man.download(registry, group)
        # for user in user_cfg['target']:
        #     man.download(registry, user)

    elif sequence == 'run':
        for user in user_cfg['target']:
            man.run(
            mode=mode,
            node=user,
            data=data
            )