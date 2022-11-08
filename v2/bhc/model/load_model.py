from __future__ import print_function, division

import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import torch.backends.cudnn as cudnn
import numpy as np
from torch.utils.data import DataLoader
from torch.autograd import Variable
import os
import copy

import time
from tqdm import tqdm
import matplotlib.pyplot as plt

from PIL import Image
import argparse
import warnings

warnings.filterwarnings("ignore")


# gpu set
device = torch.device('cpu')


## define labels
classes = ['plane', 'car', 'bird', 'cat',
        'deer', 'dog', 'frog', 'horse', 'ship', 'truck']



def get_weights_list(model_type):

    weights_dir = './home/best_model'

    if model_type == 'resnet':
        weights = os.listdir(weights_dir + '/resnet')
    elif model_type == 'efficientnet':
        weights = os.listdir(weights_dir + '/efficientnet')
    elif model_type == 'mobilenet':
        weights = os.listdir(weights_dir + '/mobilenet')
    elif model_type == 'resnet_advanced':
        weights = os.listdir(weights_dir + '/resnet_advanced')
    else:
        print("No model found. please check exact name of model or typo, unless pytorch_hub has the model what you are looking for.")
        exit()
    
    weights_dir = weights_dir + '/' + model_type

    return weights_dir, weights


def get_hub_path(model_type):

    hub_dict = {
        'resnet':'pytorch/vision:v0.10.0',
        'resnet_advanced':'pytorch/vision:v0.10.0',
        'efficientnet':'pytorch/vision',
        'mobilenet':'pytorch/vision'
    }
    hub_path = hub_dict[model_type]

    return hub_path

    
def select_model(model_type, model_name):

    ## load model architecture
    hub_path = get_hub_path(model_type)
    model = torch.hub.load(hub_path, model_name, pretrained=False)


    ## change output layer fitted with dataset categories
    if model_type == 'resnet' or model_type == 'resnet_advanced':
        num_ftrs = model.fc.in_features
        model.fc = nn.Linear(num_ftrs, len(classes))
    elif model_type == 'efficientnet':
        num_ftrs = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(num_ftrs, len(classes))
    elif model_type == 'mobilenet' and 'mobilenet_v2' in model_name:
        num_ftrs = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(num_ftrs, len(classes))
    elif model_type == 'mobilenet' and 'mobilenet_v3' in model_name:
        num_ftrs = model.classifier[3].in_features
        model.classifier[3] = nn.Linear(num_ftrs, len(classes))


    ## load saved weights
    weights_path, weights = get_weights_list(model_type)


    ## update trained weights to model
    for w_list in weights:
        try:
            val = model_name in w_list
            if val:
                model_path = weights_path + '/' + w_list
                saved_weights = torch.load(model_path, map_location=torch.device('cpu'))
                print('model loaded successfully')
        except:
            print("No saved_wieghts found. we may haven't trained the model what you are looking for yet.")
            exit()

    model.load_state_dict(saved_weights)
    model.to(device)
    
    return model