import sqlite3
import argparse
import os
import time
import textwrap


class device_manager:

    def __init__(self, db_file, affiliation, name, ip, port, type, owner, hw, op_sys, gpu):
        self.con = sqlite3.connect(db_file)
        self.affiliation = affiliation
        self.name = name
        self.ip = ip
        self.port = port
        self.type = type
        self.owner = owner
        self.hw = hw
        self.op_sys = op_sys
        self.gpu = gpu
        

    def view(self):
        cur = self.con.cursor()
        cur.execute("select * from nodes;")
        print(cur.fetchall())

    def insert(self):
        try:
            cmd = "ssh-copy-id {host_name}@{ip} -p {port}".format(host_name=self.owner, ip=self.ip, port=self.port)
            if os.system(cmd) != 0:
                raise Exception('Error')
        except:
            print("wrong command.")
        else:
            with open('/home/keti/tmp_host.ini', 'w') as f:
                f.write('{name} ansible_host={ip} ansible_port={port}'.format(name=self.name, ip=self.ip, port=self.port))


        try:
            cmd = 'ansible-playbook copy_cert.yaml -l {name} -i /home/keti/tmp_host.ini -e "host_name={host_name}"'.format(name=self.name, host_name=self.owner)
            if os.system(cmd) != 0:
                raise Exception('Error')
        except:
            print("wrong command.")
        else:
            now = round(time.time())

            data = []

            data.append(now)
            data.append(self.affiliation)
            data.append(self.name)
            data.append(self.ip)
            data.append(self.port)
            data.append(self.type)
            data.append(self.owner)
            data.append(self.hw)
            data.append(self.op_sys)
            data.append(self.gpu)

            data = tuple(data) 

            cur = self.con.cursor()
            query = "insert into nodes values(?,?,?,?,?,?,?,?,?,?);"
            cur.execute(query, data)
            self.con.commit()
        

    def delete(self):
        cur = self.con.cursor()
        query = "delete from nodes where name={name}".format(name=self.name)
        cur.execute(query)
        self.con.commit()


    def file_config(self):
        cur = self.con.cursor()
        cur.execute('select name, ip, port from nodes where type=builder;')
        print(cur.fetchall())

        with open("hosts.ini", "w") as f:
            pass


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
    print(args)


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
        dm.insert()
        dm.file_config()
        
    elif args.mode == 'delete':
        dm.delete()
        dm.file_config()