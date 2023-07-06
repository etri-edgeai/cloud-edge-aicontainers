## ================= getting temperature datas from systeminfo ================== ##

import sqlite3
import platform
import os
import re
from datetime import datetime


## get temp
if platform.system() == 'Windows':
    stream = os.popen(
        'wmic /namespace:\\\\root\wmi PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature'
    )
    output = stream.read()
    p = re.compile('[0-9]+')
    output = p.findall(output)
    output = output[1]
    output = int(output)
    output = round(output / 10 - 273.15, 2)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('{now} 현재 온도 : {output}℃ 입니다.'.format(now=now, output=output))

elif platform.system() == 'Linux':
    os.system('ls')



## make new data
data = []
tmp = []
node = 'bhc'
tmp.append(now)
tmp.append(node)
tmp.append(output)
tmp = tuple(tmp)
data.append(tmp)

## db manipulation
con = sqlite3.connect('nodes.db3')
cur = con.cursor()
query = "insert into temp values(?,?,?);"

cur.executemany(query, data)
con.commit()

cur.execute('select * from temp')
print(cur.fetchall())
con.close()