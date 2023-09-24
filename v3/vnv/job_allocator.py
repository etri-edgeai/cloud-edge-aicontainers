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
        
        '''
        hostname = 'txp'
        start_frame = 0
        end_frame = 10000
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:start_frame', start_frame)
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:end_frame', end_frame)
        '''
        
        hostname = 'n01'
        start_frame = 0
        end_frame = 24500
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:start_frame', start_frame)
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:end_frame', end_frame)
        
        hostname = 'n02'
        start_frame = 24500
        end_frame = 49000
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:start_frame', start_frame)
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:end_frame', end_frame)
        
        hostname = 'rpi6431'
        start_frame = 49000
        end_frame = 49300
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:start_frame', start_frame)
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:end_frame', end_frame)
        
        hostname = 'rpi6432'
        start_frame = 49300
        end_frame = 49700
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:start_frame', start_frame)
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:end_frame', end_frame)
        
        hostname = 'rpi6433'
        start_frame = 49700
        end_frame = 50000
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:start_frame', start_frame)
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:end_frame', end_frame)
        
        '''
        hostname = 'rpi6434'
        start_frame = 49600
        end_frame = 49800
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:start_frame', start_frame)
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:end_frame', end_frame)  

        hostname = 'rpi6435'
        start_frame = 49800
        end_frame = 50000
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:start_frame', start_frame)
        rcon.set_data(f'vnv:edge:advanced:job:{hostname}:end_frame', end_frame)  
        '''
        
        
        
    def get_job(self, hostname):
        start_frame = int(rcon.get_data(f'vnv:edge:advanced:job:{hostname}:start_frame'))
        end_frame = int(rcon.get_data(f'vnv:edge:advanced:job:{hostname}:end_frame'))
        return start_frame, end_frame
    