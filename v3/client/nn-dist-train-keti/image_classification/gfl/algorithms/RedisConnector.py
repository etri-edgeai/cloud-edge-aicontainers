#--------------------------------------
# Configurations
#--------------------------------------
# RedisHost = 'evc.re.kr'
# RedisPort = '20079'
RedisHost = 'localhost'
RedisPort = '6379'

#--------------------------------------
# Class
#--------------------------------------
import redis
import torch
from collections import OrderedDict
import pickle

class RedisConnector:
    
    def __init__(self):
        self.redis_client = redis.StrictRedis(
            host = RedisHost, 
            port = RedisPort, 
            db = 0 )
 
    def set_ordered_dict(self, key, ordered_dict_model):
        print(f'[d] key = {key}')
        self.redis_client.set(key, pickle.dumps(ordered_dict_model))
    
    def get_ordered_dict(self, key):
        print(f'[d] key = {key}')
        od = pickle.loads(self.redis_client.get(key))
        return od

    def set_data(self, key, data):
        print(f'[d] key = {key}')
        self.redis_client.set(key, data)
        
    def get_data(self, key):
        print(f'[d] key = {key}')
        return self.redis_client.get(key)
