#------------------------------------------------------
# vnv
#------------------------------------------------------

#!/bin/bash

# http://keticmr.iptime.org:22809

# <ubuntu> 
# $ sudo apt install speedtest-cli

# <rpi> 
# $ sudo pip3 install speedtest-cli

import os
import time
from model_selector import ModelSelection

def run(cmd, is_show=False):

    # import subprocess
    # p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    # if(is_show):
    #     print(p.communicate())
    stream = os.popen(cmd)
    output = stream.read()

    if is_show:
        print( output )
    else:
        pass

def main(mode = 'baseline'):
    if mode == 'baseline' or mode == 'advanced':
        print(f'[+] Start {mode} experiment')
    else:
        print(f'[-] error, there is no [{mode}] mode.')
        return
    #---------------------------------------------------
    start = time.time()
    #---------------------------------------------------

    #----------------------------------
    # 에지 디바이스의 상태정보를 얻습니다.
    #----------------------------------

    wdir = ' /home/jpark/WorkDevEdgeAI/cloud-edge-aicontainers/v2/vnv/mission2/'
    py = ' /usr/bin/python3'
    selected_model = 'resnet152' # default
    device = 'cuda'
    N = 10
    ask_pass_option = '' #  '--ask-become-pass'
    model_selector = ModelSelection()

    print( wdir )
    print( py )
    print( selected_model )
    print(' ')
    #cmd_sub = ' /usr/bin/python3 -c "import torch; print(torch.cuda.is_available())" '
    cmd = f'ansible vnv -m shell -a "cd {wdir}; {py} cuda_is_available.py " -i hosts.ini '
    run(cmd, True)

    # for ubuntu
    cmd = f'ansible vnv -m shell -a "cat /proc/cpuinfo" -i hosts.ini > ./tmp/baseline_cpuinfo.txt'
    run(cmd, False)

    cmd = f'cat ./tmp/baseline_cpuinfo.txt | grep "model name" '
    run(cmd, False)

    cmd = f'ansible vnv -m shell -a "cat /proc/meminfo" -i hosts.ini > ./tmp/baseline_meminfo.txt '
    run(cmd, False)

    cmd = f'cat ./tmp/baseline_meminfo.txt | grep "MemTotal" '
    run(cmd, False)

    #----------------------------------
    # 추론을 위한 AI 모델을 선택합니다.
    #----------------------------------
    
    if mode == 'baseline':
        selected_model = model_selector.greedModelSelection()
    elif mode == 'advanced':
        selected_model = model_selector.advancedModelSelection()

    print(f'mode = {mode}, selected_model = {selected_model}')
    

    #----------------------------------
    # 에지 디바이스에서 추론을 수행합니다. 
    #----------------------------------

    cmd = f'ansible vnv -i hosts.ini -m shell -a "cd {wdir}; pwd; {py} vnv03.py --model {selected_model} --device {device} --N {N};"  {ask_pass_option} ' 
    run(cmd, False)

    #---------------------------------------------------
    end = time.time()
    #---------------------------------------------------

    print('[d] Total processing time [seconds] = ', end - start)
    print('[+] Done baseline experiment')


import sys
if __name__ == "__main__":
    
    # total arguments
    n = len(sys.argv)
    for i in range(1, n):
        print(sys.argv[i], end = " ")

    if n != 2:
        print('[-] argument error')
        print('    e.g. python3 run_vnv.py baseline')
        print('    e.g. python3 run_vnv.py advanced')
    main(sys.argv[1])

#------------------------------------------------------
# End of this file
#------------------------------------------------------
