import sqlite3

import os
import re
from datetime import datetime

import schedule
import time

import warnings

warnings.filterwarnings(action='ignore')



## getting temperature data from Edge nodes

## define data output function
def get_temp_data(hosts_file, conn):
    ## write file
    os.system('ansible user -i {hosts_file} -m command -a "cat /sys/devices/virtual/thermal/thermal_zone0/temp" > tmp/templog.txt'.format(hosts_file=hosts_file))

    ## data processing
    file = open('tmp/templog.txt', 'r')
    line = file.readline()
    p = re.compile('rpi[\d]+')
    data = []

    while line:

        if p.match(line):
            # gen list, save node name
            tmp = p.findall(line)

            # save temperature data
            line = file.readline()
            line = int(line)
            line = round(line / 1000, 2)
            line = str(line)
            tmp.append(line.strip())

            ## save as float, unix timestamp
            now = round(time.time())

            ## save as string, datetime
            # now = datetime.now()
            
            tmp.insert(0, now)
            print(tmp)

            # manipulate data type for db.log
            tmp = tuple(tmp)
            data.append(tmp)
        
        line = file.readline()

    # show data shape
    # print(data)

    ## db manipulation
    con = conn
    cur = con.cursor()
    query = "insert into time_temp values(?,?,?);"
    cur.executemany(query, data)
    con.commit()

    cur.execute('select * from time_temp')
    # data = cur.fetchall()

    # for col in data:
    #     print(col)



# if __name__ == '__main__':

#     conn = sqlite3.connect('../edge_logs.db3')
#     get_temp_data('../../hosts.ini', conn)