import sqlite3

import os
import re

import schedule
import time

import warnings

warnings.filterwarnings(action='ignore')


def get_current_traffic(playbook, hosts_file, conn):

    os.system('ansible-playbook {playbook} -i {hosts_file} -t network,traffic --extra-vars "ansible_sudo_pass=ketiabcs" > test.txt'.format(playbook=playbook, hosts_file=hosts_file))

    rows = []
    p_start = re.compile('TASK \[get current traffic].+')
    p_end = re.compile('PLAY RECAP.+')

    with open('test.txt', 'r') as f:

        lines = f.readlines()

        for line in lines:
            print(line)

    ## search task start line
        for line in lines:
            start = p_start.search(str(line))

            ## save index of string data
            if start:
                idx = lines.index(line)
                run = True

                while run:
                    ## drop no-useful strings and characters
                    lines[idx] = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s\.]", "", lines[idx])
                    lines[idx] = re.sub(" +", " ", lines[idx])
                    lines[idx] = re.sub("\n", "", lines[idx])
                    lines[idx] = re.sub("changed.+", "", lines[idx])

                    rows.append(lines[idx])
                    ## search end of task
                    end = p_end.search(lines[idx])

                    idx += 1

                    if end:
                        run = False

    rows = [v for v in rows if v]

    for row in rows:
        rows[rows.index(row)] = row.strip()

    nodes = []

    con = conn
    cur = con.cursor()
    cur.execute('select name from nodes where type = "user"')
    tmp = cur.fetchall()

    for node in tmp:
        node = str(node)
        node = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", node)
        nodes.append(node)

    data = []

    p_rx = re.compile('rx\s+[\d.]+')
    p_tx = re.compile('tx\s+[\d.]+')

    for node in nodes:
        for row in rows:
            if node in row:
                idx = rows.index(row)
                idx += 1

                tmp = []

                if 'msg' in rows[idx]:
                    rx = p_rx.findall(rows[idx])
                    rx = re.sub("[^0-9.]", "", str(rx))
                    tx = p_tx.findall(rows[idx])
                    tx = re.sub("[^0-9.]", "", str(tx))

                    tmp.append(rx)
                    tmp.append(tx)

                    d= []

                    for i in range(len(tmp)):
                        d.append(tmp[i])

                    data.append(d)

    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = float(data[i][j])

    print(data)

    now = round(time.time())
    log = []

    for i in range(len(nodes)):
        tmp = []
        tmp.append(now)
        tmp.append(nodes[i])
        tmp.append(data[i][0])
        tmp.append(data[i][1])
        tmp = tuple(tmp)
        log.append(tmp)

    print(log)

    # ## insert data into DB
    # con = conn
    # cur = con.cursor()
    # query = "insert into traffic values(?,?,?,?);"
    # cur.executemany(query, log)
    # con.commit()

    # ## show result
    # cur.execute('select * from traffic')
    # out = cur.fetchall()

    # for col in out:
    #     print(col)



def get_traffic_json(playbook, hosts_file, conn):

    os.system('ansible-playbook {playbook} -i {hosts_file} -t network,traffic --extra-vars "ansible_sudo_pass=ketiabcs" > tmp/netlog.txt'.format(playbook=playbook, hosts_file=hosts_file))

    rows = []
    p_start = re.compile('TASK \[Debug].+')
    p_end = re.compile('PLAY RECAP.+')

    with open('tmp/netlog.txt', 'r') as f:

        lines = f.readlines()

    ## search task start line
        for line in lines:
            start = p_start.search(str(line))

            ## save index of string data
            if start:
                idx = lines.index(line)
                run = True

                while run:
                    ## drop no-useful strings and characters
                    lines[idx] = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s\.]", "", lines[idx])
                    lines[idx] = re.sub(" +", " ", lines[idx])
                    lines[idx] = re.sub("\n", "", lines[idx])
                    lines[idx] = re.sub("changed.+", "", lines[idx])

                    rows.append(lines[idx])
                    ## search end of task
                    end = p_end.search(lines[idx])

                    idx += 1

                    if end:
                        run = False

    rows = [v for v in rows if v]

    for row in rows:
        rows[rows.index(row)] = row.strip()

    nodes = []

    con = conn
    cur = con.cursor()
    cur.execute('select name from nodes where type = "user"')
    tmp = cur.fetchall()

    for node in tmp:
        node = str(node)
        node = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", node)
        nodes.append(node)

    data = []

    p_rx = re.compile('RX\d+')
    p_tx = re.compile('TX\d+')
    now = round(time.time())
    
    for node in nodes:
        for row in rows:
            if node in row:
                tmp = []
                idx = rows.index(row)
                idx += 1
                tmp.append(now)
                tmp.append(node)

                if 'msg' in rows[idx]:
                    rx = p_rx.findall(rows[idx])
                    rx = re.sub("[^0-9.]", "", str(rx))
                    tx = p_tx.findall(rows[idx])
                    tx = re.sub("[^0-9.]", "", str(tx))

                    tmp.append(rx)
                    tmp.append(tx)
                    data.append(tmp)

    for i in range(len(data)):
        data[i] = tuple(data[i])
    
    cur = conn.cursor()
    query = "insert into traffic values(?,?,?,?);"
    cur.executemany(query, data)
    con.commit()
    
    cur.execute('select * from traffic')
    out = cur.fetchall()
    
    for col in out:
        print(col)



# if __name__ == "__main__" :

#     playbook = "network_info.yaml"
#     hosts_file = "../../edge-hosts.ini"
#     conn = sqlite3.connect('../edge_logs.db3')

#     get_traffic_json(playbook, hosts_file, conn)