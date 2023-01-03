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
def get_temp_data():
    ## write file
    os.system('ansible users -m command -a "cat /sys/devices/virtual/thermal/thermal_zone0/temp" > templog.txt')

    ## data processing
    file = open('templog.txt', 'r')
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

            # save datetime
            # now = datetime.now() # .strftime('%Y-%m-%d %H:%M:%S')
            # tmp.insert(0, now)

            # manipulate data type for db.log
            tmp = tuple(tmp)
            data.append(tmp)
        
        line = file.readline()

    # show data shape
    # print(data)

    ## db manipulation
    con = sqlite3.connect('nodes.db3')
    cur = con.cursor()
    query = "insert into temp values(datetime('now'),?,?);"
    cur.executemany(query, data)
    con.commit()

    cur.execute('select * from temp')
    data = cur.fetchall()

    for col in data:
        print(col)

    con.close()


if __name__ == '__main__':

    ## make scheduler
    schedule.every(5).seconds.do(get_temp_data)

    while True:
        schedule.run_pending()
        time.sleep(1)