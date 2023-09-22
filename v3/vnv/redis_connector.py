#--------------------------------------
# Configurations
#--------------------------------------
RedisHost = 'evc.re.kr'
RedisPort = '20079'
# RedisHost = 'localhost'
# RedisPort = '6379'

#--------------------------------------
# Class
#--------------------------------------
import redis
import torch
from collections import OrderedDict
import pickle

class redis_connector:
    
    def __init__(self):
        self.redis_client = redis.StrictRedis(
            host = RedisHost, 
            port = RedisPort, 
            db = 0 )

    #----------------------------------------------------
    # 문자, 숫자와 같은 단순한 {key, value} 데이터를 쓰고(set), 읽습니다(get).
    #----------------------------------------------------
    def set_data(self, key, data):
        print(f'[d] key = {key}')
        self.redis_client.set(key, data)
        
    def get_data(self, key):
        print(f'[d] key = {key}')
        return self.redis_client.get(key)

    #----------------------------------------------------
    # OrderedDict 타입의 모델 정보를 쓰고(set), 읽습니다(get).
    #----------------------------------------------------
    def set_ordered_dict(self, key, ordered_dict_model):
        print(f'[d] key = {key}')
        self.redis_client.set(key, pickle.dumps(ordered_dict_model))
    
    def get_ordered_dict(self, key):
        print(f'[d] key = {key}')
        od = pickle.loads(self.redis_client.get(key))
        return od

    #----------------------------------------------------
    # Optimizer 정보를 쓰고(set), 읽습니다(get).
    #----------------------------------------------------
    def set_optimizer(self, key, optimizer):
        print(f'[d] key = {key}')
        
        opt = {
            'optimizer_state_dict': optimizer.state_dict(),
            'optimizer_architecture': optimizer
        }
        self.redis_client.set(key, pickle.dumps(opt))
    
    def get_optimizer(self, key):
        print(f'[d] key = {key}')
                
        loaded_data = pickle.loads(self.redis_client.get(key))
        
        # 옵티마이저 복원
        loaded_optimizer = loaded_data['optimizer_architecture']
        loaded_optimizer.load_state_dict(loaded_data['optimizer_state_dict'])

        return loaded_optimizer