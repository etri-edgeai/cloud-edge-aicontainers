import sqlite3
import argparse
import os
import time
import textwrap
import pandas as pd
import re
from datetime import datetime

class model_manager:

    def __init__(self, db_file, host, model_name, task, arch, version, model_file, builder, user):

        self.con = sqlite3.connect(db_file)
        self.host = host
        self.arch = arch
        self.task = task
        self.model_name = model_name
        self.version = version
        self.model_file = model_file
        self.builder = builder
        self.user = user

    def config(self, copy_playbook, build_playbook, distrb_playbook, hosts_file):

        self.copy_playbook = copy_playbook
        self.build_playbook = build_playbook
        self.distrb_playbook = distrb_playbook
        self.hosts_file = hosts_file
    
    def insert_db(self):

        os.system('ansible-playbook {playbook} -i {hosts_file} -l {host_name} -t log -e "tag={tag}" > modelinfo.txt'.format(playbook=self.build_playbook, hosts_file=self.hosts_file, host_name=self.builder, tag=self.arch))

        rows = []
        p_start = re.compile('TASK \[get result].+')
        p_end = re.compile('PLAY RECAP.+')

        with open('modelinfo.txt', 'r') as f:

            lines = f.readlines()

        ## search task start line
            for line in lines:
                start = p_start.search(str(line))

                ## save index of string data
                if start:
                    idx = lines.index(line)
                    run = True

                    while run:
                        lines[idx] = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s\.\-\:]", "", lines[idx])
                        lines[idx] = re.sub(" +", " ", lines[idx])
                        lines[idx] = re.sub("\n", "", lines[idx])
                        lines[idx] = re.sub("changed.+", "", lines[idx])

                        rows.append(lines[idx])

                        end = p_end.search(lines[idx])

                        idx += 1

                        if end:
                            run = False

        data =[]
        p_date = re.compile('\d+-\d+-\d+ \d+:\d+:\d+')

        for row in rows:
            if 'date' in row:
                tmp = p_date.findall(row)
                data.append(tmp[0])

            elif 'size' in row:
                row = row.strip(' size')
                row = row.strip('GB')
                data.append(row)

        tmp = []
        log = []
        time_format = "%Y-%m-%d %H:%M:%S"

        tmp.append(time.mktime(datetime.strptime(data[0], time_format).timetuple()))
        tmp.append(self.host)
        tmp.append(self.name)
        tmp.append(data[1])
        tmp.append(self.task)
        tmp.append(self.arch)
        tmp.append(self.version)
        tmp = tuple(tmp)

        log.append(tmp)

        cur = self.con.cursor()
        query = "insert into modelinfo_detail values(?,?,?,?,?,?,?)"
        cur.executemany(query, log)
        self.con.commit()
        
        cur.execute('select * from modelinfo_detail')
        db_show = cur.fetchall()
        
        for row in db_show:
            print(row)


    def register(self):

        query = 'select owner_name, model_name, architecture from modelinfo_detail'
        cur = self.con.cursor()
        cur.execute(query)
        sent = cur.fetchall()
        
        for rows in sent:
            for i in range(len(rows)):
                if self.host in rows[i] and self.model_name in rows[i+1] and self.arch in rows[i+2]:
                    print('host : ', rows[i])
                    print('model name : ', rows[i+1])
                    print('architecture : ', rows[i+2])
                    raise Exception('model already exist. check model list or use "--mode update".')

        try:
            cmd = 'ansible-playbook {playbook} -l rpi6401 -i /home/keti/host.ini -e "model_name={model_file}"'.format(playbook=self.copy_playbook, model_file=self.model_file)
            if os.system(cmd) != 0:
                raise Exception('Error')

        except:
            print("wrong command.")
        
        print('build start')

        try:
            cmd = 'ansible-playbook {playbook} -i {hosts_file} -l {host_name} -t build,test,push -e "tag={tag}, ver={version}"'.format(playbook=self.build_playbook, hosts_file=self.hosts_file, host_name=self.builder, tag=self.model_name, version=self.version)
            if os.system(cmd) != 0:
                raise Exception('Error')
            
        except:
            print("wrong command")

        
    def delete(self):
        
        cmd = '''
        curl -v --silent -H "Accept: application/vnd/docker/distribution.manifest.v2+json" {registry}/v2/{arch}-model/manifests/{model_name}_{version} 2>&1 | grep docker-content-digest | awk '{print ($3)}' > tmp_reg.txt
        '''.format(registry=registry, arch=self.arch, model_name=self.model_name, version=self.version)

        os.system(cmd)

        with open('tmp_reg.txt', 'r') as f:
            data = f.readline()

        cmd = '''
        curl -X DELETE {registry}/v2/{arch}-model/manifests/{content}
        '''.format(registry=registry, arch=self.arch, content=data)

        os.system(cmd)

        cmd = 'docker exec -it edge-registry bin/registry garbage-collect /etc/docker/registry/config.yaml'
        os.system(cmd)
        os.system('docker restart edge-registry')

        query = 'delete from modelinfo_detail where architecture="{arch}" and model_name="{model_name}" and version="{version}"'.format(arch=self.arch, model_name=self.model_name, version=self.version)
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()


    def update(self):

        pass


    def download(self):

        query = 'select owner_name, model_name, architecture from modelinfo_detail'
        cur = self.con.cursor()
        cur.execute(query)
        sent = cur.fetchall()
        
        for rows in sent:
            for i in range(len(rows)):
                if self.host in rows[i] and self.model_name in rows[i+1] and self.arch in rows[i+2]:
                    print('host : ', rows[i])
                    print('model name : ', rows[i+1])
                    print('architecture : ', rows[i+2])
                    print()
                    print('Model found. start distribution.')
                else:
                    raise Exception('Model not found. please check models-list.')
        
        os.system('ansible-playbook {playbook} -l {host_name} -t distrb -i {hosts_file} -e "registry={registry} model_tag={tag}"'.format(playbook=self.distrb_playbook, hosts_file=self.hosts_file, host_name=self.user, registry=registry, tag=self.model_name))

        os.system('ansible-playbook {playbook} -t search -i {hosts_file} -l {host_name}'.format(playbook=playbook, hosts_file=hosts_file, host_name=hosts))


    def run(self):

        pass


    def view(self):

        query = "select DATETIME(time, 'unixepoch') as date, host, model_name, size_GB, task, architecture, version from modelinfo_detail"
        print(pd.read_sql_query(query, self.con))


if __name__ == "__main__":

    registry = '123.214.186.252:39500'
    model_file = 'model.tar.gz'
    copy_playbook_path = '/home/keti/cloud-edge-aicontainers/v2/bhc/webapp/db/model/build/copy_model.yaml'
    build_playbook_path = '/home/keti/cloud-edge-aicontainers/v2/bhc/webapp/db/model/build/autorun.yaml'

    try:
        cmd = 'ansible-playbook {playbook_path} -l rpi6401 -i /home/keti/hosts.ini -e "model_name={model_file}"'.format(playbook_path=playbook_path, model_file=model_file)
        if os.system(cmd) != 0:
            raise Exception('Error')

    except:
        print("wrong command.")

    