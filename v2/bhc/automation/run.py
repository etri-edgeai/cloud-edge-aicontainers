import os
import platform
import re

def get_reg_ip():
    print("Write IP address of registry including port...")
    ip = str(input())
    # regex = re.compile('[\d]+[.][\d]+[.][\d]+[.][\d]+[:][\d]+')
    # if not regex.match(ip):
    #     print("IP incorrect. please check again..")
    # else:
    #     return ip
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
    
    def docker_script(self, image):
        pull_image = f"docker pull {image}"
        print(pull_image)
        build_container = f"docker run -d --name edge-model -it {image}"
        print(build_container)

        return pull_image, build_container
    
    def prediction(self, model_type, model_name):
        get_pred = f"docker exec edge-model python home/classifier.py --model_type {model_type} --model_name {model_name}"

        return get_pred

def generate_model(dpull, drun):
    os.system(dpull)
    os.system(drun)

def main():
    sh_gen = script_generator(ip, os, arch)
    
    docker_image = sh_gen.get_image()
    pull, run = sh_gen.docker_script(docker_image)
    generate_model(pull, run)

    model_type, model_name = get_models()
    start = sh_gen.prediction(model_type, model_name)
    os.system(start)


if __name__=="__main__":
    
    print("Dectecting Operation System...")
    print()

    op_sys = platform.system()
    print("OS : ", op_sys)

    print("Detecting CPU Architecture...")
    print()

    arch = platform.machine()
    print("Architecture : ", arch)
    
    ip = get_reg_ip()

    main()
