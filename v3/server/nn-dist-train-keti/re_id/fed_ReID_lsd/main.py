# -*- coding: utf-8 -*-
from __future__ import print_function, division
import argparse
import torch
import time
import os
import yaml
import random
import numpy as np
import scipy.io
import pathlib
import sys
import json
import copy
import multiprocessing as mp
import torch.nn.functional as F
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from PIL import Image
from client import Client
from server import Server
from utils import set_random_seed
from data_utils import Data

mp.set_start_method('spawn', force=True)
sys.setrecursionlimit(10000)
version =  torch.__version__

parser = argparse.ArgumentParser(description='Training')
parser.add_argument('--gpu_ids',default='0', type=str,help='gpu_ids: e.g. 0  0,1,2  0,2')
parser.add_argument('--model_name',default='ft_ResNet50', type=str, help='output model name')
parser.add_argument('--project_dir',default='.', type=str, help='project path')
parser.add_argument('--data_dir',default='data',type=str, help='training dir path')
parser.add_argument('--datasets',default='Market,DukeMTMC-reID,cuhk03-np-detected,cuhk01,MSMT17,viper,prid,3dpes,ilids',type=str, help='datasets used')
parser.add_argument('--train_all', action='store_true', help='use all training data' )
parser.add_argument('--stride', default=2, type=int, help='stride')
parser.add_argument('--lr', default=0.05, type=float, help='learning rate')
parser.add_argument('--drop_rate', default=0.5, type=float, help='drop rate')

# arguments for federated setting
parser.add_argument('--local_epoch', default=1, type=int, help='number of local epochs')
parser.add_argument('--batch_size', default=32, type=int, help='batch size')
parser.add_argument('--num_of_clients', default=9, type=int, help='number of clients')

# arguments for data transformation
parser.add_argument('--erasing_p', default=0, type=float, help='Random Erasing probability, in [0,1]')
parser.add_argument('--color_jitter', action='store_true', help='use color jitter in training' )

# arguments for testing federated model
parser.add_argument('--which_epoch',default='last', type=str, help='0,1,2,3...or last')
parser.add_argument('--multi', action='store_true', help='use multiple query' )
parser.add_argument('--multiple_scale',default='1', type=str,help='multiple_scale: e.g. 1 1,1.1  1,1.1,1.2')
parser.add_argument('--test_dir',default='all',type=str, help='./test_data')

# arguments for optimization
parser.add_argument('--cdw', action='store_true', help='use cosine distance weight for model aggregation, default false' )
parser.add_argument('--kd', action='store_true', help='apply knowledge distillation, default false' )
parser.add_argument('--regularization', action='store_true', help='use regularization during distillation, default false' )

#arguments for ntd loss
parser.add_argument('--tau', type=int, default=3, help='ntd loss hyperparameter (tau)')
parser.add_argument('--beta', type=int, default=1, help='ntd loss hyperparameter (beta)')


def train():
    args = parser.parse_args()
    print(args)
    
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda:{}".format(args.gpu_ids) if use_cuda else "cpu")
    set_random_seed(1)

    data = Data(args.datasets, args.data_dir, args.batch_size, args.erasing_p, args.color_jitter, args.train_all)
    data.preprocess()#dictionary에 각 client(Dataset)에 올릴 dataloader 생성!!
    
    clients = {}
    for cid in data.client_list:#data.client_list: 리스트 안에 dataset name 나열!! cid는 dataset name!!
        clients[cid] = Client(
            cid, 
            data, 
            device, 
            args.project_dir, 
            args.model_name, 
            args.local_epoch, 
            args.lr, 
            args.batch_size, 
            args.drop_rate, 
            args.stride, args.tau, args.beta)

    server = Server(
        clients, 
        data, 
        device, 
        args.project_dir, 
        args.model_name, 
        args.num_of_clients, 
        args.lr, 
        args.drop_rate, 
        args.stride, 
        args.multiple_scale)#args.lr 필요 없을 거 같음!!

    dir_name = os.path.join(args.project_dir, 'model', args.model_name)#./model/ft_ResNet50
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)

    print("=====training start!========")
    rounds = 800
    for i in range(rounds):
        print('='*10)
        print("Round Number {}".format(i))
        print('='*10)
        server.train(i, args.cdw, use_cuda) #추후에 args.cdw 인자 없애도 될 것 같음!!
        save_path = os.path.join(dir_name, 'federated_model.pth')
#         torch.save(server.federated_model.cpu().state_dict(), save_path)
        torch.save(server.federated_model, save_path)

        if (i+1)%100 == 0:
#             server.test(use_cuda)
            server.test()

#             if args.kd:#pure fedpav 기준 필요 없을 것 같음!! 
#                 server.knowledge_distillation(args.regularization)
#                 server.test(use_cuda)
        server.draw_curve()

if __name__ == '__main__':
    train()




