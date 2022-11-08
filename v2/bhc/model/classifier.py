from __future__ import print_function, division

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
from load_model import *
import textwrap

warnings.filterwarnings("ignore")


# gpu set
device = torch.device('cpu')



def get_infer():

    ## load model
    model = select_model(args.model_type, args.model_name)

    ## define preprocessing
    import torchvision
    from torchvision import datasets, models, transforms
    test_preprocess = torchvision.transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])


    ## load input data
    data_path = './home/data/'
    data_path = data_path + args.input
    img = Image.open(data_path)
    img_tensor = test_preprocess(img)
    input_batch = img_tensor.unsqueeze(0)


    ## test model
    input_batch = input_batch.to(device)
    output = model(input_batch)
    probabilities = torch.nn.functional.softmax(output[0], dim=0)

    top5_prob, top5_catid = torch.topk(probabilities, 5)
    print()
    for i in range(top5_prob.size(0)):
        print(classes[top5_catid[i]], top5_prob[i].item())
    print()


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
                docker_inference_model
        -----------------------------------------
        model list : 
        
        < resnet || resnet_advanced >

            - resnet18
            - resnet34
            - resnet50
            - resnet101
            - resnet152
            
        < efficientnet >

            - efficientnet_b0
            - efficientnet_b1
            - efficientnet_b2
            - efficientnet_b3
            - efficientnet_b4
            - efficientnet_b5
            - efficientnet_b6
            - efficientnet_b7

        < mobilenet >

            - mobilenet_v2
            - mobilenet_v3_small
            - mobilenet_v3_large
        '''))
    parser.add_argument(
        '--model_type',
        default='resnet',
        type=str,
        help='select model type (resnet, efficientnet, mobilenet)'
    )
    parser.add_argument(
        '--model_name',
        default='resnet152',
        type=str,
        help='select exact name of model (please check model_list)'
    )
    parser.add_argument(
        '--input',
        default='test.jpeg',
        help='path of data for prediction (insert your data in ./data/)'
    )

    args = parser.parse_args()
    print()
    print(args)
    print()

    get_infer()

