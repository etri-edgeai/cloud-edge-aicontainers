import yaml
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from m_model import model_manager

with open('test.yaml') as f:

    test = yaml.load(f, Loader=yaml.FullLoader)

cfg = test['runs']


# load configurations
for run in cfg:
    print()
    print("start", run['name'])
    print()
    print()

    # action
    mode = run['activation']
    # edge node
    nodes = run['node']

    for vars in run['path']:
        if vars:
            globals()[vars] = (run['path'][vars])
            print(f'{vars} : {globals()[vars]}')
    
    for vars in run['vars']:
        if vars:
            globals()[vars] = (run['vars'][vars])
            print(f'{vars} : {globals()[vars]}')


    # run EVC
    for node in nodes:
        man = model_manager(
            db_file=db,
            owner=owner,
            model_name=model_name,
            task=task,
            version=version,
            model_file=modelfile,
            dockerfile=dockerfile,
            builder=node
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
            man.download()

