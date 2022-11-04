import os
import platform
import re

def get_reg_ip():
    print("Write IP address of registry including port...")
    ip = str(input())
    print()
    # regex = re.compile('[\d]+[.][\d]+[.][\d]+[.][\d]+[:][\d]+')
    # if not regex.match(ip):
    #     print("IP incorrect. please check again..")
    # else:
    #     return ip
    return ip

def get_models():
    print()
    cmd = 'docker exec edge-model python home/classifier.py --help'
    os.system(cmd)
    print()
    print("check the list and choose your model...")
    print()
    model_type = str(input("write model type : "))
    model_name = str(input("write model name : "))

    return model_type, model_name


class script_generator:

    def __init__(self, ip, os, arch):
        self.os = os
        self.arch = arch
        self.ip = ip
    
    def get_image(self):
        # if self.arch == 'AMD64':
        #     image = 'edge-model:1.1'
        image = 'edge-model:1.1'
        
        image = f"{self.ip}/{image}"
    
        return image
    
    def build_script(self, image):
        pull_image = f"docker pull {image}"
        build_container = f"docker run -d --name edge-model -it {image}"

        return pull_image, build_container
    
    def pred_script(self, model_type, model_name):
        get_pred = f"docker exec edge-model python home/classifier.py --model_type {model_type} --model_name {model_name}"

        return get_pred

def generate_model(dpull, drun):
    os.system(dpull)
    os.system(drun)

def main():
    gen = script_generator(ip, os, arch)
    
    docker_image = gen.get_image()
    pull, run = gen.build_script(docker_image)
    generate_model(pull, run)

    model_type, model_name = get_models()
    start = gen.pred_script(model_type, model_name)
    os.system(start)


if __name__=="__main__":
    
    print("Dectecting Operation System...")
    op_sys = platform.system()
    print("OS : ", op_sys)
    print()

    print("Detecting CPU Architecture...")
    arch = platform.machine()
    print("Architecture : ", arch)
    print()

    ip = get_reg_ip()

    main()
