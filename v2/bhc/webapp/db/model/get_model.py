import sqlite3
import json
import os
import re
import argparse
import textwrap
import time

def get_model_info(registry, conn):
    
    os.system("curl -s https://{registry}/v2/_catalog -k > tmp/modelog.txt".format(registry=registry))

    with open('modelog.txt', 'r') as f:
        data = json.load(f)
    
    model_list = []

    for repo in data['repositories']:
        os.system("curl -s https://{registry}/v2/{data}/tags/list -k > tmp/modelog.txt".format(registry=registry, data=repo))

        with open('modelog.txt', 'r') as f:
            tmp = json.load(f)

        model_list.append(tmp)

    data = []

    for models in model_list :
        for tag in models['tags']:
            tmp = []
            tmp.append(models['name'])
            tmp.append(tag)
            data.append(tmp)

    for i in range(len(data)):
        data[i] = tuple(data[i])

    con = conn
    cur = con.cursor()
    cur.execute("delete from model_list")
    query = "insert into model_list values(?,?);"
    cur.executemany(query, data)
    con.commit()

    cur.execute('select * from model_list;')
    out = cur.fetchall()

    for col in out :
        print(col)



def init_progress(conn):

    cur = conn.cursor()
    cur.execute("delete from model_desc;")
    cur.execute("delete from dstrb_progress;")
    conn.commit()
    


def get_desc(host, tag, conn):
    
    if tag == 'imagenet':
        desc = '''
            Keras Applications 라이브러리에서 제공하는 사전학습 모델들입니다.
            크게 11종류의 이미지 분류 모델을 지원합니다.
            각 모델의 성능은 ImageNet dataset을 기준으로 측정하였습니다.
            ImageNet dataset은 약 1천개의 클래스를 가진 데이터셋입니다.
            Refence url : 
                Keras Applications : https://keras.io/api/applications/
                ImageNet : https://www.image-net.org/
        '''
    
    data = []
    data.append(host)
    data.append(tag)
    data.append(desc)

    cur = conn.cursor()
    query = "insert into model_desc values(?,?,?);"
    cur.execute(query, data)
    conn.commit()



def model_download(playbook, hosts_file, registry, hosts, tag):
    
    data = []
    tmp = []

    now = round(time.time())
    name = hosts
    rst = "Distribution Activating..."

    tmp.append(now)
    tmp.append(name)
    tmp.append(rst)
    
    tmp = tuple(tmp)
    data.append(tmp)

    cur = conn.cursor()
    query = "insert into dstrb_progress values(?,?,?);"
    cur.executemany(query, data)
    conn.commit()
    
    os.system('ansible-playbook {playbook} -l {host_name} -t distrb -i {hosts_file} -e "registry={registry} model_tag={tag}"'.format(playbook=playbook, hosts_file=hosts_file, host_name=hosts, registry=registry, tag=tag))

    os.system('ansible-playbook {playbook} -t search -i {hosts_file} -l {host_name}'.format(playbook=playbook, hosts_file=hosts_file, host_name=hosts))

    


if __name__ == "__main__":
   
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            start model distribution

            python get_model.py
            --playbook
            --hosts_file
            --registry
            --host
            --tag
        
            '''
        )
    )
    parser.add_argument(
        '--playbook',
        default='get_model.yaml',
        type=str,
        help='ansible-playbook file path'
    )
    parser.add_argument(
        '--hosts_file',
        default='../../edge-hosts.ini',
        type=str,
        help='ansible hosts.ini file path'
    )
    parser.add_argument(
        '--registry',
        default='123.214.186.252:39500',
        type=str,
        help='regsitry server ip address or domain'
    )
    parser.add_argument(
        '--host',
        type=str,
        help='name of node according to which registered in ansible_host file'
    )
    parser.add_argument(
        '--tag',
        type=str,
        help='AI model which you want to use. choose Task. (can see above)'
    )

    args = parser.parse_args()
    print(args)

    conn = sqlite3.connect('../edge_logs.db3')

    get_desc(args.host, args.tag, conn)

    model_download(
        args.playbook,
        args.hosts_file,
        args.registry,
        args.host,
        args.tag
    )

    data = []
    tmp = []

    now = round(time.time())
    rst = 'Distribution Done !'

    tmp.append(now)
    tmp.append(args.host)
    tmp.append(rst)
    tmp = tuple(tmp)
    data.append(tmp)

    cur = conn.cursor()
    query = "insert into dstrb_progress values(?,?,?);"
    cur.executemany(query, data)
    conn.commit()