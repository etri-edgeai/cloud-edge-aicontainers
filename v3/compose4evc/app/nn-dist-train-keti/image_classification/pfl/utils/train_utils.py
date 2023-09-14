from torchvision import datasets, transforms
from models.Nets import MobileNetCifar, MobileNetCifar_FN

from utils.sampling import iid, shard, lda, lda_test

import numpy as np
import sys

trans_mnist = transforms.Compose([transforms.ToTensor(),
                                  transforms.Normalize((0.1307,), (0.3081,))])
trans_cifar10_train = transforms.Compose([transforms.RandomCrop(32, padding=4),
                                          transforms.RandomHorizontalFlip(),
                                          transforms.ToTensor(),
                                          transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                               std=[0.229, 0.224, 0.225])])
trans_cifar10_val = transforms.Compose([transforms.ToTensor(),
                                        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                             std=[0.229, 0.224, 0.225])])



trans_cifar100_train = transforms.Compose([transforms.RandomCrop(32, padding=4),
                                          transforms.RandomHorizontalFlip(),
                                          transforms.ToTensor(),
                                          transforms.Normalize(mean=[0.507, 0.487, 0.441],
                                                               std=[0.267, 0.256, 0.276])])
trans_cifar100_val = transforms.Compose([transforms.ToTensor(),
                                         transforms.Normalize(mean=[0.507, 0.487, 0.441],
                                                              std=[0.267, 0.256, 0.276])])

def get_data(args, env='fed'):
    if args.dataset == 'mnist':
        dataset_train = datasets.MNIST('data/mnist/', train=True, download=True, transform=trans_mnist)
        dataset_test = datasets.MNIST('data/mnist/', train=False, download=True, transform=trans_mnist)
        if args.iid==True:
            dict_users_train = iid(dataset_train, args.num_users)
            dict_users_test = iid(dataset_test, args.num_users)
            
        else:
            if args.hetero_option=="shard":
                dict_users_train, rand_set_all = shard(dataset_train, args.num_users, args.shard_per_user)
                dict_users_test, rand_set_all = shard(dataset_test, args.num_users, args.shard_per_user, rand_set_all=rand_set_all)
            elif args.hetero_option=="lda":
                dict_users_train = lda(dataset_train, args.num_users, args.alpha)
                dict_users_test = lda_test(dataset_train, dataset_test, args.num_users, dict_users_train)
    elif args.dataset == 'cifar10':
        dataset_train = datasets.CIFAR10('data/cifar10', train=True, download=True, transform=trans_cifar10_train)
        dataset_test = datasets.CIFAR10('data/cifar10', train=False, download=True, transform=trans_cifar10_val)
        if args.iid==True:
            dict_users_train = iid(dataset_train, args.num_users)
            dict_users_test = iid(dataset_test, args.num_users)
            
        else:
            if args.hetero_option=="shard":
                dict_users_train, rand_set_all = shard(dataset_train, args.num_users, args.shard_per_user)
                dict_users_test, rand_set_all = shard(dataset_test, args.num_users, args.shard_per_user, rand_set_all=rand_set_all)
            elif args.hetero_option=="lda":
                dict_users_train = lda(dataset_train, args.num_users, args.alpha)
                dict_users_test = lda_test(dataset_train, dataset_test, args.num_users, dict_users_train)
            
    elif args.dataset == 'cifar100':
        dataset_train = datasets.CIFAR100('data/cifar100', train=True, download=True, transform=trans_cifar100_train)
        dataset_test = datasets.CIFAR100('data/cifar100', train=False, download=True, transform=trans_cifar100_val)
        if args.iid==True:
            dict_users_train = iid(dataset_train, args.num_users)
            dict_users_test = iid(dataset_test, args.num_users)
            
        else:
            if args.hetero_option=="shard":
                dict_users_train, rand_set_all = shard(dataset_train, args.num_users, args.shard_per_user)
                dict_users_test, rand_set_all = shard(dataset_test, args.num_users, args.shard_per_user, rand_set_all=rand_set_all)
            elif args.hetero_option=="lda":
                dict_users_train = lda(dataset_train, args.num_users, args.alpha)
                dict_users_test = lda_test(dataset_train, dataset_test, args.num_users, dict_users_train)
            
            
    else:
        exit('Error: unrecognized dataset')


    return dataset_train, dataset_test, dict_users_train, dict_users_test

def get_model(args):
    if args.fn:
        if args.model == 'mobile': 
            net_glob = MobileNetCifar_FN(args.num_classes, args.feature_norm).to(args.device)
            
    elif not args.fn:
        if args.model == 'mobile': 
            net_glob = MobileNetCifar(args.num_classes).to(args.device)

    else:
        exit('Error: unrecognized model')

    return net_glob



def record_net_data_stats(net_dataidx_map, all_targets):
    net_cls_counts = {}#각 client가 어떤 label을 몇개씩 가지고 있는지 통계량 기재!!

    for net_i, dataidx in net_dataidx_map.items():
        unq, unq_cnt = np.unique(all_targets[dataidx], return_counts=True)#전체 train data 중에 net_i번째 client가 가지고 있는 data가 어떤 label을 가지고 있는지의 정보가 unq, unq의 각 element가 몇개 들어있는지 기재하는게 unq_count이다!!
        tmp = {unq[i]: unq_cnt[i] for i in range(len(unq))}#tmp에는 unq가 key unq_count가 value가 되게 기재!!
        net_cls_counts[net_i] = tmp
    return net_cls_counts #각 client가 어떤 label을 몇개씩 가지고 있는지 통계량 기재!!
