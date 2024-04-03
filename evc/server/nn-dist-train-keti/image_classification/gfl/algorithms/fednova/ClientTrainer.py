import torch
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), "../../")))

from algorithms.BaseClientTrainer import BaseClientTrainer
from algorithms.fednova.utils import *

from train_tools.preprocessing.cifar10.loader import get_dataloader_cifar10
from train_tools.preprocessing.cifar100.loader import get_dataloader_cifar100

__all__ = ["ClientTrainer"]

DATA_LOADERS = {
    "cifar10": get_dataloader_cifar10,
    "cifar100": get_dataloader_cifar100,
}

class ClientTrainer(BaseClientTrainer):
    def __init__(self, **kwargs):
        super(ClientTrainer, self).__init__(**kwargs)
        """
        ClientTrainer class contains local data and local-specific information.
        After local training, upload weights to the Server.
        """

        self.weighted_d = None
        self.d_i = None
        self.c_i = None

        # Boolean variable which allows scaffold-like Cross-Client Variance Reduction
        self.nova_ccvr = self.algo_params.nova_ccvr

    def train(self):
        """Local training"""

        # Keep global model weights
        self._keep_global()

        self.model.train()
        self.model.to(self.device)

        local_size = self.datasize
        root = os.path.join("./data", self.data_name)
        self.trainloader=DATA_LOADERS[self.data_name](root=root, train=True, batch_size=50, dataidxs=self.train_idxs)  

        for _ in range(self.local_epochs):
            for data, targets in self.trainloader:
                self._nova_step(data, targets)

        # update control variates for scaffold algorithm
        aidi = self._update_control_variate()

        local_results = self._get_local_stats()

        return local_results, local_size, aidi

    def download_global(self, server_weights, server_optimizer, weighted_d, d_i):
        """Load model & Optimizer"""
        self.model.load_state_dict(server_weights)

        server_optimizer_info=server_optimizer['param_groups'][0]
    
        body_params = [p for name, p in self.model.named_parameters() if 'classifier' not in name]
        head_params = [p for name, p in self.model.named_parameters() if 'classifier' in name]
    
        self.optimizer= torch.optim.SGD([{'params': body_params, 'lr': server_optimizer_info['lr']},
                                     {'params': head_params, 'lr': server_optimizer_info['lr']}],
                                    momentum=server_optimizer_info['momentum'],
                                    weight_decay=server_optimizer_info['weight_decay'])
        self.weighted_d, self.d_i = weighted_d.to(self.device), d_i.to(self.device)
        self.c_i = self.weighted_d - self.d_i
        
        

    def _nova_step(self, data, targets):
        self.optimizer.zero_grad()

        # forward pass
        data, targets = data.to(self.device), targets.to(self.device)
        logits = self.model(data)
        loss = self.criterion(logits, targets)

        # backward pass
        loss.backward()

        grad_batch = flatten_grads(self.model).detach().clone()
        # add control variate if it is enabled
        if self.nova_ccvr:
            grad_batch = grad_batch + self.c_i
            grad_batch = grad_batch.detach().clone()

        self.optimizer.zero_grad()

        self.model = assign_grads(self.model, grad_batch)
        self.optimizer.step()

    @torch.no_grad()
    def _update_control_variate(self):
        local_lr = self.__get_learning_rate()

        server_params = flatten_weights(self.dg_model)
        local_params = flatten_weights(self.model)
        param_move = server_params - local_params

        aidi = torch.from_numpy(param_move / local_lr)

        return aidi.detach().clone()

    def __get_learning_rate(self):
        for param_group in self.optimizer.param_groups:
            return param_group["lr"]
