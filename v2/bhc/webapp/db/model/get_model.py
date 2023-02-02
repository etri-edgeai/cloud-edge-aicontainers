import sqlite3
import json
import os
import re
import argparse
import textwrap

def get_model_info():
    
    os.system("curl -s https:/123.214.186.252:39500/v2/_catalog -k > modelog.txt")

    with open('modelog.txt', 'r') as f:
        data = json.load(f)
    
    model_list = []

    for repo in data['repositories']:
        os.system("curl -s https://123.214.186.252:39500/v2/{data}/tags/list -k > modelog.txt".format(data=repo))

        with open('modelog.txt', 'r') as f:
            tmp = json.load(f)

        model_list.append(tmp)

    return data['repositories'], model_list
    


def get_desc():
    pass


def model_download(playbook, hosts_file, hosts, registry, model_name, tag):
    
    os.system('ansible-playbook {playbook} -l {host_name} -t distrb -i {hosts_file} -e "registry={registry} image_name={model_name} model_tag={tag}"'.format(playbook=playbook, hosts_file=hosts_file, host_name=hosts, regsitry=registry, model_name=model_name, tag=tag))

    os.system('ansible-playbook {playbook} -t search -i {hosts_file} -l {host_name} > modelog.txt'.format(playbook=playbook, hosts_file=hosts_file, host_name=hosts))

    with open('modelog.txt', 'r') as f:
        lines = f.readlines()

    for line in lines:
        print(line)


if __name__ == "__main__":

    repo_list, model_list = get_model_info()

    for model in model_list:
        print(model)
        print()
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            start model distribution

            --host_name
            --model_name
            --tag
        
            '''
        )
    )

    parser.add_argument(
        '--host_name',
        type=str,
        help='name of node according to which registered in ansible_host file'
    )

    parser.add_argument(
        '--model_name',
        type=str,
        help='AI model which you want to use. consider CPU architecture. (can see above)'
    )

    parser.add_argument(
        '--tag',
        type=str,
        help='AI model which you want to sue. consider Task. (can see above)'
    )

    args = parser.parse_arge()
    print(args)

    