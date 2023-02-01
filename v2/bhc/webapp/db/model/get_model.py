import sqlite3
import json
import os
import re

def get_model_info():
    
    os.system("curl -s https:/123.214.186.252:39500/v2/_catalog -k > modelog.txt")

    with open('modelog.txt', 'r') as f:
        data = json.load(f)
    
    print(type(data['repositories'][0]))

def model_download():
    pass

def get_desc():
    pass

if __name__ == "__main__":

    get_model_info()