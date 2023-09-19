import torch
from torch.utils.data import DataLoader
from collections import Counter

import random
import numpy as np
import os
import logging
import pickle


from .cifar10.loader import get_all_targets_cifar10, get_dataloader_cifar10
from .cifar100.loader import get_all_targets_cifar100, get_dataloader_cifar100

__all__ = ["data_distributer"]


logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


DATA_INSTANCES = {
    "cifar10": get_all_targets_cifar10,
    "cifar100": get_all_targets_cifar100,
}

DATA_LOADERS = {
    "cifar10": get_dataloader_cifar10,
    "cifar100": get_dataloader_cifar100,
}



def data_distributer(
    root,
    dataset_name,
    batch_size,
    n_clients,
    partition
):
    """
    Distribute dataloaders for server and locals by the given partition method.
    """

    root = os.path.join(root, dataset_name)
    all_targets_train = DATA_INSTANCES[dataset_name](root)
    all_targets_test = DATA_INSTANCES[dataset_name](root, train=False)
    
    
    num_classes = len(np.unique(all_targets_train))
    net_dataidx_map_test = None

    local_info = {
        i: {"datasize": 0, "train_idxs": None, "test_idxs": None} for i in range(n_clients)
    }
    
    print(partition)

    if partition.method == "iid":
        net_dataidx_map = iid_partition(all_targets_train, n_clients)
        net_dataidx_map_test = iid_partition(all_targets_test, n_clients)
        
    elif partition.method == "sharding" or partition.method == "sharding_new":
        print('here')
        net_dataidx_map, rand_set_all = sharding_partition(all_targets_train, n_clients, partition.shard_per_user)
        net_dataidx_map_test, rand_set_all = sharding_partition(all_targets_test, n_clients, partition.shard_per_user, rand_set_all=rand_set_all)
        
    elif partition.method == "lda":
        net_dataidx_map = lda_partition(all_targets_train, n_clients, partition.alpha)
        
    else:
        raise NotImplementedError
        
    #Use the given setting
    if partition.method == "iid":
        dict_save_path = 'train_tools/preprocessing/dict_users_10_iid.pkl'
        with open(dict_save_path, 'rb') as handle:#기존 pretrained되었을 때 쓰였던 클라이언트 구성으로 덮어씌운다.
            net_dataidx_map, net_dataidx_map_test = pickle.load(handle)
    
    elif partition.method == "sharding":    
        dict_save_path = 'train_tools/preprocessing/dict_users_{}_{}.pkl'.format(num_classes, partition.shard_per_user)

        with open(dict_save_path, 'rb') as handle:#기존 pretrained되었을 때 쓰였던 클라이언트 구성으로 덮어씌운다.
            net_dataidx_map, net_dataidx_map_test = pickle.load(handle)
            
    elif partition.method == "sharding_new":
        dict_save_path = 'train_tools/preprocessing/dict_users_10_2_new.pkl'

        with open(dict_save_path, 'rb') as handle:#기존 pretrained되었을 때 쓰였던 클라이언트 구성으로 덮어씌운다.
            net_dataidx_map, net_dataidx_map_test = pickle.load(handle)

            
    elif partition.method == "lda":    
        dict_save_path = 'train_tools/preprocessing/dict_users_lda_{}_{}.pkl'.format(partition.alpha, num_classes)

        with open(dict_save_path, 'rb') as handle:#기존 pretrained되었을 때 쓰였던 클라이언트 구성으로 덮어씌운다.
            net_dataidx_map, net_dataidx_map_test = pickle.load(handle)
        
    print(">>> Distributing client train data...")
    
    # Count class samples in Clients
    
    traindata_cls_dict = record_net_data_stats(net_dataidx_map, all_targets_train)
    
    logging.info('Data statistics: %s' % str(traindata_cls_dict))
    traindata_cls_counts = net_dataidx_map_counter(net_dataidx_map, all_targets_train)

    for client_idx, dataidxs in net_dataidx_map.items():
        local_info[client_idx]["datasize"] = len(dataidxs)
        local_info[client_idx]["train_idxs"] = dataidxs
        
    if partition.method == "sharding":
        for client_idx, dataidxs in net_dataidx_map_test.items():
            local_info[client_idx]["test_idxs"] = dataidxs
            
    
    test_loader={"global": None, "local": None}
    
    test_loader["global"]=DATA_LOADERS[dataset_name](root=root, train=False, batch_size=100, dataidxs=None)
    
    if net_dataidx_map_test is not None:
        test_loader["local"]={}
        for i in range(n_clients):
            test_loader["local"][i]=DATA_LOADERS[dataset_name](root=root, train=False, batch_size=100, dataidxs=local_info[i]["test_idxs"])
            


    data_distributed = {
        "local": local_info,
        "data_map": traindata_cls_counts,
        "num_classes": num_classes,
        "data_name": dataset_name,
        "test_loader": test_loader 
            
    }

    return data_distributed



def iid_partition(all_targets, n_clients):
    labels = np.array(all_targets)
    length = int(len(labels) / n_clients)
    tot_idx = np.arange(len(labels))
    net_dataidx_map = {}

    for client_idx in range(n_clients):
        np.random.shuffle(tot_idx)
        data_idxs = tot_idx[:length]
        tot_idx = tot_idx[length:]
        net_dataidx_map[client_idx] = np.array(data_idxs)

    return net_dataidx_map


def sharding_partition(all_targets, n_clients, shard_per_user, rand_set_all=[]):
    
    net_dataidx_map, all_idxs = {i: np.array([], dtype='int64') for i in range(n_clients)}, [i for i in range(len(all_targets))]
    
    idxs_dict = {}#각 class candidate를 key 로 갖고 key에 해당하는 data idxs를 value로!!
    for i in range(len(all_targets)):
        label = torch.tensor(all_targets[i]).item()
#         label = dall_targets[i].clone().detach().item()
        if label not in idxs_dict.keys():
            idxs_dict[label] = []
        idxs_dict[label].append(i)    
        
    num_classes = len(np.unique(all_targets))
    
    shard_per_class = int(shard_per_user * n_clients / num_classes)#shard_per_class*num_classes 갯수의 shard를 구성할거임!!
    #idxs_dict[label]의 데이터를 label에 관계없이 동일한 shard 갯수로 쪼개기 위함!!, 각 클라이언트들은 shard_per_user 갯수만큼의 shard를 가질 것인데, idxs_dict[label]의 각 shard내의 데이타 수는 label에 따라 차별화 될 수 있음. 즉 label에 해당하는 데이타 갯수에 비례하게끔 shard 내의 데이타 수가 비례!! ex) class 1,2,...,10-> 각각 50개의 shard 가짐, class 1 데이타 갯수 500개, 5000개라면, class 1의 한 shard는 10개, class 10의 한 shard는 100개의 데이터 보유
    for label in idxs_dict.keys(): #idxs_dict[label]은 shard_per_class로 나누어떨어지지 않는 경우가 있어, 나누어떨어지지 않는 경우 최대한 균일하게 쪼개기 위해서 나머지를 1개씩 최종적으로 뿌리는 방식의 구현, cifar는 할 필요 없으나 mnist에는 적용되어야 함!!
        x = idxs_dict[label]#label에 해당하는 index set
        num_leftover = len(x) % shard_per_class #label마다 보유한 통일된 shard 수로 나눠서 나눈 나머지!!, 즉 남은 것들은 버릴 것이다.
        leftover = x[-num_leftover:] if num_leftover > 0 else []#찌꺼기 부분들!!
        x = np.array(x[:-num_leftover]) if num_leftover > 0 else np.array(x)
        x = x.reshape((shard_per_class, -1))#(shard_per_class, len(x)/shard_per_class)#이제는 찌꺼기 없이 나눠떨어지는 형태!!
        x = list(x)
        for i, idx in enumerate(leftover):
            x[i] = np.concatenate([x[i], [idx]])#0~찌꺼기 갯수-1번째 shard index까지 각각 찌꺼기 1개씩 붙여넣음!!
        idxs_dict[label] = x

    if len(rand_set_all) == 0:#train loader 구성시에 걸림!!
        rand_set_all = list(range(num_classes)) * shard_per_class#[0,1,num_classes-1]* shard_per_class, 우리는 전체 data를 shard_per_class*num_classes 갯수의 shard로 쪼갤 것이다!! 
        random.shuffle(rand_set_all)
        assert((shard_per_class*num_classes)%n_clients==0)
        rand_set_all = np.array(rand_set_all).reshape((n_clients, -1))#(n_clients,shard_per_class*num_classes/n_clients), shard_per_class*num_classes가 n_clients로 나누어떨어져야한다는 제약조건 존재!!
      
    
    # divide and assign
    for i in range(n_clients):
        rand_set_label = rand_set_all[i]
        rand_set = []
        for label in rand_set_label:
            idx = np.random.choice(len(idxs_dict[label]), replace=False)#shard 1개에 해당하는 idx
            rand_set.append(idxs_dict[label].pop(idx))#idxs_dict[label][idx] 지운것으로 변경->idxs_dict[label][idx] 지운것으로 변경, rand_set->idxs_dict[label][idx] 추가. i.e. rand_set는 shard 1개(array dataset index) 추가하며 indx_dict는 shard 1개(array dataset index) 지움!!
            
        net_dataidx_map[i] = np.concatenate(rand_set)#rand_set의 여러 array들을 concatenate하여 client i가 가질 data의 index들을 담은 리스트로 반환!!
        

    return net_dataidx_map, rand_set_all




def lda_partition(all_targets, n_clients, alpha):
    min_size = 0
    N, K = len(all_targets), len(np.unique(all_targets))
    
    labels = all_targets
    unique_classes = np.unique(labels)
    length = int(len(labels) / n_clients)
    net_dataidx_map = {}
    
    while min_size < 10:
        idx_batch = [[] for _ in range(n_clients)]
        for k in range(K):
            # get a list of batch indexes which are belong to label k
            idx_k = np.where(all_targets == k)[0]
            
            idx_batch, min_size = partition_class_samples_with_dirichlet_distribution(
                N, alpha, n_clients, idx_batch, idx_k
            )

    for i in range(n_clients):
        np.random.shuffle(idx_batch[i])
        net_dataidx_map[i] = idx_batch[i]

    return net_dataidx_map


def partition_class_samples_with_dirichlet_distribution(
    N, alpha, client_num, idx_batch, idx_k
):
    np.random.shuffle(idx_k)
    proportions = np.random.dirichlet(np.repeat(alpha, client_num)) #probability vector
    # get the index in idx_k according to the dirichlet distribution
    proportions = np.array(
        [p * (len(idx_j) < N / client_num) for p, idx_j in zip(proportions, idx_batch)]
    )#이미 client k가 평균 갯수 이상의 데이타를 가지면 proportion 0으로 바꿔서 배정 안함
    proportions = proportions / proportions.sum()#다시 normalize
    proportions = (np.cumsum(proportions) * len(idx_k)).astype(int)[:-1]#idx_k개에서 몇개씩 잘라서 줄것인지에 대해 결정(분기점이라 total 개수-1개만 결정되면 됨, i.e. len=num_clients-1)

    # generate the batch list for each client
    idx_batch = [
        idx_j + idx.tolist()
        for idx_j, idx in zip(idx_batch, np.split(idx_k, proportions))
    ]#순서대로 정해진 갯수 잘라서 배정
    min_size = min([len(idx_j) for idx_j in idx_batch])

    return idx_batch, min_size




def net_dataidx_map_counter(net_dataidx_map, all_targets):
    data_map = [[] for _ in range(len(net_dataidx_map.keys()))]
    num_classes = len(np.unique(all_targets))

    prev_key = -1
    for key, item in net_dataidx_map.items():
        client_class_count = [0 for _ in range(num_classes)]
        class_elems = all_targets[item]
        for elem in class_elems:
            client_class_count[elem] += 1

        data_map[key] = client_class_count

    return np.array(data_map)


def record_net_data_stats(net_dataidx_map, all_targets):
    net_cls_counts = {}#각 client가 어떤 label을 몇개씩 가지고 있는지 통계량 기재!!

    for net_i, dataidx in net_dataidx_map.items():
        unq, unq_cnt = np.unique(all_targets[dataidx], return_counts=True)#전체 train data 중에 net_i번째 client가 가지고 있는 data가 어떤 label을 가지고 있는지의 정보가 unq, unq의 각 element가 몇개 들어있는지 기재하는게 unq_count이다!!
        tmp = {unq[i]: unq_cnt[i] for i in range(len(unq))}#tmp에는 unq가 key unq_count가 value가 되게 기재!!
        net_cls_counts[net_i] = tmp
    return net_cls_counts #각 client가 어떤 label을 몇개씩 가지고 있는지 통계량 기재!!
