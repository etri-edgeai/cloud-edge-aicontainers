import sqlite3
import argparse
import os


class device_manager:

    def __init__(self, db_file, time, group, name, ip, port, type, owner, hw, os, gpu):
        self.con = sqlite3.connect(db_file)
        self.create_time = time
        self.group = group
        self.name = name
        self.ip = ip
        self.port = port
        self.type = type
        self.owner = owner
        self.hw = hw
        self.os = os
        self.gpu = gpu
        

    def view(self):
        cur = self.con.cursor()
        cur.execute("select * from nodes;")
        print(cur.fetchall())

    def insert(self):
        # data = []

        # cur = self.con.cursor()
        # query = "insert into nodes values(?,?,?,?,?,?,?,?,?)"
        # cur.executemany(query, data)
        # self.con.commit()

        os.system("ssh-copy-id {name}@{ip} -p {port}".format(name=self.name, ip=self.ip, port=self.port))

        with open('/home/keti/tmp_host.ini', 'w') as f:
            f.write('{name} ansible_host={ip} ansible_port={port}')

        os.system('ansible-playbook ~/copy_cert.yaml -l n02 -i /home/keti/tmp_host.ini')



        

    def delete(self):
        cur = self.con.cursor()
        query = "delete from nodes where name={name}".format(name=self.name)
        cur.execute(query)
        self.con.commit()


    def file_config(self):
        with open("hosts.ini", "w") as f:
            pass


if __name__ == "__main__":

    group = 'keti'
    name = 'n02'
    ip = '123.214.186.192'
    num_port = '33322'

    os.system("ssh-copy-id {group}@{ip} -p {port}".format(group=group, ip=ip, port=num_port))

    with open('/home/keti/tmp_host.ini', 'w') as f:
        f.write('{name} ansible_host={ip} ansible_port={port}'.format(name=name, ip=ip, port=num_port))

    os.system('ansible-playbook /home/keti/copy_cert.yaml -l n02 -i /home/keti/tmp_host.ini')