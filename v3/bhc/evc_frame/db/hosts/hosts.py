import sqlite3
import json
import numpy as np
import re

## getting Edge nodes list from ansible/hosts file

## parsing hosts.ini
# file = open('/etc/ansible/hosts', 'r')

def get_hosts(hosts_file, conn):

    file = open('{hosts_file}'.format(hosts_file=hosts_file), 'r')
    f = file.readlines()
    # print(f)

    ## preprocessing
    clean = []
    p1 = re.compile(' ansible_host=')
    p2 = re.compile(' ansible_port=')

    for w in f:
        w = re.sub(p1, " ", w)
        w = re.sub(p2, " ", w)
        w = w.strip('\n')
        clean.append(w)

    clean = [v for v in clean if v]
    # print(clean)

    data = []
    idx = 0
    tmp = []

    for w in clean:
        test = w.split()
        data.append(test)
    
    print(data)

    for w in clean:
        idx += 1

        if "[builders]" in w:
            save = True

            while save:
                tmp = []
                print(idx)
                print(data)
                node_id = np.random.randint(100)
                tmp.append(node_id)
                tmp.append(clean[idx])
                tmp.append('builder')
                tmp = tuple(tmp)
                data.append(tmp)
                idx += 1

                if clean[idx] == '[users]':
                    break

    idx = 0

    for w in clean:
        idx += 1

        if "[users]" in w:
            save = True

            while save:

                try:
                    tmp = []
                    node_id = np.random.randint(100)
                    tmp.append(node_id)
                    tmp.append(clean[idx])
                    tmp.append('user')
                    tmp = tuple(tmp)
                    data.append(tmp)
                    idx += 1

                except:
                    break

    file.close()


    # ## db manipulation

    # # connect to db
    # con = conn
    # cur = con.cursor()
    # query = "insert into nodes values(?,?,?,?,?,?,?,?,?,?);"

    # # insert data
    # cur.execute('delete from nodes;')
    # cur.executemany(query, data)
    # con.commit()

    # # show result
    # cur.execute('select * from nodes')
    # print(cur.fetchall())


if __name__ == '__main__':

    conn = sqlite3.connect('../edge_logs.db3')
    get_hosts('../../hosts.ini', conn)