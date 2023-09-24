import os
import yaml
import re
from device_info import set_model4infer

from collections import OrderedDict
from redis_connector import redis_connector
rcon = redis_connector()


class JobAllocator():
    def __init__(self):
        pass
    
    def job_allocator(self):
        get_device_ministat()
        get_cluster_list()
    
                
        hostname = socket.gethostname()
    
        if mode == 'getinfo':
            pass
        else:
            rcon.set_data(f'vnv:edge:{mode}:{hostname}:done_frames', cnt)
        