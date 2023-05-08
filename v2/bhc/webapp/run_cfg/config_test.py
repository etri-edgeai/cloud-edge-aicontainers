import yaml
import pprint
import sys
import os

with open('test.yaml') as f:

    test = yaml.load(f, Loader=yaml.FullLoader)

cfg = test['runs']
pp = pprint.PrettyPrinter(indent=4)


for run in cfg:
    print()
    print("start", run['name'])
    print()
    print()

    pp.pprint(run)
    print()
    print()

    for vars in run['path']:
        if vars:
            globals()[vars] = (run['path'][vars])
            print(f'{vars} : {globals()[vars]}')
    
    for vars in run['vars']:
        if vars:
            globals()[vars] = (run['vars'][vars])
            print(f'{vars} : {globals()[vars]}')