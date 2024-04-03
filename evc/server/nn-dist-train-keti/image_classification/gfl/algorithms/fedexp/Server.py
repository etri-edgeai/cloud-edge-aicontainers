import copy
import os
import sys
import math
import numpy as np
import torch

sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), "../../")))

from algorithms.fedavg.ClientTrainer import ClientTrainer
from algorithms.BaseServer import BaseServer

__all__ = ["Server"]


class Server(BaseServer):
    def __init__(
        self, algo_params, model, data_distributed, optimizer, scheduler, **kwargs
    ):
        super(Server, self).__init__(
            algo_params, model, data_distributed, optimizer, scheduler, **kwargs
        )
        """
        Server class controls the overall experiment.
        """
        self.client = ClientTrainer(
            algo_params=self.algo_params,
            model=copy.deepcopy(model),
            local_epochs=self.local_epochs,
            device=self.device,
            num_classes=self.num_classes,
        )

        self.M   = self.n_clients
        self.eps = self.algo_params.eps

        print("\n>>> FedExp Server initialized...\n")


    def _aggregation(self, w, ns):
        """Average locally trained model parameters"""

        # Get proportion
        prop = torch.tensor(ns, dtype=torch.float)
        if self.data_distributed["test_loader"]["local"]==None:#lda setting
            prop /= torch.sum(prop)
        
        else:
            prop = torch.ones_like(prop, dtype=torch.float)
            prop /= torch.sum(prop)
      
        state_prev = copy.deepcopy(self.model.state_dict())

        # Get gradient vectors and their norms
        grad_list = []
        grad_norm_list = []
        for i in range(len(w)):
            grad = {}
            for k in state_prev.keys():
                grad[k] = w[i][k] - state_prev[k].to(self.device)
            
            grad_list.append(grad)
            grad_norm_list.append(self._get_state_dict_2norm(grad))

        # Calculate norms
        grad_norm_avg = np.average(grad_norm_list)

        grad_avg = self._get_copied_averaged_weight(grad_list, prop)
        grad_avg_norm = self._get_state_dict_2norm(grad_avg)

        # Calculate global eta
        eta_g = min(1, (0.5 * grad_norm_avg / (grad_avg_norm + self.M * self.eps)))

        state_update = {}
        for k in grad_avg.keys():
            state_update[k] = eta_g * grad_avg[k] + state_prev[k].to(self.device)                 

        return copy.deepcopy(state_update)


    def _get_copied_averaged_weight(self, w, prop):
        w_avg = copy.deepcopy(w[0])
        for k in w_avg.keys():
            w_avg[k] = w_avg[k] * prop[0]

        for k in w_avg.keys():
            for i in range(1, len(w)):
                w_avg[k] += w[i][k] * prop[i]

        return w_avg

    def _get_state_dict_2norm(self, state_dict):
        norm2 = 0
        for k in state_dict.keys():
            norm2 += torch.norm(state_dict[k]) ** 2

        return math.sqrt(norm2)