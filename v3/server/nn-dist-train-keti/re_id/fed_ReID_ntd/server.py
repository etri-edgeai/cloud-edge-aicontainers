import os
import math
import json
import matplotlib.pyplot as plt
from utils import get_model, extract_feature
import torch.nn as nn
import torch
import scipy.io
import copy
from data_utils import ImageDataset
import random
import torch.optim as optim
from torchvision import datasets
import sys

def aggregate_models(models, weights):
    """aggregate models based on weights
    params:
        models: model updates from clients
        weights: weights for each model, e.g. by data sizes or cosine distance of features
    """
    training_num=sum(weights)
    averaged_params=models[0]
    for k in averaged_params.keys():
        for i in range(0, len(models)):
            w=weights[i]/training_num
            if i==0:
                averaged_params[k]=models[i][k]*w
            else:
                averaged_params[k]+=models[i][k]*w
    return averaged_params


class Server():
    def __init__(self, clients, data, device, project_dir, model_name, num_of_clients, lr, drop_rate, stride, multiple_scale):
        self.project_dir = project_dir
        self.data = data
        self.device = device
        self.model_name = model_name
        self.clients = clients
        self.client_list = self.data.client_list
        self.num_of_clients = num_of_clients
        self.lr = lr
        self.multiple_scale = multiple_scale
        self.drop_rate = drop_rate
        self.stride = stride

        self.multiple_scale = []
        for s in multiple_scale.split(','):
            self.multiple_scale.append(math.sqrt(float(s)))

        self.full_model = get_model(750, drop_rate, stride) #750 들어가도 상관없음, 이것은 class 갯수인데 server에서는 도려낼거라 의미없음!!               
        self.full_model.classifier.classifier = nn.Sequential()
        self.federated_model_0=self.full_model.to(self.device) #feature extractor만 남긴다!!
        self.federated_model=copy.deepcopy(self.federated_model_0).state_dict()
        self.federated_model_0.eval()
        self.train_loss = [] #매 round마다 중앙 서버 모델 performance 기재


    def train(self, epoch, cdw, use_cuda):
        if (epoch+1)%5==0:
            self.lr*=0.99
        models = []
        loss = []
        data_sizes = []
        current_client_list = random.sample(self.client_list, self.num_of_clients) #cross-device도 가능은 함!!
        for i in current_client_list:
            self.clients[i].train(self.federated_model, use_cuda, self.lr)
            loss.append(self.clients[i].get_train_loss())
            models.append(self.clients[i].get_model())
            data_sizes.append(self.clients[i].get_data_sizes())


        avg_loss = sum(loss) / self.num_of_clients

        print("==============================")
        print("number of clients used:", len(models))
        print('Train Epoch: {}, AVG Train Loss among clients of lost epoch: {:.6f}'.format(epoch, avg_loss))
        
        self.train_loss.append(avg_loss)
        
        weights = data_sizes
        

        self.federated_model = aggregate_models(models, weights)

    def draw_curve(self):
        plt.figure()
        x_epoch = list(range(len(self.train_loss)))
        plt.plot(x_epoch, self.train_loss, 'bo-', label='train')
        plt.legend()
        dir_name = os.path.join(self.project_dir, 'model', self.model_name)
        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)
        plt.savefig(os.path.join(dir_name, 'train.png'))
        plt.close('all')
        
    def test(self):
        print("="*10)
        print("Start Tesing!")
        print("="*10)
        print('We use the scale: %s'%self.multiple_scale)#multiple scale 의미 없는 것 같음
        
        for dataset in self.data.datasets:
            self.federated_model_0.load_state_dict(self.federated_model)
            
            with torch.no_grad():
                gallery_feature = extract_feature(self.federated_model_0, self.data.test_loaders[dataset]['gallery'], self.multiple_scale, self.device) #각 gallery 데이타의 normalized된 feature vector를 concatenate한다.
                query_feature = extract_feature(self.federated_model_0, self.data.test_loaders[dataset]['query'], self.multiple_scale, self.device) #각 query 데이타의 normalized된 feature vector를 concatenate한다.

            result = {
                'gallery_f': gallery_feature.numpy(),
                'gallery_label': self.data.gallery_meta[dataset]['labels'],
                'gallery_cam': self.data.gallery_meta[dataset]['cameras'],
                'query_f': query_feature.numpy(),
                'query_label': self.data.query_meta[dataset]['labels'],
                'query_cam': self.data.query_meta[dataset]['cameras']}

            scipy.io.savemat(os.path.join(self.project_dir,
                        'model',
                        self.model_name,
                        'pytorch_result.mat'),
                        result)
                        
            print(self.model_name)
            print(dataset)

            os.system('python evaluate.py --result_dir {} --dataset {}'.format(os.path.join(self.project_dir, 'model', self.model_name), dataset))

