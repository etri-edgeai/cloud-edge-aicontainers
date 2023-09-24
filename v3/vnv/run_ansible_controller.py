#------------------------------------------------------
# vnv 2023
#------------------------------------------------------

#!/bin/bash

# <ubuntu> 
# $ sudo apt install speedtest-cli

# <rpi> 
# $ sudo pip3 install speedtest-cli

import os
import yaml
import time
import socket
from collections import OrderedDict
from redis_connector import redis_connector

rcon = redis_connector()
wdir = ' /home/jpark/www/cloud-edge-aicontainers/v3/vnv/'
py = ' /home/jpark/www/cloud-edge-aicontainers/v3/vnv/venv/bin/python'
ask_pass_option = '' #  '--ask-become-pass'

from device_info import get_device_info, get_model4infer


#------------------------------------------------------
# run
#------------------------------------------------------
def run(cmd, is_show=False):
    # import subprocess
    # p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    # if(is_show):
    #     print(p.communicate())
    stream = os.popen(cmd)
    output = stream.read()

    if is_show:
        print( output )
        return output
    else:
        return None


def update_average_result():
    rcon.set_data('vnv:avg:baseline:top1', 0)
    rcon.set_data('vnv:avg:baseline:top5', 0)
    rcon.set_data('vnv:avg:baseline:latency', 0)
    rcon.set_data('vnv:avg:advanced:top1', 0)
    rcon.set_data('vnv:avg:advanced:top5', 0)
    rcon.set_data('vnv:avg:advanced:latency', 0)
    
def update_server_result(od):
    hostname = socket.gethostname()
    #rcon.set_ordered_dict(f'vnv:server:{hostname}', od)
    #print('output = ', rcon.get_ordered_dict(f'vnv:server:{hostname}'))
    rcon.hmset(f'vnv:server:{hostname}', od)
    print('output = ', rcon.hgetall(f'vnv:server:{hostname}'))


def main(mode = 'baseline'):
    
    #----------------------------------
    # 코드 업데이트
    #----------------------------------
    cmd = f'ansible vnv -i ./config/hosts.ini -m shell -a "cd {wdir}; git pull;"  {ask_pass_option} ' 
    print(cmd)
    run(cmd, True)
        
    cmd = f'ansible vnv -i ./config/hosts.ini -m shell -a "cd {wdir}; python3 -m venv venv; source venv/bin/activate; pip install -r requirements.txt;" -e "ansible_shell_executable=/bin/bash" {ask_pass_option} ' 
    print(cmd)
    run(cmd, True)
        

    #----------------------------------
    # 데이터셋 다운로드
    #----------------------------------
    dataset_root = './dataset'
    #cmd = f'ansible vnv -i ./config/hosts.ini -m shell -a "cd {wdir}; mkdir dataset; {py} download_imagenet_mini_dataset.py" -e "ansible_shell_executable=/bin/bash" {ask_pass_option} ' 
    #print(cmd)
    #run(cmd, True)
    
    
    #----------------------------------
    # 프로세스를 시작합니다.
    #----------------------------------
    st_total = time.time() #---------------------

    if mode == 'getinfo' or mode == 'baseline' or mode == 'advanced':
        print(f'[+] Start {mode} Mode')
    else:
        print(f'[-] error, there is no [{mode}] mode.')
        return

    #----------------------------------
    # 에지 디바이스의 기본 상태정보를 얻습니다.
    #----------------------------------
    st_getstatus = time.time() #---------------------

    cmd = f'ansible vnv -m shell -a "cd {wdir}; {py} device_info.py " -i ./config/hosts.ini '
    run(cmd, True)
    
    print( get_device_info() )

    #----------------------------------
    # 추론을 위한 테스트 영상을 준비합니다.
    #----------------------------------
    if mode == 'baseline' or mode == 'advanced':
        fpath_testimages = dataset_root + '/imagenet-val/'
    else:
        fpath_testimages = dataset_root + '/imagenet-mini-val/'
    print(f'fpath_testimages = {fpath_testimages}')

    
    #----------------------------------
    # 에지 디바이스의 추론 성능 정보를 얻고 종료합니다.
    #----------------------------------

    if mode == 'getinfo':
        cmd = f'ansible vnv -i ./config/hosts.ini -m shell -a "cd {wdir}; pwd; {py} inference4vnv.py --mode {mode} --fpath_testimages {fpath_testimages};"  {ask_pass_option} ' 
        print("\n", cmd, "\n")
        run(cmd, True)
        return


    et_getstatus = time.time() #---------------------

    
    
    
    if True:
        #----------------------------------
        # 에지 디바이스에서 추론을 수행합니다. 
        #----------------------------------
        st_inference = time.time() #---------------------

        cmd = f'ansible vnv -i ./config/hosts.ini -m shell -a "cd {wdir}; pwd; {py} inference4vnv.py --mode {mode} --fpath_testimages {fpath_testimages};"  {ask_pass_option} ' 
        print("\n", cmd, "\n")
        run(cmd, True)
            
        et_inference = time.time() #---------------------

        #---------------------------------------------------
        et_total = time.time()
        #---------------------------------------------------

        print( f'[d] workding dir = {wdir}' )
        print( f'[d] py = {py}' )

        T = et_total - st_total
        
        title1 = 'TimeOfGetStatus'
        t1 = et_getstatus - st_getstatus
        ratio = t1 / T
        disp_time(title1, t1, ratio)
 
        
        title3 = 'TimeOfInference'
        t3 = et_inference - st_inference
        ratio = t3 / T
        disp_time(title3, t3, ratio)
            
        title4 = 'TimeOfTotal'
        t4 = et_total - st_total
        ratio = t4 / T
        disp_time(title4, t4, ratio)

        od = OrderedDict({
            title1:t1,
            title2:t2,
            title3:t3,
            title4:t4
        })
        update_server_result(od)
        
        print(f'[+] Done {mode} experiment')

def disp_time(title, t, ratio):
    print(f'{t}, {ratio * 100} %, {title} ')


#------------------------------------------------------
# main
#------------------------------------------------------

import sys
if __name__ == "__main__":
    
    # total arguments
    n = len(sys.argv)
    for i in range(1, n):
        print(sys.argv[i], end = " ")

    if n != 2:
        print('[-] argument error')
        print('    e.g. python3 run_ansible_controller.py baseline')
        print('    e.g. python3 run_ansible_controller.py advanced')
    main(sys.argv[1])

#------------------------------------------------------
# End of this file
#------------------------------------------------------