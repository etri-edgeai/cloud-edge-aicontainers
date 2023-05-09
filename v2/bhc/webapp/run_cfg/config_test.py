import yaml
import pprint
import sys
import os
import re

with open('test.yaml') as f:

    test = yaml.load(f, Loader=yaml.FullLoader)

cfg = test['runs']
pp = pprint.PrettyPrinter(indent=4)


for run in cfg:
    print()
    print("start", run['name'])
    print()
    print()

    # pp.pprint(run)
    mode = run['activation']
    print('mode : ', mode)
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


# build_playbook = '/home/keti/cloud-edge-aicontainers/v2/bhc/webapp/db/model/img_build/autorun.yaml'
# hosts_file = '/home/keti/cloud-edge-aicontainers/v2/bhc/webapp/hosts.ini'
# builder = 'n02'
# model_name = 'plate_detector'
# version = 'v1.0'

# os.system('ansible-playbook {playbook} -i {hosts_file} -l {host_name} -t log -e "tag={tag} ver={version}" > modelinfo.txt'.format(playbook=build_playbook, hosts_file=hosts_file, host_name=builder, tag=model_name, version=version))

# rows = []
# p_start = re.compile('TASK \[get result].+')
# p_end = re.compile('PLAY RECAP.+')

# with open('modelinfo.txt', 'r') as f:

#     lines = f.readlines()

# ## search task start line
#     for line in lines:
#         start = p_start.search(str(line))

#         ## save index of string data
#         if start:
#             idx = lines.index(line)
#             run = True

#             while run:
#                 lines[idx] = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s\.\-\:\_]", "", lines[idx])
#                 lines[idx] = re.sub(" +", " ", lines[idx])
#                 lines[idx] = re.sub("\n", "", lines[idx])
#                 lines[idx] = re.sub("changed.+", "", lines[idx])

#                 rows.append(lines[idx])

#                 end = p_end.search(lines[idx])

#                 idx += 1

#                 if end:
#                     run = False

# data =[]
# p_date = re.compile('\d+-\d+-\d+ \d+:\d+:\d+')

# for row in rows:
#     if 'date' in row:
#         tmp = p_date.findall(row)
#         data.append(tmp[0])

#     elif 'size' in row:
#         row = row.strip(' size')
#         row = row.strip('GB')
#         data.append(row)

#     elif 'repo' in row:
#         row = row.strip(' repo')
#         data.append(row)

# print(data)