#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6

import math
import random
from itertools import permutations
import numpy as np
import torch
import pdb
import sys


def iid(dataset, num_users): #중앙 서버에 shared data 부여하는 것만 추가!!
    """
    Sample I.I.D. client data from MNIST dataset
    :param dataset:
    :param num_users:
    :return: dict of image index
    
    """

    labels=np.array(dataset.targets)
    length = int(len(labels) / num_users)
    tot_idx = np.arange(len(labels))
    dict_users = {}

    for client_idx in range(num_users):
        np.random.shuffle(tot_idx)
        data_idxs = tot_idx[:length]
        tot_idx = tot_idx[length:]
        dict_users[client_idx] = np.array(data_idxs)

    return dict_users
    
    
    
    
def shard(dataset, num_users, shard_per_user, rand_set_all=[]):
    """
    Sample non-I.I.D client data from MNIST dataset
    :param dataset:
    :param num_users:
    :return:
    """
    dict_users, all_idxs = {i: np.array([], dtype='int64') for i in range(num_users)}, [i for i in range(len(dataset))]
    
    idxs_dict = {}#각 class candidate를 key 로 갖고 key에 해당하는 data idxs를 value로!!
    for i in range(len(dataset)):
        label = torch.tensor(dataset.targets[i]).item()
#         label = dataset.targets[i].clone().detach().item()
        if label not in idxs_dict.keys():
            idxs_dict[label] = []
        idxs_dict[label].append(i)    
        
    num_classes = len(np.unique(dataset.targets))
    
    shard_per_class = int(shard_per_user * num_users / num_classes)#shard_per_class*num_classes 갯수의 shard를 구성할거임!!
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
        assert((shard_per_class*num_classes)%num_users==0)
        rand_set_all = np.array(rand_set_all).reshape((num_users, -1))#(num_users,shard_per_class*num_classes/num_users), shard_per_class*num_classes가 num_users로 나누어떨어져야한다는 제약조건 존재!!
      
    
    # divide and assign
    for i in range(num_users):
        rand_set_label = rand_set_all[i]
        rand_set = []
        for label in rand_set_label:
            idx = np.random.choice(len(idxs_dict[label]), replace=False)#shard 1개에 해당하는 idx
            rand_set.append(idxs_dict[label].pop(idx))#idxs_dict[label][idx] 지운것으로 변경->idxs_dict[label][idx] 지운것으로 변경, rand_set->idxs_dict[label][idx] 추가. i.e. rand_set는 shard 1개(array dataset index) 추가하며 indx_dict는 shard 1개(array dataset index) 지움!!
            
        dict_users[i] = np.concatenate(rand_set)#rand_set의 여러 array들을 concatenate하여 client i가 가질 data의 index들을 담은 리스트로 반환!!
        

    return dict_users, rand_set_all

def lda(dataset_train, num_users, alpha): 
    """
    Sample non-I.I.D client data from MNIST dataset
    :param dataset:
    :param num_users:
    :param alpha:
    :return: dict of image index
    """
    min_size = 0
    all_targets=np.array(dataset_train.targets)
    N, K = len(all_targets), len(np.unique(all_targets))
    
    labels = all_targets
    unique_classes = np.unique(labels)
    dict_users = {}
    
    while min_size < 10:
        idx_batch = [[] for _ in range(num_users)]
        for k in range(K):
            # get a list of batch indexes which are belong to label k
            idx_k = np.where(all_targets == k)[0]
            
            idx_batch, min_size = partition_class_samples_with_dirichlet_distribution(
                N, alpha, num_users, idx_batch, idx_k
            )

    for i in range(num_users):
        np.random.shuffle(idx_batch[i])
        dict_users[i] = idx_batch[i]

    return dict_users


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


def lda_test(dataset_train, dataset_test, num_users, dict_train): 
    all_targets_train=np.array(dataset_train.targets)
    
    net_cls_counts = {}
    
    for net_i, dataidx in dict_train.items():
        unq, unq_cnt = np.unique(all_targets_train[dataidx], return_counts=True)#전체 train data 중에 net_i번째 client가 가지고 있는 data가 어떤 label을 가지고 있는지의 정보가 unq, unq의 각 element가 몇개 들어있는지 기재하는게 unq_count이다!!
        tmp = {unq[i]: unq_cnt[i] for i in range(len(unq))}#tmp에는 unq가 key unq_count가 value가 되게 기재!!
        net_cls_counts[net_i] = tmp

        
    K = len(np.unique(all_targets_train))
    all_targets=np.array(dataset_test.targets)
    
    dict_users = {}
    
    idx_batch = [[] for _ in range(num_users)]
    for i in range(num_users):
        for k in range(K):
            # get a list of batch indexes which are belong to label k
            idx_k = np.where(all_targets == k)[0]
            np.random.shuffle(idx_k)
            if k in net_cls_counts[i].keys():
                data_idxs = idx_k[:net_cls_counts[i][k]]
                idx_batch[i]+=data_idxs.tolist()
    for i in range(num_users):
        np.random.shuffle(idx_batch[i])
        dict_users[i] = idx_batch[i]

    return dict_users




