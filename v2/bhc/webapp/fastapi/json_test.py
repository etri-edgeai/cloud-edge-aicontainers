import sqlite3
import json

rtn = {
    'log' : [

    ]
}

con = sqlite3.connect('./nodes.db3')
cur = con.cursor()
cur.execute('select * from temp_convrt')
test = cur.fetchall()

idx = 0

for row in test:
    row = list(row)

    if idx != 0:

        if row[0] == rtn['log'][idx-1]['time']:
            rtn['log'][idx-1]['data'].append({
                'node': row[1],
                'temperature' : row[2]
            })

        elif row[0] != rtn['log'][idx-1]['time']:
            rtn['log'].append({
            'time' : row[0],
            'data' : [{
                'node': row[1],
                'temperature' : row[2]
            }]
        })
            idx += 1

    else:
        rtn['log'].append({
            'time' : row[0],
            'data' : [{
                'node': row[1],
                'temperature' : row[2]
            }]
        })
        idx += 1

print(json.dumps(rtn, indent=2))
print()
print('데이터 갯수 : {len_log} 건'.format(len_log=len(rtn['log'])))

