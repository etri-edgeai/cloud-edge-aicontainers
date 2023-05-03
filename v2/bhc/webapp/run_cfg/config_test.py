import yaml
import pprint
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from m_model import model_manager

with open('test.yaml') as f:

    test = yaml.load(f, Loader=yaml.FullLoader)

cfg = test['runs']

pp = pprint.PrettyPrinter(indent=4)
print("start", cfg[0]['name'])

mode = cfg[0]['activation']
nodes = cfg[0]['node']
dockerfile = cfg[0]['path']['dockerfile']
model_file = cfg[0]['path']['modelfile']
db_file = cfg[0]['path']['db']
registry = cfg[0]['vars']['registry']
owner = cfg[0]['vars']['owner']
task = cfg[0]['vars']['task']
model_name = cfg[0]['vars']['model_name']
version = cfg[0]['vars']['version']

for node in nodes:
    man = model_manager(
        db_file,
        owner,
        model_name,
        task,
        version,
        model_file,
        node
    )

    if mode == 'register':
        done = man.register()

        if done:
            man.insert_db()
            man.view()


    elif mode == 'download':
        man.download()

