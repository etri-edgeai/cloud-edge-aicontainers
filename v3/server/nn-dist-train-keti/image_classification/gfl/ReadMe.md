# Global Federated Learning (GFL) Algorithms Codebase

This repository is designed mainly for research, and pytorch implementation of GFL algorithms.  

We implemented various FL algorithms in our framework: 
- **FedAVG**, **Scaffold**, **Fedprox**, **FedNova**, **FedEXP**, and **FedNTD (Ours)**.
## Installation

First check that the requirements are satisfied:</br>
Python 3.7.16</br>
pytorch 1.12.0</br>
torchvision 0.13.0</br>
numpy 1.21.5</br>
matplotlib 3.5.3</br>
Pillow 9.4.0</br>

The next step is to clone the repository:
```bash
git clone https://github.com/etri-edgeai/nn-dist-train.git
```
Then, change the directory.
```bash
cd image_classification/gfl
```


The logs are uploaded to the wandb server. If you do not have a wandb account, just install and use as offline mode.
```
pip install wandb
wandb off
```
## Data & Model

We run GFL algorithms experiments on (CIFAR10, VGG11) and (CIFAR100, mobileNet).

Before starting the implementation, first download cifar10 and cifar100 using the following method:

```
sh generate_cifar.sh
```
## How to Run Codes?

The configuration skeleton for each algorithm is in `./config/*.json`. 
- `python ./main.py --config_path ./config/algorithm_name.json` conducts the experiment with the default setups.

There are two ways to change the configurations:
1. Change (or Write a new one) the configuration file in `./config` directory with the above command.
2. Use parser arguments to overload the configuration file.
- `--dataset_name`: name of the datasets (e.g., `mnist`, `cifar10`, `cifar100` or `cinic10`).
  - for cinic-10 datasets, the data should be downloaded first using `./data/cinic10/download.sh`.
- `--n_clients`: the number of total clients (default: 100).
- `--batch_size`: the size of batch to be used for local training. (default: 50)
- `--partition_method`: non-IID partition strategy (e.g. `sharding`, `lda`).
- `--partition_s`: shard per user (only for `sharding`).
- `--partition_alpha`: concentration parameter alpha for latent Dirichlet Allocation (only for `lda`).
- `--model_name`: model architecture to be used (e.g., `fedavg_mnist`, `fedavg_cifar`, or `mobile`).
- `--n_rounds`: the number of total communication rounds. (default: `200`)
- `--sample_ratio`: fraction of clients to be ramdonly sampled at each round (default: `0.1`)
- `--local_epochs`: the number of local epochs (default: `5`).
- `--lr`: the initial learning rate for local training (default: `0.01`)
- `--momentum`: the momentum for SGD (default: `0.9`).
- `--wd`: weight decay for optimization (default: `1e-5`)
- `--algo_name`: algorithm name of the experiment (e.g., `fedavg`, `fedntd`)
- `--seed`: random seed


## Script for running example

###  (CIFAR10, VGG11) Experiment
- FedAVG
	- Shard Setting
		- Run `sh fedavg_cifar10_shard.sh`.
	- LDA Setting
		- Run `sh fedavg_cifar10_lda.sh`.

- FedNTD 
	- Shard Setting
		- Run `sh fedntd_cifar10_shard.sh`.
	- LDA Setting
		- Run `sh fedntd_cifar10_lda.sh`.


- Scaffold
	- Shard Setting
		- Run `sh scaffold_cifar10_shard.sh`.
	- LDA Setting
		- Run `sh scaffold_cifar10_lda.sh`.

	
	
- FedEXP
	- Shard Setting
		- Run `sh fedexp_cifar10_shard.sh`.
	- LDA Setting
		- Run `sh fedexp_cifar10_lda.sh`.

###  (CIFAR100, mobileNet) Experiment
- FedAVG
	- Shard Setting
		- Run `sh fedavg_cifar100_shard.sh`.
	- LDA Setting
		- Run `sh fedavg_cifar100_lda.sh`.

- Scaffold
	- Shard Setting
		- Run `sh scaffold_cifar100_shard.sh`.
	- LDA Setting
		- Run `sh scaffold_cifar100_lda.sh`.

	
- FedNTD 
	- Shard Setting
		- Run `sh fedntd_cifar100_shard.sh`.
	- LDA Setting
		- Run `sh fedntd_cifar100_lda.sh`.
	
- FedEXP
	- Shard Setting
		- Run `sh fedexp_cifar100_shard.sh`.
	- LDA Setting
		- Run `sh fedexp_cifar100_lda.sh`.


## Experiment Results
Below is an example of experimental results conducted in the (CIFAR10, VGG11) setting:

We utilized momentum SGD with an initial learning rate of 0.01, setting the momentum to 0.9, and applying a weight decay of 1e-5.

All experiments were carried out over 320 rounds to comprehensively evaluate model performance and convergence behavior. To ensure effective convergence during training, we decreased the learning rate by 0.1 at both the halfway mark and three-quarters of the federated learning rounds.



 
| Algorithm              | shard  2  | shard  5  | shard  10 | lda  0.1 | lda  0.5 | lda  1.0 |
|------------------------|------------|------------|------------|----------|----------|----------|
| FedAVG             | 65.42      | 79.95      | 83.18      | 61.5    | 80.98    | 82.1    |
| **FedNTD (Ours)**           | 70.63      | 80.22      | 82.78      | 68.44    | 81.53    | 82.17    |




## Contact
Feel free to contact us if you have any questions:)

- Seongyoon Kim: curisam@kaist.ac.kr


# Acknowledgements

This codebase was adapted from https://doc.fedml.ai/ and https://github.com/Lee-Gihun/FedNTD/.

