import sqlite3
import argparse



class device_manager:

    def __init__(self, db_file, time, group, name, type, owner, hw, os, gpu, ip):
        self.con = sqlite3.connect(db_file)
        self.create_time = time
        self.update_time = time
        self.group = group
        self.name = name
        self.type = type
        self.owner = owner
        self.hw = hw
        self.os = os
        self.gpu = gpu
        self.ip = ip        

    def view(self):
        cur = self.con.cursor()
        cur.execute("select * from nodes;")
        print(cur.fetchall())

    def insert(self):
        data = []

        cur = self.con.cursor()
        query = "insert into nodes values(?,?,?,?,?,?,?,?,?)"
        cur.executemany(query, data)
        self.con.commit()

    def delete(self):
        cur = self.con.cursor()
        query = "delete from nodes where name={name}".format(name=self.name)
        cur.execute(query)
        self.con.commit()

    def file_config(self):
        with open("hosts.ini", "w") as f:
            pass


if __name__ == "__main__":

    pass