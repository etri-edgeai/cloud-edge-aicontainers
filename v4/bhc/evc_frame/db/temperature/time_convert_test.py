import sqlite3
import datetime

con = sqlite3.connect('nodes.db3')
cur = con.cursor()

cur.execute('select * from temp')
test = cur.fetchall()

# test[0] = list(test[0])
# test[0][0] = str(test[0][0])
# test[0][0] = datetime.datetime.strptime(test[0][0], '%Y-%m-%d %H:%M:%S').timestamp()
# test[0] = tuple(test[0])
# print(test[0])

new_data = []

for data in test:
    data = list(data)
    data[0] = str(data[0])
    data[0] = datetime.datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S').timestamp()
    data = tuple(data)
    new_data.append(data)

for row in new_data:
    print(row)

print(len(new_data))
print(type(new_data))

## db manipulation
query = "insert into temp_convrt values(?,?,?);"
cur.executemany(query, new_data)
con.commit()

# test = str(test[0])
# print(test)
# print(type(test))
# unixtime = datetime.datetime.strptime(test, '%Y-%m-%d %H:%M:%S').timestamp()
# print(unixtime)


# cnt = 0
# for row in cur:
#     print(row)
#     cnt += 1

# print(cnt)

