import torch
import torch.nn as nn
import copy

from .measures import *
import time
import sys

import matplotlib.pyplot as plt
import numpy as np
import torchvision
import os


from train_tools.preprocessing.cifar10.loader import get_dataloader_cifar10
from train_tools.preprocessing.cifar100.loader import get_dataloader_cifar100

__all__ = ["BaseClientTrainer"]


DATA_LOADERS = {
    "cifar10": get_dataloader_cifar10,
    "cifar100": get_dataloader_cifar100,
}




class BaseClientTrainer:
    def __init__(self, algo_params, model, local_epochs, device, num_classes):
        """
        ClientTrainer class contains local data and local-specific information.
        After local training, upload weights to the Server.
        """

        # algorithm-specific parameters
        self.algo_params = algo_params
        # model & optimizer
        self.model = model
        self.criterion = nn.CrossEntropyLoss()
        self.local_epochs = local_epochs
        self.device = device
        self.datasize = None # client index에 맞게 채워질 예정
        self.num_classes = num_classes
        self.train_idxs = None # client index에 맞게 채워질 예정
        self.test_idxs = None # client index에 맞게 채워질 예정
        self.data_name = None

    def train(self):
        """Local training"""
        self.model.train()
        self.model.to(self.device)
        
        local_size = self.datasize
        
        epoch_loss = []
        
        root = os.path.join("./data", self.data_name)
        self.trainloader=DATA_LOADERS[self.data_name](root=root, train=True, batch_size=50, dataidxs=self.train_idxs)  
        
        for _ in range(self.local_epochs):
            batch_loss=[]
            for data, targets in self.trainloader:
                self.optimizer.zero_grad()
                
                # forward pass
                data, targets = data.to(self.device), targets.to(self.device)
                output = self.model(data)
                loss = self.criterion(output, targets)

                # backward pass
                loss.backward()

                self.optimizer.step()
                batch_loss.append(loss.item())
            epoch_loss.append(sum(batch_loss)/len(batch_loss))
        local_results = self._get_local_stats()
        
    
        return local_results, local_size


    def _get_local_stats(self):
        local_results = {}

        local_results["train_acc"] = evaluate_model(
            self.model, self.trainloader, self.device
        )
        
        
        
#         (
#             local_results["classwise_accuracy"],
#             local_results["test_acc"],
#         ) = evaluate_model_classwise(
#             self.model, self.testloader, self.num_classes, device=self.device,
#         )

        return local_results

    def download_global(self, server_weights, server_optimizer):
        """Load model & Optimizer"""
        self.model.load_state_dict(server_weights)

        server_optimizer_info=server_optimizer['param_groups'][0]
    
        body_params = [p for name, p in self.model.named_parameters() if 'classifier' not in name]
        head_params = [p for name, p in self.model.named_parameters() if 'classifier' in name]
    
        self.optimizer= torch.optim.SGD([{'params': body_params, 'lr': server_optimizer_info['lr']},
                                     {'params': head_params, 'lr': server_optimizer_info['lr']}],
                                    momentum=server_optimizer_info['momentum'],
                                    weight_decay=server_optimizer_info['weight_decay'])
       
        
        

    def upload_local(self):
        """Uploads local model's parameters"""
        local_weights = copy.deepcopy(self.model.state_dict())

        return local_weights

    def reset(self):
        """Clean existing setups"""
        self.datasize = None
        
        self.train_idxs = None 
        self.test_idxs = None 
        self.data_name = None
        
        
        self.trainloader = None
        self.testloader = None
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=0)

    def _keep_global(self): #fedntd clienttrainer 용도 같음!!
        """Keep distributed global model's weight"""
        self.dg_model = copy.deepcopy(self.model)
        self.dg_model.to(self.device)

        for params in self.dg_model.parameters():
            params.requires_grad = False
