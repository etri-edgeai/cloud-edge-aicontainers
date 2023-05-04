import yaml
import pprint
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from m_model import model_manager

with open('test.yaml') as f:

    test = yaml.load(f, Loader=yaml.FullLoader)

cfg = test['runs']

# pp = pprint.PrettyPrinter(indent=4)
print("start", cfg[0]['name'])

# action
mode = cfg[0]['activation']

# edge node
nodes = cfg[0]['node']

# files for action
dockerfile = cfg[0]['path']['dockerfile']
model_file = cfg[0]['path']['modelfile']
copy_playbook = cfg[0]['path']['copy_playbook']
build_playbook = cfg[0]['path']['build_playbook']
distrb_playbook = cfg[0]['path']['distrb_playbook']
hosts_file = cfg[0]['path']['hosts_file']
db_file = cfg[0]['path']['db']

# arguments
registry = cfg[0]['vars']['registry']
owner = cfg[0]['vars']['owner']
task = cfg[0]['vars']['task']
model_name = cfg[0]['vars']['model_name']
version = cfg[0]['vars']['version']

# run EVC
for node in nodes:
    man = model_manager(
        db_file=db_file,
        owner=owner,
        model_name=model_name,
        task=task,
        version=version,
        model_file=model_file,
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

