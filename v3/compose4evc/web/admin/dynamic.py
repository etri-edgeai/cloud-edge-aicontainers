# dynamic invenotory
# J.Park, 2022-07-05

import os
import sys
import argparse
import json
import subprocess

def parse_args():
    parser = argparse.ArgumentParser(description='dynamic inventory tester')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true')
    group.add_argument('--host')
    return parser.parse_args()

def list_running_hosts():
    #hosts = [{"mac":"localhost"}, {"rpi1":"192.168.0.11"}, {"rpi2":"192.168.0.12"}]
    hosts = ["localhost"]
    return hosts

def get_host_details(host):
#host_details = [{"host_attr1":"a", "host_attr2":"b"}]
    host_details = [{"ansible_host":"localhost",
    "ansible_port":22,
    "dtap":"dev",
    "comment":"Host server"}]
    return host_details

def main():
    args = parse_args()
    if args.list:
        hosts = list_running_hosts()
        json.dump({"mac":hosts}, sys.stdout)
    else:
        details = get_host_details(args.host)
        json.dump(details, sys.stdout)

if __name__ == '__main__':
    main()
    
