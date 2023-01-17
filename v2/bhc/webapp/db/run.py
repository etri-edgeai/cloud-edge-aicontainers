from sysinfo import get_sysinfo_db as sys
from geoloc import get_geoloc_db as geo
from hosts import hosts 
from temperature import get_temp_db as temp
from model_preds import test_runmodel

import schedule
import time


## scheduling
def get_system_informations():

    hosts.get_hosts()
    geo.get_geo_data()

    ## make scheduler
    schedule.every(5).seconds.do(sys.get_cpurat_data)
    schedule.every(5).seconds.do(sys.get_storage_data)
    schedule.every(5).seconds.do(sys.get_mem_data)
    schedule.every(5).seconds.do(temp.get_temp_data)

    while True:
        schedule.run_pending()
        time.sleep(1)


def get_prediction():

    test_runmodel()



if __name__ == '__main__':

    get_system_informations()
