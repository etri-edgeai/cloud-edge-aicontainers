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
from model_selector import ModelSelection
from collections import OrderedDict
from redis_connector import redis_connector
rcon = redis_connector()


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
    
def update_edge_result(od):
    rcon.set_ordered_dict('vnv:aaa', od)
    print('output = ', rcon.get_ordered_dict('vnv:aaa'))
    
    
    
def main(mode = 'baseline'):
    #----------------------------------
    # 프로세스를 시작합니다.
    #----------------------------------
    st_total = time.time() #---------------------

    if mode == 'baseline' or mode == 'advanced':
        print(f'[+] Start {mode} experiment')
    else:
        print(f'[-] error, there is no [{mode}] mode.')
        return

    #----------------------------------
    # 에지 디바이스의 상태정보를 얻습니다.
    #----------------------------------
    st_getstatus = time.time() #---------------------
    wdir = ' /home/jpark/www/cloud-edge-aicontainers/v3/vnv/'
    py = ' /home/jpark/www/cloud-edge-aicontainers/v3/vnv/venv/bin/python'
    
    #selected_model = 'resnet152' # default
    device = 'cuda'
    N = 0
    ask_pass_option = '' #  '--ask-become-pass'
    model_selector = ModelSelection()

    #cmd_sub = ' /usr/bin/python3 -c "import torch; print(torch.cuda.is_available())" '
    cmd = f'ansible vnv -m shell -a "cd {wdir}; {py} cuda_is_available.py " -i ./config/hosts.ini '
    z = run(cmd, True)

    if 'True' in z : is_cuda_available = 1 
    else: is_cuda_available = 0

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

    et_getstatus = time.time() #---------------------

    
    #----------------------------------
    # 추론을 위한 AI 모델을 선택합니다.
    #----------------------------------
    
    st_modelselection = time.time() #---------------------

    if mode == 'baseline':
        selected_model = model_selector.greedModelSelection()
    elif mode == 'advanced':
        selected_model = model_selector.advancedModelSelection(cfg=None)
    
    if True:
        print(f'mode = {mode}, selected_model = {selected_model}')
        et_modelselection = time.time() #---------------------

        #----------------------------------
        # 에지 디바이스에서 추론을 수행합니다. 
        #----------------------------------
        st_inference = time.time() #---------------------
        cmd = f'ansible vnv -i ./config/hosts.ini -m shell -a "cd {wdir}; pwd; {py} inference4vnv.py --model {selected_model} --device {device} --N {N};"  {ask_pass_option} ' 
        
        print(cmd)
        run(cmd, True)
        et_inference = time.time() #---------------------
        
        #---------------------------------------------------
        et_total = time.time()
        #---------------------------------------------------

        print( f'[d] workding dir = {wdir}' )
        print( f'[d] py = {py}' )
        print( f'[d] selected_model = {selected_model}' )

        od = OrderedDict()
        T = et_total - st_total
        
        title = 'Get status time'
        t = et_getstatus - st_getstatus
        ratio = t / T
        disp_time(title, t, ratio)
        od[title] = t
        
        title = 'Model selection time'
        t = et_modelselection - st_modelselection
        ratio = t / T
        disp_time(title, t, ratio)
        od[title] = t
        
        title = 'Inference time'
        t = et_inference - st_inference
        ratio = t / T
        disp_time(title, t, ratio)
        od[title] = t
            
        title = 'Total time'
        t = et_total - st_total
        ratio = t / T
        disp_time(title, t, ratio)
        od[title] = t

        update_edge_result(od)
        
        print(f'[+] Done {mode} experiment')

        
    '''
    elif mode == 'advanced':
        config_file = os.getcwd() + '/' + 'config.yaml'
        
        with open(config_file) as f:
            cfg = yaml.load(f, Loader=yaml.FullLoader)

        selected_model = model_selector.advancedModelSelection(cfg)

        for m in selected_model.keys():
            for n in selected_model[m]:
                print(f'mode = {mode}, node = {n}, selected_model = {m}')
                et_modelselection = time.time() #---------------------
                

                #----------------------------------
                # 에지 디바이스에서 추론을 수행합니다. 
                #----------------------------------
                st_inference = time.time() #---------------------
                cmd = f'ansible vnv -i ./config/hosts.ini -l {n} -m shell -a "cd {wdir}; pwd; {py} inference4vnv.py --model {m} --device {device} --N {N};"  {ask_pass_option} ' 
                
                print(cmd)
                run(cmd, True)
                et_inference = time.time() #---------------------
                
                #---------------------------------------------------
                et_total = time.time()
                #---------------------------------------------------

                print( f'[d] workding dir = {wdir}' )
                print( f'[d] py = {py}' )
                print( f'[d] node =  {n}' )
                print( f'[d] selected_model = {m}' )

                T = et_total - st_total
                
                title = 'Get status time'
                t = et_getstatus - st_getstatus
                ratio = t / T
                disp_time(title, t, ratio)
                
                title = 'Model selection time'
                t = et_modelselection - st_modelselection
                ratio = t / T
                disp_time(title, t, ratio)

                title = 'Inference time'
                t = et_inference - st_inference
                ratio = t / T
                disp_time(title, t, ratio)
                
                title = 'Total time'
                t = et_total - st_total
                ratio = t / T
                disp_time(title, t, ratio)

                print(f'[+] Done {mode} experiment')

    '''



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