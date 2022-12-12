import os
## test network
print("test if network is available...")
print()
os.system('ansible builders -m ping')
os.system('ansible builders -m command -a "ls -l"')

## build test
tag = "test22"
reg_url = "http://192.168.1.2:5000"

os.system('ansible-playbook copy.yaml -e "Dockerfile_path={Dockerfile_path} zipModel_path={zipModel_path}"'.format(Dockerfile_path=Dockerfile_path, zipModel_path=zipModel_path))


os.system('ansible-playbook autorun.yaml -e "tag={tag} registry={reg_url}"'.format(tag=tag, reg_url=reg_url))
