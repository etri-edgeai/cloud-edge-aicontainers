import torch
import copy
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), "../../")))

from algorithms.BaseClientTrainer import BaseClientTrainer

from train_tools.preprocessing.cifar10.loader import get_dataloader_cifar10
from train_tools.preprocessing.cifar100.loader import get_dataloader_cifar100

__all__ = ["ClientTrainer"]

DATA_LOADERS = {
    "cifar10": get_dataloader_cifar10,
    "cifar100": get_dataloader_cifar100,
}

class ClientTrainer(BaseClientTrainer):
    def __init__(self, criterion, **kwargs):
        super(ClientTrainer, self).__init__(**kwargs)
        """
        ClientTrainer class contains local data and local-specific information.
        After local training, upload weights to the Server.
        """
        self.criterion = criterion

    def train(self):
        """Local training"""

        # Keep global model's weights
        self._keep_global()

        self.model.train()
        self.model.to(self.device)

        local_results = {}
        local_size = self.datasize
        root = os.path.join("./data", self.data_name)
        self.trainloader=DATA_LOADERS[self.data_name](root=root, train=True, batch_size=50, dataidxs=self.train_idxs)  

        for _ in range(self.local_epochs):
            for data, targets in self.trainloader:
                self.optimizer.zero_grad()

                # forward pass
                data, targets = data.to(self.device), targets.to(self.device)
                logits, dg_logits = self.model(data), self._get_dg_logits(data)
                loss = self.criterion(logits, targets, dg_logits)

                # backward pass
                loss.backward()
                self.optimizer.step()

        local_results = self._get_local_stats()

        return local_results, local_size

    def _get_dg_logits(self, data):
        with torch.no_grad():
            dg_logits = self.dg_model(data)

        return dg_logits
