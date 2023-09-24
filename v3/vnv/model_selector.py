import os
import yaml
import re

class ModelSelection():
    def __init__(self):
        # Models
        self.urlroot = 'http://keticmr.iptime.org:22080/edgeai/models_jpark/'

        self.model_names_resnet = [ 
            'resnet18',
            'resnet34',
            'resnet50',
            'resnet101',
            'resnet152',
        ]
        self.repo_resnet = 'pytorch/vision:v0.10.0'

        self.model_names_mobnet = [
            'mobilenet_v3_small',
            'mobilenet_v3_large',
        ]
        self.repo_mobnet = 'pytorch/vision:v0.10.0'

        self.model_names_effnet = [ 
            'nvidia_efficientnet_b0',
            'nvidia_efficientnet_b4',
            'nvidia_efficientnet_widese_b0',
            'nvidia_efficientnet_widese_b4',
        ]
        self.repo_effnet = 'NVIDIA/DeepLearningExamples:torchhub'

        model_names = self.model_names_resnet + self.model_names_effnet + self.model_names_mobnet
        pth_names = [ model_name + '-dict.pth' for model_name in model_names ]

        self.urlmodels = []
        for pth_name in pth_names:
            self.urlmodels.append(self.urlroot + pth_name)

    def hi(self):
        return 'hi'

    def showAllModels(self):
        print( self.urlmodels )

    def getinfoModelSelection(self, cfg):
        return ['mobilenet_v3_small'] # 간단한 모델을 실행합니다.
    
    def greedModelSelection(self):
        return ['resnet152']
    
    def advancedModelSelection(self, cfg):
        #return 'resnet18'
        return ['mobilenet_v3_small']
    
        node_nuc = []
        node_rpi = []
        node_sv = []

        for d in cfg['target'].keys():
            if 'nuc' in d:
                for i in range(len(cfg['target'][d])):
                    node_nuc.append(cfg['target'][d][i]['name'])
            
            elif 'rpi' in d:
                for i in range(len(cfg['target'][d])):
                    node_rpi.append(cfg['target'][d][i]['name'])
            
            elif 'server' in d:
                for i in range(len(cfg['target'][d])):
                    node_sv.append(cfg['target'][d][i]['name'])

            new_dict = {
                "resnet18" : node_rpi,
                "resnet50" : node_nuc,
                "resnet152" : node_sv
                }

        return new_dict

        