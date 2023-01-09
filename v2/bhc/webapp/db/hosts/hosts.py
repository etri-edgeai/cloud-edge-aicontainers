import sqlite3
import json
import numpy as np
import re

## getting Edge nodes list from ansible/hosts file

## parsing hosts.ini
# file = open('/etc/ansible/hosts', 'r')
file = open('../../edge-hosts.ini', 'r')
line_num = 1
f = file.readlines()

## preprocessing
clean = []
p =  re.compile(' [ansible].+')

for w in f:
    w = re.sub(p, "", w)
    w = w.strip('\n')
    clean.append(w)

clean = [v for v in clean if v]

print(clean)

data = []
idx = 0

for w in clean:
    print(w)
    print(type(w))
    idx += 1
    print(idx)

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

print()
print(data)


## db manipulation

# connect to db
con = sqlite3.connect('../nodes.db3')
cur = con.cursor()
query = "insert into nodes values(?,?,?);"

# insert data
cur.execute('delete from nodes;')
cur.executemany(query, data)
con.commit()

# show result
cur.execute('select * from nodes')
print(cur.fetchall())
con.close()


