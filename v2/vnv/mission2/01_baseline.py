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

cmd = 'ansible vnv -m shell -a "cat /proc/cpuinfo" -i hosts.ini > ./tmp/baseline_cpuinfo.txt'
run(cmd, False)

cmd = 'ansible vnv -m shell -a "cat /proc/meminfo" -i hosts.ini > ./tmp/baseline_meminfo.txt'
run(cmd, False)

#---------------------------------------------------
end = time.time()
#---------------------------------------------------

# print('t = ', end - start)
print('[+] Done baseline experiment')
