
# Personalized Federated Learning (PFL) Algorithms Codebase

This repository is designed mainly for research, and pytorch implementation of PFL algorithms.  

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
Finally, change the directory.
```bash
cd image_classification/pfl
```
## Data & Model

We run PFL algorithms experiments on CIFAR100 using mobileNet.

## Script for running
###  1-step Algorithms
- Local only
	- Run `sh run_local.sh`.
	
- FedPer
	- Run `sh run_per_fedavg.sh`.
		
- Per-FedAVG
	- Run `sh run_per_fedavg.sh`.

- FedRep
	- Run `sh run_per_fedavg.sh`.
	


###  2-step Algorithms
- FedAVG-FT
	- Run the   `sh run_fedavg.sh` script followed by executing `FedAVG-FT.ipynb` in sequence.

- FedBABU-FT
	- Run the   `sh run_fedbabu.sh` script followed by executing `FedBABU-FT.ipynb` in sequence.

- FedFN-FT
	- Run the   `sh run_fedfn.sh` script followed by executing `FedFN-FT.ipynb` in sequence.


## Experiment Results

| Algorithm              | shard  10  | shard  50  | shard  100 | lda  0.1 | lda  0.5 | lda  1.0 |
|------------------------|------------|------------|------------|----------|----------|----------|
| Local only             | 58.64      | 25.38      | 18.52      | 43.63    | 21.03    | 14.88    |
| FedPer (2019)          | 70.92      | 33.73      | 22.77      | 55.93    | 27.32    | 18.93    |
| Per-FedAVG (2020)      | 32.57      | 43.09      | 45.0       | 35.12    | 42.95    | 42.82    |
| FedRep (2021)          | 62.69      | 34.66      | 26.53      | 48.52    | 30.94    | 23.93    |
| FedAVG (2017)          | 36.63      | 40.51      | 43.18      | 33.70    | 39.91    | 41.36    |
| FedAVG-FT (2017)       | 70.39      | 43.54      | 44.08      | 55.06    | 45.07    | 43.66    |
| FedBABU (2022)         | 44.92      | 40.7       | 39.81      | 38.71    | 39.87    | 37.55    |
| FedBABU-FT (2022)            | 79.11      | 51.36      | 45.12      | 69.05    | 51.14    | 43.39    |
| FedFN (Ours)           | 47.23      | 49.72      | 51.33      | 41.30    | 45.73    | 44.00    |
| **FedFN-FT**           | **82.02**      | **54.72**      | **52.99**      | **69.50**    | **51.76**    | **46.85**    |





## Contact
Feel free to contact us if you have any questions:)

- Seongyoon Kim: curisam@kaist.ac.kr


# Acknowledgements

This codebase was adapted from https://github.com/pliang279/LG-FedAvg and https://github.com/jhoon-oh/FedBABU.
