import os
import yaml
import re
from device_info import set_model4infer

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

    def showAllModels(self):
        print( self.urlmodels )

    def greedModelSelection(self):
        set_model4infer('mobilenet_v3_large')
        return ['mobilenet_v3_large']

    def advancedModelSelection(self):
        set_model4infer('mobilenet_v3_small')
        return ['mobilenet_v3_small']
    
        