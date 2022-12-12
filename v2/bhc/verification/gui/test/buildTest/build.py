import os
## test network
os.system('ansible builders -m ping')
os.system('ansible builders -m command -a "ls -l"')

## build test
tag = "test22"
reg_url = "192.168.1.2:5000"
os.system('ansible-playbook copy.yaml')
os.system('ansible-playbook autorun.yaml -e "tag={tag} registry={reg_url}"'.format(tag=tag, reg_url=reg_url))
