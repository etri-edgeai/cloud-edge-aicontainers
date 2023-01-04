import sqlite3

import os
import re

import schedule
import time

import warnings

warnings.filterwarnings(action='ignore')


def get_cpurat_data():
    ## write temporary log file
    os.system("ansible-playbook sysinfo.yaml > syslog.txt")

    ## regexs
    p_start = re.compile('TASK \[cpu usage].+')
    p_end = re.compile('PLAY RECAP.+')

    ## read file
    with open('syslog.txt', 'r') as f:
        lines = f.readlines()

        ## search task start line
        for line in lines:
            start = p_start.search(str(line))

            ## save index of string data
            if start:
                idx = lines.index(line)
                run = True
                i = 0
                rows = []

                while run:
                    ## drop no-useful strings and characters
                    lines[idx+i] = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s\.]", "", lines[idx+i])
                    lines[idx+i] = re.sub("\n", "", lines[idx+i])

                    rows.append(lines[idx+i])
                    ## search end of task
                    end = p_end.search(lines[idx+i])

                    i += 1

                    if end:
                        run = False

    ## drop null data in lists
    rows = [v for v in rows if v]

    ## drop spaces
    for row in rows:
        rows[rows.index(row)] = row.strip()

    data = []
    nodes = []

    ## load current nodes info from hosts table
    con = sqlite3.connect('../nodes.db3')
    cur = con.cursor()
    cur.execute('select name from nodes where type = "users"')
    tmp = cur.fetchall()

    ## save node lists
    for node in tmp:
        node = list(node)
        node = str(node)
        node = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", node)
        nodes.append(node)

    ## save cpu-ratio data part
    for node in nodes:
        for row in rows:
            if node in row:
                idx = rows.index(row)
                idx += 1

                if "msg" in rows[idx]:
                    data.append(rows[idx])


    now = round(time.time())
    log = []

    ## save and arrange data before inserting into DB
    for i in range(len(nodes)):
        tmp = []
        tmp.append(nodes[i])
        tmp.append(data[i])
        tmp.append(now)
        tmp = tuple(tmp)
        log.append(tmp)

    ## insert data into DB
    con = sqlite3.connect('../nodes.db3')
    cur = con.cursor()
    query = "insert into sysinfo values(?,?,?);"
    cur.executemany(query, log)
    con.commit()

    ## show result
    cur.execute('select * from sysinfo')
    out = cur.fetchall()

    for col in out:
        print(col)
    
    con.close()

## scheduling
if __name__ == '__main__':

    ## make scheduler
    schedule.every(5).seconds.do(get_cpurat_data)

    while True:
        schedule.run_pending()
        time.sleep(1)
