import sqlite3

import os
import re
from datetime import datetime

import schedule
import time

import warnings

warnings.filterwarnings(action='ignore')



## write file
os.system('ansible-playbook sysinfo.yaml')

## data processing
file = open('syslog.txt', 'r')
line = file.readline()
p = re.compile('rpi[\d]+')
data = []

line = file.readline()
print(line)
file.close()