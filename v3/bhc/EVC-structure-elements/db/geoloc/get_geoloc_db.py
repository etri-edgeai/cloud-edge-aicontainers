import sqlite3

import os
import re

import schedule
import time

from geopy.geocoders import Nominatim

import warnings

warnings.filterwarnings(action='ignore')


def get_geo_data(conn):
    con = conn
    cur = con.cursor()
    cur.execute("select name from nodes where type = 'user';")
    nodes = []

    for node in cur.fetchall():
        node = list(node)
        nodes.append(node)

    add1 = '월드컵북로54길 11'
    add2 = '부천시 삼정동 283-1'
    add3 = '강원도 원주시 북원로 2852'
    add4 = '경상북도 청송군 주왕산면 지리 180-4'
    add5 = '여수시 중앙동 246-1'

    nodes[0].append(add1)
    nodes[1].append(add2)
    nodes[2].append(add3)
    nodes[3].append(add4)
    nodes[4].append(add5)

    print(nodes)
    print(len(nodes))
    
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)

    data = []

    for i in range(len(nodes)):
        geo = geolocoder.geocode(nodes[i][1])
        print(geo)
        crd = {"lat": geo.latitude, "lng": geo.longitude}
        nodes[i].append(crd['lat'])
        nodes[i].append(crd['lng'])
        nodes[i] = tuple(nodes[i])
        data.append(nodes[i])

    print(data)

    query = 'insert into location values(?,?,?,?);'
    cur.execute('delete from location;')
    cur.executemany(query, data)
    con.commit()

    cur.execute('select * from location')
    cols = cur.fetchall()

    for col in cols:
        print(col)

# if __name__ == '__main__':

#     get_geo_data()