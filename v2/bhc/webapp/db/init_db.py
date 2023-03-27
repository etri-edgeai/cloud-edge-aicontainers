import sqlite3
from sqlite3 import Error



def create_db(db_file):

    conn = None

    try:
        conn = sqlite3.connect(db_file)
        return conn
    
    except Error as e:
        print(e)

    return conn


def create_table(conn, table_query):

    try:
        c = conn.cursor()
        c.execute(table_query)
    
    except Error as e:
        print(e)


def main(file_path):

    database = file_path

    nodes_table = """ CREATE TABLE IF NOT EXISTS nodes (
                    time NOT NULL,
                    affiliation text NOT NULL,
                    name text PRIMARY KEY,
                    ip text NOT NULL,
                    port text NOT NULL,
                    type text NOT NULL,
                    owner text NOT NULL,
                    hw text,
                    os text,
                    gpu text
                );"""

    location_table = """ CREATE TABLE IF NOT EXISTS location (
                        name text NOT NULL,
                        address text NOT NULL,
                        latitude real NOT NULL,
                        longitude real NOT NULL
                    );"""

    time_temp_table = """ CREATE TABLE IF NOT EXISTS time_temp (
                        time NOT NULL,
                        name text NOT NULL,
                        temperature NOT NULL
                    )"""

    cpuinfo_table = """ CREATE TABLE IF NOT EXISTS cpuinfo (
                        time NOT NULL,
                        name text NOT NULL,
                        cpuratio real NOT NULL
                    );"""

    strginfo_table = """ CREATE TABLE IF NOT EXISTS strginfo (
                        time NOT NULL,
                        name text NOT NULL,
                        inuse real NOT NULL,
                        capacity real NOT NULL
                    );"""

    meminfo_table = """ CREATE TABLE IF NOT EXISTS meminfo (
                        time NOT NULL,
                        name text NOT NULL,
                        memratio real NOT NULL
                    );"""

    modelpred_table = """ CREATE TABLE IF NOT EXISTS modelpred (
                        time NOT NULL,
                        name text NOT NULL,
                        class text NOT NULL,
                        probability real NOT NULL
                    );"""

    traffic_table = """ CREATE TABLE IF NOT EXISTS traffic (
                        time NOT NULL,
                        name text NOT NULL,
                        rx_bps real NOT NULL,
                        tx_bps real NOT NULL
                    );"""
    
    model_list_table = """ CREATE TABLE IF NOT EXISTS model_list (
                        name text NOT NULL,
                        tag text NOT NULL
                    );"""

    model_desc_table = """ CREATE TABLE IF NOT EXISTS model_desc (
                        node text NOT NULL,
                        tag text NOT NULL,
                        desc text NOT NULL
                    );"""

    dstrb_progress_table = """ CREATE TABLE IF NOT EXISTS dstrb_progress (
                        time NOT NULL,
                        name text NOT NULL,
                        status text NOT NULL
                    );"""
    
    input_image_table = """ CREATE TABLE IF NOT EXISTS input_image (
                        time NOT NULL,
                        name_node text NOT NULL,
                        name_img text PRIMARY KEY
                    );"""

    modelinfo_detail_table = """ CREATE TABLE IF NOT EXISTS modelinfo_detail (
                        time NOT NULL,
                        owner_name text NOT NULL,
                        model_name text NOT NULL,
                        size_GB real NOT NULL,
                        task text NOT NULL,
                        version text NOT NULL
                    );"""

    conn = create_db(database)

    if conn is not None:
        create_table(conn, nodes_table)
        create_table(conn, location_table)
        create_table(conn, time_temp_table)
        create_table(conn, cpuinfo_table)
        create_table(conn, strginfo_table)
        create_table(conn, meminfo_table)
        create_table(conn, modelpred_table)
        create_table(conn, traffic_table)
        create_table(conn, model_list_table)
        create_table(conn, model_desc_table)
        create_table(conn, dstrb_progress_table)
        create_table(conn, input_image_table)
        create_table(conn, modelinfo_detail_table)
    
    else:
        print("Cannot connect database.")




if __name__ == "__main__":

    main('edge_logs.db3')



