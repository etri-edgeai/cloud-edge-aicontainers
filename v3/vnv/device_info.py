import torch
import socket
import platform, psutil

from collections import OrderedDict
from redis_connector import redis_connector
rcon = redis_connector()

def set_device_info(od):
    hostname = socket.gethostname()
    rcon.hmset(f'vnv:edge:info:{hostname}', od)

def get_device_info():
    hostname = socket.gethostname()
    device_info = rcon.hgetall(f'vnv:edge:info:{hostname}')
    return device_info

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
