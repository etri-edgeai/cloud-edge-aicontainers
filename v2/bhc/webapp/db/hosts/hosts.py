import sqlite3
import json
import numpy as np

## getting Edge nodes list from ansible/hosts file

## parsing hosts.ini
nodes = []
file = open('/etc/ansible/hosts', 'r')
line_num = 1
line = file.readline()

if "builders" in line:

    while line:
        line = file.readline()

        if len(line.split()) == 2:
            node = line.split()
            node[1] = node[1].strip('ansible_host=')
            node.append('builders')
            node_id = np.random.randint(100)
            node.insert(0, node_id)
            node = tuple(node)
            nodes.append(node)

        line_num += 1

        if "users" in line:

            while line:
                line = file.readline()

                if len(line.split()) == 2:
                    node = line.split()
                    node[1] = node[1].strip('ansible_host=')
                    node.append('users')
                    node_id = np.random.randint(100)
                    node.insert(0, node_id)
                    node = tuple(node)
                    nodes.append(node)

                line_num += 1

file.close()

print(nodes)



## db manipulation
con = sqlite3.connect('../nodes.db3')
cur = con.cursor()
query = "insert into nodes values(?,?,?,?);"

cur.execute('delete from nodes;')
cur.executemany(query, nodes)
con.commit()

cur.execute('select * from nodes')
print(cur.fetchall())
con.close()



