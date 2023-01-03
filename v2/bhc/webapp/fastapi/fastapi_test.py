import sqlite3


from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/a")
def read_root():
    con = sqlite3.connect('./nodes.db3')
    cur = con.cursor()

    cur.execute('select * from temp_convrt')
    test = cur.fetchall()

    rtn = {'log' : []}

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
    return rtn

@app.get("/f/{field}")
def read_root(field):
    con = sqlite3.connect('./nodes.db3')
    cur = con.cursor()

    cur.execute('select * from temp_convrt')
    test = cur.fetchall()

    rtn = {}
    for data in test:
        data = list(data)
        if not data[1] in rtn :
            rtn[data[1]] = []
        rtn[data[1]].append([data[0], data[2]])
    return rtn[field]

