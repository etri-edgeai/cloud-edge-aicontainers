#!/bin/bash

# http://keticmr.iptime.org:22809

# <ubuntu> 
# $ sudo apt install speedtest-cli

# <rpi> 
# $ sudo pip3 install speedtest-cli

import os
import subprocess
import time

# This is our shell command, executed by Popen.

def run(cmd, is_show=False):
    #p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    #if(is_show):
    #    print(p.communicate())

    stream = os.popen(cmd)
    output = stream.read()
    output


print('[+] Start baseline experiment')
#---------------------------------------------------
start = time.time()
#---------------------------------------------------

cmd = 'ansible vnv -m shell -a "cat /proc/cpuinfo" -i hosts.ini > ./tmp/baseline_cpuinfo.txt'
run(cmd, False)

cmd = 'ansible vnv -m shell -a "cat /proc/meminfo" -i hosts.ini > ./tmp/baseline_meminfo.txt'
run(cmd, False)

#cmd = 'ansible vnv -i hosts.ini -m shell -a "cd /home/jpark/WorkDevEdgeAI/cloud-edge-aicontainers/v2/vnv/mission2; pwd; /usr/bin/python3 vnv03.py resnet18 cuda 0;"  --ask-become-pass  > ./tmp/baseline.txt  ' 
cmd = 'ansible vnv -i hosts.ini -m shell -a "cd /home/jpark/WorkDevEdgeAI/cloud-edge-aicontainers/v2/vnv/mission2; pwd; /usr/bin/python3 vnv03.py resnet152 cuda 0;"  > ./tmp/baseline.txt  ' 
run(cmd, False)

#---------------------------------------------------
end = time.time()
#---------------------------------------------------

print('t = ', end - start)
print('[+] Done baseline experiment')
