import sqlite3
import argparse
import os
import time
import textwrap
import pandas as pd


class device_manager:

    def __init__(self, db_file, affiliation, name, ip, port, role, owner, hw=None, op_sys=None, gpu=None):
        self.con = sqlite3.connect(db_file)
        self.affiliation = affiliation
        self.name = name
        self.ip = ip
        self.port = port
        self.role = role
        self.owner = owner
        self.hw = hw
        self.op_sys = op_sys
        self.gpu = gpu
        
    def config(self, playbook, registry):

        self.playbook = playbook
        self.registry = registry

    def view(self):

        query = "select DATETIME(time, 'unixepoch') as date, affiliation, name, ip, port, type, owner, hw, os, gpu from nodes;"
        print(pd.read_sql_query(query, self.con))

    def insert(self, hub=False):

        done = True

        try:
            cmd = "ssh-copy-id -p {port} {host_name}@{ip}".format(host_name=self.owner, ip=self.ip, port=self.port)
            if os.system(cmd) != 0:
                raise Exception('Error')
            
        except Exception as e:
            done = False
            print(e, "wrong command.")
            raise

        else:
            with open('tmp/tmp_host.ini', 'w') as f:
                f.write('{name} ansible_host={ip} ansible_port={port}'.format(name=self.name, ip=self.ip, port=self.port))


        if hub == False:
            try:
                cmd = 'ansible-playbook {playbook} -l {name} -i tmp/tmp_host.ini -t http -e "host_name={host_name} registry={registry}"'.format(playbook=self.playbook, name=self.name, host_name=self.owner, registry=self.registry)
                if os.system(cmd) != 0:
                    raise Exception('Error')
                
            except Exception as e:
                print(e, "wrong command.")
                raise

        now = round(time.time())

        data = []

        data.append(now)
        data.append(self.affiliation)
        data.append(self.name)
        data.append(self.ip)
        data.append(self.port)
        data.append(self.role)
        data.append(self.owner)
        data.append(self.hw)
        data.append(self.op_sys)
        data.append(self.gpu)

        data = tuple(data) 

        cur = self.con.cursor()
        query = "insert or ignore into nodes values(?,?,?,?,?,?,?,?,?,?);"
        cur.execute(query, data)
        self.con.commit()

        return done
        

    def delete(self):

        cur = self.con.cursor()
        query = 'delete from nodes where name="{name}"'.format(name=self.name)
        cur.execute(query)
        self.con.commit()


    def file_config(self):

        cur = self.con.cursor()
        query = 'select distinct type from nodes'
        cur.execute(query)
        tmp = cur.fetchall()

        type = []
        for i in tmp:
            i = list(i)
            type.append(i[0])

        
        for t in type:
            if t == 'builder':
                query = 'select name, ip, port from nodes where type="{type}"'.format(type=t)
                cur.execute(query)
                tmp = cur.fetchall()

                builder_data = []

                for i in range(len(tmp)):
                    tmp[i] = list(tmp[i])
                    builder_data.append(tmp[i])

            elif t == 'user':
                query = 'select distinct affiliation from nodes where type="{type}"'.format(type=t)
                cur.execute(query)
                tmp = cur.fetchall()

                group = []

                for i in tmp:
                    i = list(i)
                    group.append(i[0])

                user_data = {}

                for g in group:
                    query = 'select name, ip, port from nodes where affiliation="{group}" and type="{type}"'.format(group=g, type=t)
                    cur.execute(query)
                    tmp = cur.fetchall()
                    user_data[g] = tmp

        

        with open('../hosts.ini','w') as f:

            f.write('[builder]')
            f.write('\n')

            for s in builder_data:
                f.write('{name} ansible_host={ip} ansible_port={port}'.format(name=s[0],ip=s[1],port=s[2]))
                f.write('\n')

            f.write('[user:children]')
            f.write('\n')

            for s in group:
                f.write('{group}'.format(group=s))
                f.write('\n')

            for s in group:
                f.write('[{group}]'.format(group=s))
                f.write('\n')
                for d in user_data[s]:
                    f.write('{name} ansible_host={ip} ansible_port={port}'.format(name=d[0],ip=d[1],port=d[2]))
                    f.write('\n')



if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            
            EVC Device Manager v0.1

            Functions
                - Register new device
                - Delete device
                - write new ansible-inventory
                    (network hosts configuration file for ansible-playbook)
        
            '''
        )
    )
    parser.add_argument(
        '-a',
        '--affiliation',
        type=str,
        help=''
    )
    parser.add_argument(
        '-n',
        '--device_name',
        type=str,
        help=''
    )
    parser.add_argument(
        '-i',
        '--ip_address',
        type=str,
        help=''
    )
    parser.add_argument(
        '-p',
        '--port_number',
        type=str,
        help=''
    )
    parser.add_argument(
        '-t',
        '--usage_type',
        type=str,
        help=''
    )
    parser.add_argument(
        '-o',
        '--owner',
        type=str,
        help=''
    )
    parser.add_argument(
        '--hw',
        type=str,
        help=''
    )
    parser.add_argument(
        '--os',
        type=str,
        help=''
    )
    parser.add_argument(
        '--gpu',
        type=str,
        help=''
    )
    parser.add_argument(
        '--mode',
        type=str,
        help=''
    )
    args = parser.parse_args()
    # print(args)


    db_file = 'db/edge_logs.db3'
    dm = device_manager(
        db_file,
        args.affiliation,
        args.device_name,
        args.ip_address,
        args.port_number,
        args.usage_type,
        args.owner,
        args.hw,
        args.os,
        args.gpu
    )

    if args.mode == 'register':
        new = dm.insert()
        
        if new:
            dm.file_config()
        
    elif args.mode == 'delete':
        dm.delete()
        dm.file_config()

    elif args.mode == 'view':
        dm.view()