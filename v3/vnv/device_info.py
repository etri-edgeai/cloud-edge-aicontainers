import torch
import socket
import platform, psutil

from collections import OrderedDict
from redis_connector import redis_connector
rcon = redis_connector()

def get_cluster_list():
    device_info = rcon.hgetall(f'vnv:edge:info')
    return device_info

def set_device_info(od):
    hostname = socket.gethostname()
    rcon.hmset(f'vnv:edge:info:{hostname}', od)

def get_device_info():
    hostname = socket.gethostname()
    device_info = rcon.hgetall(f'vnv:edge:info:{hostname}')
    return device_info

def get_device_ministat(hostnames):
    hostname = socket.gethostname()

    model_names = ['mobilenet_v3_small',
                       'mobilenet_v3_large',
                       'resnet18',
                       'resnet34',
                       'resnet50',
                       'resnet101',
                       'resnet152',
                       'nvidia_efficientnet_b0',
                       'nvidia_efficientnet_b4',
                       'nvidia_efficientnet_widese_b0',
                       'nvidia_efficientnet_widese_b4',
                  ]
                       
    for hostname in hostnames:
        for model_name in model_names:
            od = rcon.hgetall(f'vnv:edge:ministat:{hostname}:{model_name}')
            print(od)
        
        

def set_model4infer(model4infer = 'mobilenet_v3_small'):
    hostname = socket.gethostname()
    
    od = get_device_info()
    od['model4infer'] = model4infer
    rcon.hmset(f'vnv:edge:info:{hostname}', od)

def get_model4infer():
    hostname = socket.gethostname()
    od = get_device_info()
    print('od = ', od)
    return
    #return od['model4infer']

import sys
if __name__ == "__main__":
    hostname = socket.gethostname()
    is_cuda_available = torch.cuda.is_available()
    if is_cuda_available:
        num_of_cuda_devices = torch.cuda.device_count()
    else:
        num_of_cuda_devices = 0
    
    od = OrderedDict({
        'hostname':hostname,
        'is_cuda_available':str(is_cuda_available),
        'num_of_cuda_devices':str(num_of_cuda_devices),
        'platform':platform.system(),
        'arch':platform.machine(),
        'cpu':platform.processor(),
        'ram_gb':str(round(psutil.virtual_memory().total / (1024.0 **3))),
        'ip_address':socket.gethostbyname(socket.gethostname()),
    })
    set_device_info(od)

#------------------------------------------------------
# End of this file
#------------------------------------------------------



    
'''
    # for ubuntu
    cmd = f'ansible vnv -m shell -a "cat /proc/cpuinfo" -i ./config/hosts.ini > ./tmp/baseline_cpuinfo.txt'
    run(cmd, True)

    cmd = f'cat ./tmp/baseline_cpuinfo.txt | grep "model name" '
    cpu_model = run(cmd, True)
    print(f'cpu_model = {cpu_model}')

    cmd = f'ansible vnv -m shell -a "cat /proc/meminfo" -i ./config/hosts.ini > ./tmp/baseline_meminfo.txt '
    run(cmd, False)

    cmd = f'cat ./tmp/baseline_meminfo.txt | grep "MemTotal" '
    mem_total = run(cmd, True)
    print(f'mem_total = {mem_total}')
'''
