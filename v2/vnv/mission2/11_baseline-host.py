#!/bin/bash

# http://keticmr.iptime.org:22809

# <ubuntu> 
# $ sudo apt install speedtest-cli

# <rpi> 
# $ sudo pip3 install speedtest-cli

import subprocess
import time

# This is our shell command, executed by Popen.

def run(cmd, is_show=False):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

    if(is_show):
        print(p.communicate())


print('[+] Start baseline experiment')
#---------------------------------------------------
start = time.time()
#---------------------------------------------------

cmd = 'ansible host -i hosts.ini -m shell -a "cd /Users/jpark/WorkDevEdgeAI/cloud-edge-aicontainers/v2/vnv/mission2; pwd; /opt/homebrew/bin/python3 vnv03.py resnet18 cpu 0"  > ./tmp/baseline.txt  ' 
run(cmd, False)

#---------------------------------------------------
end = time.time()
#---------------------------------------------------

print('t = ', end - start)
print('[+] Done baseline experiment')
