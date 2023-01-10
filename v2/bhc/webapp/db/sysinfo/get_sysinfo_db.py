import sqlite3

import os
import re

import schedule
import time

import warnings

warnings.filterwarnings(action='ignore')


def get_cpurat_data():
    ## write temporary log file
    os.system("ansible-playbook sysinfo.yaml -i ../../edge-hosts.ini -t cpu > syslog.txt")

    ## regexs
    rows = []
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

    nodes = []
    data = []

    ## load current nodes info from hosts table
    con = sqlite3.connect('../nodes.db3')
    cur = con.cursor()
    cur.execute('select name from nodes where type = "user"')
    tmp = cur.fetchall()

    ## save node lists
    for node in tmp:
        node = list(node)
        node = str(node)
        node = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", node)
        nodes.append(node)

    ## save cpu-ratio data
    for node in nodes:
        for row in rows:
            if node in row:
                idx = rows.index(row)
                idx += 1

                if "msg" in rows[idx]:
                    rows[idx] = re.sub(r"[a-zA-Z\s]", "", rows[idx])
                    data.append(rows[idx])

    ## save time
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
    query = "insert into cpuinfo values(?,?,?);"
    cur.executemany(query, log)
    con.commit()

    ## show result
    cur.execute('select * from cpuinfo')
    out = cur.fetchall()

    for col in out:
        print(col)
    
    con.close()




def get_storage_data():
    ## write log file
    # os.system("ansible-playbook sysinfo.yaml -t storage1 > syslog.txt")

    # ## regexs
    # p_start = re.compile('TASK \[storage total].+')
    # p_end = re.compile('PLAY RECAP.+')

    # ## read file
    # with open('syslog.txt', 'r') as f:
    #     lines = f.readlines()

    #     ## search task start line
    #     for line in lines:
    #         start = p_start.search(str(line))

    #         ## save index of string data
    #         if start:
    #             idx = lines.index(line)
    #             run = True
    #             i = 0
    #             rows_total = []

    #             while run:
    #                 ## drop no-useful strings and characters
    #                 lines[idx+i] = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s\.]", "", lines[idx+i])
    #                 lines[idx+i] = re.sub("\n", "", lines[idx+i])

    #                 rows_total.append(lines[idx+i])
    #                 ## search end of task
    #                 end = p_end.search(lines[idx+i])

    #                 i += 1

    #                 if end:
    #                     run = False
    ## write log file
    os.system("ansible-playbook sysinfo.yaml -i ../../edge-hosts.ini -t storage2 > syslog.txt")

    ## regexs & var
    rows_inuse = []
    p_start = re.compile('TASK \[storage inuse].+')
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

                while run:
                    ## drop no-useful strings and characters
                    lines[idx+i] = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s\.]", "", lines[idx+i])
                    lines[idx+i] = re.sub("\n", "", lines[idx+i])

                    rows_inuse.append(lines[idx+i])
                    ## search end of task
                    end = p_end.search(lines[idx+i])

                    i += 1

                    if end:
                        run = False
    ## write log file
    os.system("ansible-playbook sysinfo.yaml -i ../../edge-hosts.ini -t storage3 > syslog.txt")

    ## regexs & var
    rows_cap = []
    p_start = re.compile('TASK \[storage capacity].+')
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

                while run:
                    ## drop no-useful strings and characters
                    lines[idx+i] = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s\.]", "", lines[idx+i])
                    lines[idx+i] = re.sub("\n", "", lines[idx+i])

                    rows_cap.append(lines[idx+i])
                    ## search end of task
                    end = p_end.search(lines[idx+i])

                    i += 1

                    if end:
                        run = False
                        
    ## drop null
    # rows_total = [v for v in rows_total if v]
    rows_inuse = [v for v in rows_inuse if v]
    rows_cap = [v for v in rows_cap if v]

    ## drop spaces
    # for row in rows_total:
    #     rows_total[rows_total.index(row)] = row.strip()
    for row in rows_inuse:
        rows_inuse[rows_inuse.index(row)] = row.strip()
    for row in rows_cap:
        rows_cap[rows_cap.index(row)] = row.strip()

    nodes = []
    # data_total = []
    data_inuse = []
    data_cap = []
    
    ## load current nodes info from hosts table
    con = sqlite3.connect('../nodes.db3')
    cur = con.cursor()
    cur.execute('select name from nodes where type = "user"')
    tmp = cur.fetchall()

    ## save node lists
    for node in tmp:
        node = list(node)
        node = str(node)
        node = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", node)
        nodes.append(node)

    ## save storage capacity data
    # for node in nodes:
    #     for row in rows_total:
    #         if node in row:
    #             idx = rows_total.index(row)
    #             idx += 1

    #             if "msg" in rows_total[idx]:
    #                 rows_total[idx] = re.sub(r"[a-zA-Z\s]", "", rows_total[idx])
    #                 data_total.append(rows_total[idx])
    for node in nodes:
        for row in rows_inuse:
            if node in row:
                idx = rows_inuse.index(row)
                idx += 1

                if "msg" in rows_inuse[idx]:
                    rows_inuse[idx] = re.sub(r"[a-zA-Z\s]", "", rows_inuse[idx])
                    data_inuse.append(rows_inuse[idx])
    for node in nodes:
        for row in rows_cap:
            if node in row:
                idx = rows_cap.index(row)
                idx += 1

                if "msg" in rows_cap[idx]:
                    rows_cap[idx] = re.sub(r"[a-zA-Z\s]", "", rows_cap[idx])
                    data_cap.append(rows_cap[idx])

    ## save time
    now = round(time.time())
    log = []


    ## save and arrange data before inserting into DB
    for i in range(len(nodes)):
        tmp = []
        tmp.append(now)
        tmp.append(nodes[i])
        # tmp.append(data_total[i])
        tmp.append(data_inuse[i])
        tmp.append(data_cap[i])
        tmp = tuple(tmp)
        log.append(tmp)


    ## insert data into DB
    con = sqlite3.connect('../nodes.db3')
    cur = con.cursor()
    query = "insert into strginfo values(?,?,?,?);"
    cur.executemany(query, log)
    con.commit()

    ## show result
    cur.execute('select * from strginfo')
    out = cur.fetchall()

    for col in out:
        print(col)
    
    con.close()





## scheduling
if __name__ == '__main__':

    ## make scheduler
    schedule.every(5).seconds.do(get_cpurat_data)
    schedule.every(5).seconds.do(get_storage_data)

    while True:
        schedule.run_pending()
        time.sleep(1)
