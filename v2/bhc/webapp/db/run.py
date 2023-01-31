import sqlite3
from sqlite3 import Error
from sysinfo import get_sysinfo_db as sys
from geoloc import get_geoloc_db as geo
from hosts import hosts 
from temperature import get_temp_db as temp
from model import test_runmodel as pred
from network import get_network_db as ntw
import init_db

import schedule
import time


def connect_db(db_file):

    conn = None

    try:
        conn = sqlite3.connect(db_file)
        return conn
    
    except Error as e:
        print(e)

    return conn


## scheduling
def get_system_informations(playbook, hosts_file, conn):

    hosts.get_hosts(hosts_file, conn)
    geo.get_geo_data(conn)

    ## make scheduler
    schedule.every(5).seconds.do(
        sys.get_cpurat_data,
        playbook=playbook,
        hosts_file=hosts_file,
        conn=conn
    )
    schedule.every(5).seconds.do(
        sys.get_storage_data,
        playbook=playbook,
        hosts_file=hosts_file,
        conn=conn
    )
    schedule.every(5).seconds.do(
        sys.get_mem_data,
        playbook=playbook,
        hosts_file=hosts_file,
        conn=conn
    )
    schedule.every(5).seconds.do(
        temp.get_temp_data,
        hosts_file=hosts_file,
        conn=conn
    )

    schedule.every(30).seconds.do(
        pred.get_pred,
        playbook=playbook,
        hosts_file=hosts_file,
        conn=conn
    )

    schedule.every(5).seconds.do(
        ntw.get_traffic_json,
        playbook=playbook,
        hosts_file=hosts_file,
        conn=conn
    )

    while True:
        schedule.run_pending()
        time.sleep(1)



def main():

    db_path = 'edge_logs.db3'

    init_db.main(db_path)
    conn = connect_db(db_path)
    hosts_file_path = '../edge-hosts.ini'
    playbook_path = 'run_playbook.yaml'

    get_system_informations(playbook_path, hosts_file_path, conn)



if __name__ == '__main__':

    main()