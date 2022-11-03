import os
import platform
import re

def get_reg_ip():
    print("Write IP address of registry including port...")
    ip = input()
    regex = re.compile('[\d]+[.][\d]+[.][\d]+[.][\d]+[:][\d]+')
    if not regex.match(ip):
        print("IP incorrect. please check again..")
    else:
        return ip

def get_models():
    cmd = 'docker exec edge-model python classifier.py --help'
    os.system(cmd)
    print("check the list and choose your model...")
    print()
    model_type = str(input("write model type : "))
    model_name = str(input("write model name : "))

    return model_type, model_name


class script_generator:

    def __init__(self, ip, os, arch, model):
        self.os = os
        self.arch = arch
        self.ip = ip
        self.model = model
    
    def get_image(self):
        if self.arch == 'AMD64':
            image = 'edge-model:1.1'
    
        return image
    
    def write_script(self, image, model_type, model_name):
        pull_image = f"docker pull {self.ip}/{image}"
        build_container = f"docker run -d --name edge-model -it {self.ip}/{image}"
        run_model = f"docker exec edge-model python home/classifier.py --model_type {model_type} --model_name {model_name}"

        return pull_image, build_container, run_model



        

    
        


            



print("Dectecting Operation System...")
print("OS : ", os)
print()
print("Detecting CPU Architecture...")
print("Architecture : ", arch)
print()

if os == 'Windows':
