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
        hostnames = ['txp',
                     'n01', 
                     'n02', 
                     'rpi6431', 
                     'rpi6432',
                     'rpi6433', 
                     'rpi6434',
                     'rpi6435', 
                    ]
                     
        ministat = get_device_ministat(hostnames)
        #get_cluster_list()

        #ministat[hostname]
        #current_hostname = socket.gethostname()
        
        hostname = 'txp'
        start_frame = 0
        end_frame = 150
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:start_frame', start_frame)
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:end_frame', end_frame)
        
        hostname = 'n01'
        start_frame = 150
        end_frame = 300
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:start_frame', start_frame)
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:end_frame', end_frame)
        
        hostname = 'n02'
        start_frame = 300
        end_frame = 450
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:start_frame', start_frame)
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:end_frame', end_frame)
        
        hostname = 'rpi6431'
        start_frame = 450
        end_frame = 460
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:start_frame', start_frame)
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:end_frame', end_frame)
        
        hostname = 'rpi6431'
        start_frame = 460
        end_frame = 470
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:start_frame', start_frame)
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:end_frame', end_frame)
        
        hostname = 'rpi6433'
        start_frame = 470
        end_frame = 480
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:start_frame', start_frame)
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:end_frame', end_frame)
        
        hostname = 'rpi6434'
        start_frame = 480
        end_frame = 490
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:start_frame', start_frame)
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:end_frame', end_frame)  

        hostname = 'rpi6435'
        start_frame = 490
        end_frame = 500
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:start_frame', start_frame)
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:end_frame', end_frame)  
        
    def get_job(self, hostname):
        start_frame = int(rcon.get_data(f'vnv:edge:advanced:job:{hostname}:start_frame'))
        end_frame = int(rcon.get_data(f'vnv:edge:advanced:job:{hostname}:end_frame'))
        return start_frame, end_frame
    