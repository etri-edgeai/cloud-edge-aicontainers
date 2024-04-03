import sqlite3

import os
import re

import schedule
import time

import warnings

warnings.filterwarnings(action='ignore')


def get_cpurat_data(playbook, hosts_file, conn):
    ## write temporary log file
    os.system("ansible-playbook -i {hosts_file} -t cpu {playbook} > tmp/syslog.txt".format(playbook=playbook, hosts_file=hosts_file))

    ## regexs
    rows = []
    p_start = re.compile('TASK \[cpu usage].+')
    p_end = re.compile('PLAY RECAP.+')

    ## read file
    with open('tmp/syslog.txt', 'r') as f:
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

    # print(rows)

    ## load current nodes info from hosts table
    con = conn
    cur = con.cursor()
    cur.execute('select name from nodes where affiliation != "builder";')
    tmp = cur.fetchall()

    ## save node lists
    for node in tmp:
        node = list(node)
        node = str(node)
        node = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", node)
        nodes.append(node)

    # print(nodes)

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
        tmp.append(now)
        tmp.append(nodes[i])
        tmp.append(data[i])
        tmp = tuple(tmp)
        log.append(tmp)

    print(log)

    ## insert data into DB
    con = conn
    cur = con.cursor()
    query = "insert into cpuinfo values(?,?,?);"
    cur.executemany(query, log)
    con.commit()

    ## show result
    cur.execute('select * from cpuinfo')
    # out = cur.fetchall()

    # for col in out:
    #     print(col)




def get_storage_data(playbook, hosts_file, conn):
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


    # ============= storage inuse =============
    ## write log file
    os.system("ansible-playbook {playbook} -i {hosts_file} -t storage2 > tmp/syslog.txt".format(playbook=playbook, hosts_file=hosts_file))

    ## regexs & var
    rows_inuse = []
    p_start = re.compile('TASK \[storage inuse].+')
    p_end = re.compile('PLAY RECAP.+')

    ## read file
    with open('tmp/syslog.txt', 'r') as f:
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


    # ============ storage cap ================
    ## write log file
    os.system("ansible-playbook {playbook} -i {hosts_file} -t storage3 > tmp/syslog.txt".format(playbook=playbook, hosts_file=hosts_file))

    ## regexs & var
    rows_cap = []
    p_start = re.compile('TASK \[storage capacity].+')
    p_end = re.compile('PLAY RECAP.+')

    ## read file
    with open('tmp/syslog.txt', 'r') as f:
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
    con = conn
    cur = con.cursor()
    cur.execute('select name from nodes where affiliation != "builder"')
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

    print(log)

    ## insert data into DB
    con = conn
    cur = con.cursor()
    query = "insert into strginfo values(?,?,?,?);"
    cur.executemany(query, log)
    con.commit()

    # ## show result
    # cur.execute('select * from strginfo')
    # out = cur.fetchall()

    # for col in out:
    #     print(col)




def get_mem_data(playbook, hosts_file, conn):

    os.system("ansible-playbook {playbook} -i {hosts_file} -t mem > tmp/syslog.txt".format(playbook=playbook, hosts_file=hosts_file))

    rows = []
    p_start = re.compile('TASK \[memory usage].+')
    p_end = re.compile('PLAY RECAP.+')

    with open('tmp/syslog.txt', 'r') as f:

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
                    lines[idx+i] = re.sub(" +", " ", lines[idx+i])
                    lines[idx+i] = re.sub("\n", "", lines[idx+i])
                    lines[idx+i] = re.sub("changed.+", "", lines[idx+i])

                    rows.append(lines[idx+i])
                    ## search end of task
                    end = p_end.search(lines[idx+i])

                    i += 1

                    if end:
                        run = False

    rows = [v for v in rows if v]

    for row in rows:
        rows[rows.index(row)] = row.strip()


    nodes = []

    con = conn
    cur = con.cursor()
    cur.execute('select name from nodes where affiliation != "builder"')
    tmp = cur.fetchall()

    for node in tmp:
        node = str(node)
        node = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", node)
        nodes.append(node)



    data = []

    p_total = re.compile('MemTotal \d+')
    # p_free = re.compile('MemFree \d+')
    p_aval = re.compile('MemAvailable \d+')

    for node in nodes:
            for row in rows:
                if node in row:
                    idx = rows.index(row)
                    idx += 1
                    
                    tmp = []
                    
                    if 'msg' in rows[idx]:
                        total = p_total.findall(rows[idx])
    #                     free = p_free.findall(rows[idx])
                        aval = p_aval.findall(rows[idx])
                        
                        total = re.sub(r"[^0-9]", "", str(total))
    #                     free = re.sub("[^0-9]", "", str(free))
                        aval = re.sub("[^0-9]", "", str(aval))
                        
                        tmp.append(total)
    #                     tmp.append(free)
                        tmp.append(aval)
                        
                        d = []
                        
                        for i in range(len(tmp)):
                            d.append(tmp[i])
                        
                        data.append(d)

    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = int(data[i][j])
            
    # print(type(data[0][0]))


    now = round(time.time())
    log = []

    for i in range(len(nodes)):
        tmp = []
        tmp.append(now)
        tmp.append(nodes[i])
        tmp.append(round(((data[i][0] - data[i][1]) / data[i][0]) * 100, 2))
        tmp = tuple(tmp)
        log.append(tmp)

    print(log)


    ## insert data into DB
    con = conn
    cur = con.cursor()
    query = "insert into meminfo values(?,?,?);"
    cur.executemany(query, log)
    con.commit()

    ## show result
    # cur.execute('select * from meminfo')
    # out = cur.fetchall()

    # for col in out:
    #     print(col)




# ## scheduling
if __name__ == '__main__':

    playbook = '../../playbooks/get_logs.yaml'
    inven = '../../hosts.ini'
    conn = sqlite3.connect('../edge_logs.db3')

    get_cpurat_data(playbook, inven, conn)
    get_storage_data(playbook, inven, conn)
    get_mem_data(playbook, inven, conn)
