import os
import yaml
import re
from device_info import *

from collections import OrderedDict
from redis_connector import redis_connector
rcon = redis_connector()


class job_allocator():
    def __init__(self):
        pass
    
    def set_job(self):
        hostnames = ['n01', 
                     'n02', 
                     'rpi6431', 
                     'rpi6432',
                     'rpi6433', 
                     'rpi6434',
                     'rpi6435', 
                     'txp',
                    ]
                     
        get_device_ministat(hostnames)
        #get_cluster_list()

        hostname = socket.gethostname()
        
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:start_frame', 0)
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:end_frame', 100)
    
    def get_job(self, hostname):
        start_frame = rcon.set_data(f'vnv:edge:advanced:job:{hostname}:start_frame', 0)
        end_frame = rcon.set_data(f'vnv:edge:advanced:job:{hostname}:start_frame', 0)
        return start_frame, end_frame
    