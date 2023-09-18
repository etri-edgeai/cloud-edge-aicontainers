import torch
import torch.nn as nn
import numpy as np
import copy
import time
import wandb

from .measures import *

from train_tools.preprocessing.cifar10.loader import get_dataloader_cifar10
from train_tools.preprocessing.cifar100.loader import get_dataloader_cifar100


__all__ = ["BaseServer"]


DATA_LOADERS = {
    "cifar10": get_dataloader_cifar10,
    "cifar100": get_dataloader_cifar100,
}


# JPark
from collections import OrderedDict
import json

class BaseServer:
    def __init__(
        self,
        algo_params,
        model,
        data_distributed,
        optimizer,
        scheduler,
        n_rounds=200,
        sample_ratio=0.1,
        local_epochs=5,
        device="cuda:0",
    ):
        """
        Server class controls the overall experiment.
        """
        self.algo_params = algo_params
        self.num_classes = data_distributed["num_classes"]
        self.model = model
        self.criterion = nn.CrossEntropyLoss()
        self.data_distributed = data_distributed
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.sample_ratio = sample_ratio
        self.n_rounds = n_rounds
        self.device = device
        self.n_clients = len(data_distributed["local"].keys())
        self.local_epochs = local_epochs
        self.server_results = {
            "client_history": [],
            "test_accuracy": [], 
            "best_accuracy":[]
        }

    def run(self):
        """Run the FL experiment"""
        self._print_start()

        for round_idx in range(self.n_rounds):
            
            print(f'[d] Round index = {round_idx}')

            start_time = time.time()

            # Make local sets to distributed to clients
            sampled_clients = self._client_sampling(round_idx)
            print(f'[d] Index list of sampled_clients = {sampled_clients}')
            self.server_results["client_history"].append(sampled_clients)
            
            # Client training stage to upload weights & stats
            updated_local_weights, client_sizes, round_results = self._clients_training(
                sampled_clients
            )#round results: 모든 select된 local model들의 local train dataset 기준 train acc만!!(light version에서는 시간 줄이기 위함!!)
            
            
            # Get aggregated weights & update global
            ag_weights = self._aggregation(updated_local_weights, client_sizes)
            print(f'[d] type(ag_weights) = {type(ag_weights)}')
            print(f'[d] len(ag_weights) = {len(ag_weights)}')
            print(f'[d] ag_weights = {ag_weights}')
            
            with open('./tmp/ag_weights.json', 'w') as f:
                f.write(json.dumps(ag_weights))

            # Update global weights and evaluate statistics
            self._update_and_evaluate(ag_weights, round_results, round_idx, start_time)
            
        print("[Best Acc Ever] Best Acc - {:2.2f}".format(self.server_results["best_accuracy"][-1]))


    def _clients_training(self, sampled_clients):
        """Conduct local training and get trained local models' weights"""

        updated_local_weights, client_sizes = [], []
        round_results = {}

        server_weights = self.model.state_dict()

        server_optimizer = self.optimizer.state_dict()
        # Client training stage
        for client_idx in sampled_clients:
            # Fetch client datasets
            self._set_client_data(client_idx)

            # Download global            
            self.client.download_global(server_weights, server_optimizer)# server로부터 해당 round의 initial model, momentum, weightdecay, lr 따옴!
            # Local training
            local_results, local_size = self.client.train()#local model의 train acc(local data 기준), local data 갯수 반환!
            # Upload locals
            updated_local_weights.append(self.client.upload_local())

            # Update results
            round_results = self._results_updater(round_results, local_results)#select된 모든 client의 train acc(local data 기준)를 dictionary에 저장(light version)
            client_sizes.append(local_size)#select된 모든 client의 train data의 size들을 저장

            # Reset local model
            self.client.reset()

        return updated_local_weights, client_sizes, round_results #select된 client에 해당하는 local model, train data수, local model의 train acc(local data 기준)(light version)

    def _client_sampling(self, round_idx):
        """Sample clients by given sampling ratio"""

        clients_per_round = max(int(self.n_clients * self.sample_ratio), 1)
        sampled_clients = np.random.choice(
            self.n_clients, clients_per_round, replace=False
        )

        return sampled_clients


    def _set_client_data(self, client_idx):
        """Assign local client datasets."""
        self.client.datasize = self.data_distributed["local"][client_idx]["datasize"]
        self.client.train_idxs = self.data_distributed["local"][client_idx]["train_idxs"]
        self.client.test_idxs = self.data_distributed["local"][client_idx]["test_idxs"]
        self.client.data_name= self.data_distributed["data_name"]

    def _aggregation(self, w, ns):
        """Average locally trained model parameters"""
        
        if self.data_distributed["test_loader"]["local"]==None:#lda setting
        
            prop = torch.tensor(ns, dtype=torch.float)
            prop /= torch.sum(prop)
            w_avg = copy.deepcopy(w[0])
            for k in w_avg.keys():
                w_avg[k] = w_avg[k] * prop[0]

            for k in w_avg.keys():
                for i in range(1, len(w)):
                    w_avg[k] += w[i][k] * prop[i]

        
        else:
            w_avg = copy.deepcopy(w[0])
            for k in w_avg.keys():
                for i in range(1, len(w)):
                    w_avg[k] += w[i][k] 

            for k in w_avg.keys():
                w_avg[k] = torch.div(w_avg[k], len(w))##global model의 state_dict!!
                 

        return copy.deepcopy(w_avg)
    
    

    def _results_updater(self, round_results, local_results):#round_results: 해당 client이전의 selected된 client들의 statistic 기술한 dictionary, local_results: 업데이트할 client에서 얻어진 local model의 train acc(local data 기준) (light version!!)
        """Combine local results as clean format"""

        for key, item in local_results.items():
            if key not in round_results.keys():
                round_results[key] = [item]
            else:
                round_results[key].append(item)

        return round_results

    def _print_start(self):
        """Print initial log for experiment"""

        if self.device == "cpu":
            return "cpu"

        if isinstance(self.device, str):
            device_idx = int(self.device[-1])#0
        elif isinstance(self.device, torch._device):
            device_idx = self.device.index#0

        device_name = torch.cuda.get_device_name(device_idx)
        print("")
        print("=" * 50)
        print("Train start on device: {}".format(device_name))#A100-PCIE-40GB
        print("=" * 50)

    def _print_stats(self, round_results, test_accs, round_idx, round_elapse, best_accs): #터미널 창에서 띄우는 것 
        
        print(
            "[Round {}/{}] Elapsed {}s (Current Time: {})".format(
                round_idx + 1,
                self.n_rounds,
                round(round_elapse, 1),
                time.strftime("%H:%M:%S"),
            )
        )
        
        print(
            "[Local Stat (Train Acc)]: {}, Avg - {:2.2f} (std {:2.2f})".format(
                round_results["train_acc"],
                np.mean(round_results["train_acc"]),
                np.std(round_results["train_acc"]),
            )
        )
        
        
        
#         print(
#             "[Local Stat (Train Loss)]: {}, Avg - {:2.2f} (std {:2.2f})".format(
#                 round_results["avg_loss"],
#                 np.mean(round_results["avg_loss"]),
#                 np.std(round_results["avg_loss"]),
#             )
#         )

#         print(
#             "[Local Stat (Test Acc)]: {}, Avg - {:2.2f} (std {:2.2f})".format(
#                 round_results["test_acc"],
#                 np.mean(round_results["test_acc"]),
#                 np.std(round_results["test_acc"]),
#             )
#         )

        print("[Server Stat] Acc - {:2.2f}".format(test_accs))
        print("[Server Stat] Best Acc - {:2.2f}".format(best_accs))
    

    def _wandb_logging(self, round_results, round_idx):#wandb log 용(plot)
        """Log on the W&B server"""

        # Local round results
#         local_results = {
#             "local_train_acc": np.mean(round_results["train_acc"]),
#             "local_test_acc": np.mean(round_results["test_acc"]),
#         }
#         wandb.log(local_results, step=round_idx)#local model statistic

        # Server round results
        server_results = {"server_test_acc": self.server_results["test_accuracy"][-1]}
        wandb.log(server_results, step=round_idx)#global model statistic
        server_best_results = {"server_best_acc": self.server_results["best_accuracy"][-1]}
        wandb.log(server_best_results, step=round_idx)#global model statistic

    def _update_and_evaluate(self, ag_weights, round_results, round_idx, start_time):
        """Evaluate experiment statistics."""

        # Update Global Server Model
        self.model.load_state_dict(ag_weights)

        # Measure Accuracy Statistics
        
        
        if self.data_distributed["test_loader"]["local"] is None:
            self.testloader=self.data_distributed["test_loader"]["global"]
            
            test_acc = evaluate_model(
                self.model, self.testloader, device=self.device
            )#.measures/predictions.py에 있음
        else:
            acc_test_local = np.zeros(self.n_clients)
            for client in range(self.n_clients):
                self.testloader=self.data_distributed["test_loader"]["local"][client]
                acc_test_local[client]=evaluate_model(self.model, self.testloader, device=self.device)
            test_acc=acc_test_local.mean()


            
        self.server_results["test_accuracy"].append(test_acc)
        
        if round_idx==0:
            self.server_results["best_accuracy"].append(test_acc)
            
            
        elif test_acc > self.server_results["best_accuracy"][-1]:  
            self.server_results["best_accuracy"].append(test_acc)
            
        else:
            self.server_results["best_accuracy"].append(self.server_results["best_accuracy"][-1])


        # Change learning rate
        if self.scheduler is not None:
            self.scheduler.step()

        round_elapse = time.time() - start_time

        # Log and Print
        self._wandb_logging(round_results, round_idx)#local_train_loss 띄움(light version)
        
        
        self._print_stats(round_results, test_acc, round_idx, round_elapse, self.server_results["best_accuracy"][-1])
        print("-" * 50)
