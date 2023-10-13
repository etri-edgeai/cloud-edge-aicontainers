import sqlite3
import argparse
import os
import time
import textwrap
import pandas as pd
import re
from datetime import datetime
import json

class model_manager:

    def __init__(self, db_file, owner, model_name, task, version, model_file, dockerfile=None, builder=None, repo=None):

        self.con = sqlite3.connect(db_file)
        self.owner = owner
        self.repo = repo
        self.model_name = model_name
        self.task = task
        self.version = version
        self.model_file = model_file
        self.dockerfile = dockerfile
        self.builder = builder




    def config(self, copy_playbook, build_playbook, distrb_playbook, idx_playbook, hosts_file, registry):

        self.copy_playbook = copy_playbook
        self.build_playbook = build_playbook
        self.distrb_playbook = distrb_playbook
        self.idx_playbook = idx_playbook
        self.hosts_file = hosts_file
        self.registry = registry




    def insert_db(self):

        os.system('ansible-playbook {playbook} -i {hosts_file} -l {builder} -t log -e "tag={tag} ver={version}" > tmp/modelinfo.txt'.format(playbook=self.build_playbook, hosts_file=self.hosts_file, tag=self.model_name, version=self.version, builder=self.builder ))

        rows = []
        p_start = re.compile('TASK \[get result].+')
        p_end = re.compile('PLAY RECAP.+')

        with open('tmp/modelinfo.txt', 'r') as f:

            lines = f.readlines()

        ## search task start line
            for line in lines:
                start = p_start.search(str(line))

                ## save index of string data
                if start:
                    idx = lines.index(line)
                    run = True

                    while run:
                        lines[idx] = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s\.\-\:\_]", "", lines[idx])
                        lines[idx] = re.sub(" +", " ", lines[idx])
                        lines[idx] = re.sub("\n", "", lines[idx])
                        lines[idx] = re.sub("changed.+", "", lines[idx])
                        lines[idx] = re.sub("ok.+", "", lines[idx])

                        rows.append(lines[idx])

                        end = p_end.search(lines[idx])

                        idx += 1

                        if end:
                            run = False

        lst = []
        p_date = re.compile('\d+-\d+-\d+ \d+:\d+:\d+')

        for row in rows:
            if 'date' in row:
                tmp = p_date.findall(row)
                lst.append(tmp[0])

            elif 'size' in row:
                row = row.strip(' size')
                row = row.strip('GB')
                lst.append(row)

            elif 'repo' in row:
                row = row.strip(' repo')
                lst.append(row)

        n = 3
        data = [lst[i * n:(i + 1) * n] for i in range((len(lst) + n - 1) // n)]

        log = []
        time_format = "%Y-%m-%d %H:%M:%S"

        for d in data:
            tmp = []
            tmp.append(time.mktime(datetime.strptime(d[0], time_format).timetuple()))
            tmp.append(self.owner)
            tmp.append(d[2])
            tmp.append(self.model_name)
            tmp.append(d[1])
            tmp.append(self.task)
            tmp.append(self.version)
            log.append(tmp)

        for i in range(len(log)):
            log[i] = tuple(log[i])

        cur = self.con.cursor()
        query = "insert or ignore into modelinfo_detail values(?,?,?,?,?,?,?)"
        cur.executemany(query, log)
        self.con.commit()
        
        ## print db present
        # cur.execute('select * from modelinfo_detail')
        # db_show = cur.fetchall()
        
        # for row in db_show:
        #     print(row)




    def register(self):

        done = True

        query = 'select owner_name, repo, model_name, version from modelinfo_detail'
        cur = self.con.cursor()
        cur.execute(query)
        sent = cur.fetchall()

        os.system('ansible-playbook {playbook} -i {hosts_file} -l {builder}> tmp/index.txt'.format(playbook=self.idx_playbook, hosts_file=self.hosts_file, builder=self.builder))
        
        rows = []
        p_start = re.compile('TASK \[get CPU architecture].+')
        p_end = re.compile('PLAY RECAP.+')

        with open('tmp/index.txt', 'r') as f:
            lines = f.readlines()

            for line in lines:
                start = p_start.search(str(line))

                if start:
                    idx = lines.index(line)
                    run = True
                    idx += 1

                    while run:
                        lines[idx] = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s\.\-\:\_]", "", lines[idx])
                        lines[idx] = re.sub(" +", " ", lines[idx])
                        lines[idx] = re.sub("\n", "", lines[idx])
                        lines[idx] = re.sub("changed.+", "", lines[idx])
                        lines[idx] = re.sub("ok: ", "", lines[idx])
                        lines[idx] = re.sub(" ansible_factsarchitecture: ", "", lines[idx])

                        rows.append(lines[idx])
                        end = p_end.search(lines[idx])
                        idx += 1

                        if end:
                            run = False
        
        self.repo = rows[1]

        for rows in sent:
            for i in range(len(rows)):
                if self.owner in rows[i] and self.repo in rows[i+1] and self.model_name in rows[i+2] and self.version in rows[i+3]:
                    print('host : ', rows[i])
                    print('repository : ', rows[i+1])
                    print('model name : ', rows[i+2])
                    print('architecture : ', rows[i+3])
                    raise Exception('model already exist. check model list or use "--mode update".')

        try:
            ## copy
            cmd = 'ansible-playbook {playbook} -l {builder} -i {hosts_file} -e "model_file={model_file} dockerfile={dockerfile}"'.format(playbook=self.copy_playbook, hosts_file=self.hosts_file, model_file=self.model_file, dockerfile=self.dockerfile, builder=self.builder)

            if os.system(cmd) != 0:
                raise Exception('Wrong Command.')

        except Exception as e:
            done = False
            raise
        
        print('build start')

        try:
            ## build
            cmd = 'ansible-playbook {playbook} -i {hosts_file} -l {builder} -t build,test,push -e "tag={tag} ver={version} model_file={model_file} registry_ip={registry}"'.format(playbook=self.build_playbook, hosts_file=self.hosts_file, tag=self.model_name, version=self.version, model_file=self.model_file, registry=self.registry, builder=self.builder)

            if os.system(cmd) != 0:
                raise Exception('Wrong Command.')
            
        except Exception as e:
            done = False
            raise

        return done




    def delete(self):

        # done = True
        # hash = "'{print ($3)}'"
        # cmd = '''
        # curl -v --silent -H "Accept: application/vnd/docker/distribution.manifest.v2+json" https://{registry}/v2/{repo}/manifests/{model_name}_{version} -k 2>&1 | grep docker-content-digest | awk {hash} > tmp_reg.txt
        # '''.format(registry=registry, repo=repo, model_name=self.model_name, version=self.version, hash=hash)

        # os.system(cmd)

        # with open('tmp_reg.txt', 'r') as f:
        #     data = f.readline()

        # data = data.replace("\n", "")
        # print(data)

        # try:
        #     cmd = '''
        #     curl -X DELETE -v https://{registry}/v2/{repo}/manifests/{content}
        #     '''.format(registry=registry, repo=repo, content=data)

        #     if os.system(cmd) != 0:
        #         raise Exception('Wrong Command.')
            
        # except Exception as e:
        #     done = False
        #     raise

        done = True
        path = '/var/lib/registry/docker/registry/v2/repositories'

        try:
            cmd = 'docker exec -it evc-registry rm -rf {path}/{repo}/_manifests/tags/{model_name}_{version}'.format(path=path, repo=self.repo, model_name=self.model_name, version=self.version)

            if os.system(cmd) != 0:
                raise Exception('Wrong Command.')
            
            else:
                print()
                print('deletion done.')
                print()
                print('start grabage-collection.')
                print()
        
        except Exception as e:
            done = False
            raise

        try:
            cmd = 'docker exec -it evc-registry bin/registry garbage-collect /etc/docker/registry/config.yml'
            
            if os.system(cmd) != 0:
                raise Exception('Wrong Command.')
            
            else:
                os.system('docker restart evc-registry')
        
        except Exception as e:
            done = False
            raise

        return done




    def delete_db(self):

        query = 'delete from modelinfo_detail where owner_name="{owner}" and repo="{repo}" and model_name="{model_name}" and version="{version}";'.format(owner=self.owner, repo=self.repo, model_name=self.model_name, version=self.version)

        print(query)
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()




    def update(self):

        done = True

        query = 'select version from modelinfo_detail where owner_name="{owner}" and model_name="{model_name}" and task="{task}"'.format(owner=self.owner, model_name=self.model_name, task=self.task)
        cur = self.con.cursor()
        cur.execute(query)
        sent = cur.fetchone()

        print(sent[0])

        if sent[0] == self.version:
            raise Exception('already have the version. please double-check the model list.')

        else:
            print(
                '''
                ================================================================
                =================== start AI model update ======================
                ================================================================
                '''
            )

        try:
            ## copy
            cmd = 'ansible-playbook {playbook} -l {builder} -i {hosts_file} -e "model_file={model_file} dockerfile={dockerfile}"'.format(playbook=self.copy_playbook, builder=self.builder, hosts_file=self.hosts_file, model_file=self.model_file, dockerfile=self.dockerfile)

            if os.system(cmd) != 0:
                raise Exception('Wrong Command.')

        except Exception as e:
            done = False
            raise
        

        try:
            ## build
            cmd = 'ansible-playbook {playbook} -i {hosts_file} -l {host_name} -t build,test,push -e "tag={tag} ver={version} model_file={model_file}"'.format(playbook=self.build_playbook, hosts_file=self.hosts_file, host_name=self.builder, tag=self.model_name, version=self.version, model_file=self.model_file)

            if os.system(cmd) != 0:
                raise Exception('Wrong Command.')
            
        except Exception as e:
            done = False
            raise

        return done




    def download(self, registry, node, server_port):

        query = 'select owner_name, model_name, version from modelinfo_detail'
        cur = self.con.cursor()
        cur.execute(query)
        sent = cur.fetchall()
        
        for rows in sent:
            for i in range(len(rows)):
                if self.owner in rows[i] and self.model_name in rows[i+1] and self.version in rows[i+2]:
                    print('owner : ', rows[i])
                    print('model name : ', rows[i+1])
                    print('version : ', rows[i+2])
                    print()
                    print('Model found. start distribution.')
                    break

                # else:
                #     raise Exception('Model not found. please check models-list.')

        ## model download to user_node
        os.system('ansible-playbook {playbook} -l {node_name} -t distrb -i {hosts_file} -e "registry={registry} model_tag={tag} version={version} server_port={server_port}"'.format(playbook=self.distrb_playbook, hosts_file=self.hosts_file, node_name=node, registry=registry, tag=self.model_name, version=self.version, server_port=server_port))

        print()
        print('Show result')
        print()

        ## docker image list to user_node
        os.system('ansible-playbook {playbook} -t search -i {hosts_file} -l {host_name}'.format(playbook=self.distrb_playbook, hosts_file=self.hosts_file, host_name=node))



    def run(self, mode, node, server_name, server_port):

        if mode == 'gradio':
            os.system('ansible-playbook {playbook} -l {node} -t gradio -i {hosts_file} -e "registry={registry} model_tag={tag} version={version} server_name={server_name} server_port={server_port}"'.format(registry=self.registry, tag=self.model_name, version=self.version, playbook=self.distrb_playbook, node=node, hosts_file=self.hosts_file, server_name=server_name, server_port=server_port))    
        elif mode == 'flask':
            os.system('ansible-playbook {playbook} -l {node} -t flask -i {hosts_file} -e "registry={registry} model_tag={tag} version={version} server_name={server_name} server_port={server_port}"'.format(registry=self.registry, tag=self.model_name, version=self.version, playbook=self.distrb_playbook, node=node, hosts_file=self.hosts_file, server_name=server_name, server_port=server_port))



    def download_weights(self, node, file):
        
        os.system(f'ansible-playbook {self.distrb_playbook} -l {node} -t weights -i {self.hosts_file} -e "weight_file={file}"')

    def view(self):
        
        query = "select DATETIME(time, 'unixepoch') as date, owner_name, repo, model_name, size_GB, task, version from modelinfo_detail"
        print(pd.read_sql_query(query, self.con))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            
            EVC AI Model Manager v0.1

            Functions
                - Register new model
                - Delete model
                - Update model
                - View model list
                - Download model
                - Run model
        
            '''
        )
    )
    parser.add_argument(
        '--owner',
        type=str,
        help=''
    )
    parser.add_argument(
        '--task',
        type=str,
        help=''
    )
    parser.add_argument(
        '--model_name',
        type=str,
        help=''
    )
    parser.add_argument(
        '--version',
        type=str,
        help=''
    )
    parser.add_argument(
        '--model_file',
        type=str,
        help=''
    )
    parser.add_argument(
        '--builder',
        type=str,
        help=''
    )
    parser.add_argument(
        '--user',
        type=str,
        help=''
    )
    parser.add_argument(
        '--mode',
        type=str,
        help=''
    )
    parser.add_argument(
        '--repo',
        type=str,
        help=''
    )
    args = parser.parse_args()

    registry = '123.214.186.252:39500'
    db_file = "./db/edge_logs.db3"
    copy_playbook_path = './playbooks/copy_model.yaml'
    build_playbook_path = './playbooks/autorun.yaml'
    distrb_playbook_path = './playbooks/run_model.yaml'
    hosts_file_path = './hosts.ini'

    manager = model_manager(
        db_file=db_file,
        owner=args.owner,
        repo=args.repo,
        model_name=args.model_name,
        task=args.task,
        version=args.version,
        model_file=args.model_file,
        builder=args.builder
        )
    print(args)

    manager.config(copy_playbook_path, build_playbook_path, distrb_playbook_path, hosts_file_path)

    if args.mode == 'register':
        done = manager.register()

        if done:
            manager.insert_db()
            manager.view()
    

    elif args.mode == 'delete':
        done = manager.delete()

        if done:
            manager.delete_db()
            manager.view()


    elif args.mode == 'view':
        manager.view()


    elif args.mode == 'download':
        manager.download(node=args.user)


    elif args.mode == 'update':
        done = manager.update()

        if done:
            manager.insert_db()
            manager.view()

    elif args.mode == 'db_config':
        manager.insert_db()
        # manager.view()