#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6

import copy
import os
import pickle
import pandas as pd
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader

from utils.options import args_parser
from utils.train_utils import get_data, get_model, record_net_data_stats
from models.Update import DatasetSplit
from models.test import test_img_local, test_img_local_all, test_img_avg_all, test_img_ensemble_all
import random
import logging

import pdb

if __name__ == '__main__':
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # parse args
    args = args_parser()
    
    # Seed
    torch.manual_seed(args.seed)#args.running_idx=args.seed
    torch.cuda.manual_seed(args.seed)
    torch.backends.cudnn.deterministic=True
    torch.backends.cudnn.benchmark=False
    np.random.seed(args.seed)
    random.seed(args.seed)
    
    args.device = torch.device('cuda:{}'.format(args.gpu) if torch.cuda.is_available() and args.gpu != -1 else 'cpu')

    if args.hetero_option=="shard":
        base_dir = './save/{}_iid{}_num{}_C{}_le{}/shard{}/'.format(
            args.model, args.iid, args.num_users, args.frac, args.local_ep, args.shard_per_user)
    elif args.hetero_option=="lda":
        base_dir = './save/{}_iid{}_num{}_C{}_le{}/alpha{}/'.format(
            args.model, args.iid, args.num_users, args.frac, args.local_ep, args.alpha)
        
    algo_dir = "local"
    
    if not os.path.exists(os.path.join(base_dir, algo_dir)):
        os.makedirs(os.path.join(base_dir, algo_dir), exist_ok=True)

    dataset_train, dataset_test, dict_users_train, dict_users_test = get_data(args)
    
    
    if args.hetero_option=="shard":
        dict_save_path = 'dict_users_100_{}.pkl'.format(args.shard_per_user)
        with open(dict_save_path, 'rb') as handle:#기존 pretrained되었을 때 쓰였던 클라이언트 구성으로 덮어씌운다.
            dict_users_train, dict_users_test = pickle.load(handle)

    elif args.hetero_option=="lda":
        dict_save_path = 'dict_users_lda_{}_100_pfl.pkl'.format(args.alpha)
        with open(dict_save_path, 'rb') as handle:#기존 pretrained되었을 때 쓰였던 클라이언트 구성으로 덮어씌운다.
            dict_users_train, dict_users_test = pickle.load(handle)
            
    print(">>> Distributing client train data...")
        
    traindata_cls_dict = record_net_data_stats(dict_users_train, np.array(dataset_train.targets))
    logging.info('Data statistics: %s' % str(traindata_cls_dict))
    
    print(">>> Distributing client test data...")    
    testdata_cls_dict = record_net_data_stats(dict_users_test, np.array(dataset_test.targets))
    logging.info('Data statistics: %s' % str(testdata_cls_dict))
    
    print(args)
        
    # build model
    net_glob = get_model(args)
    net_glob.train()

    net_local_list = []
    for user_ix in range(args.num_users):
        net_local_list.append(copy.deepcopy(net_glob))

    # training
    results_save_path = os.path.join(base_dir, 'local/results.csv')

    loss_train = []
    net_best = None
    best_loss = None
    best_acc = None
    best_epoch = None

    lr = args.lr
    results = []

    criterion = nn.CrossEntropyLoss()

    for user, net_local in enumerate(net_local_list):
        model_save_path = os.path.join(base_dir, 'local/model_user{}.pt'.format(user))
        net_best = None
        best_acc = None

        ldr_train = DataLoader(DatasetSplit(dataset_train, dict_users_train[user]), batch_size=args.local_bs, shuffle=True)
        optimizer = torch.optim.SGD(net_local.parameters(), lr=lr, momentum=0.9, weight_decay=1e-5)
        scheduler = torch.optim.lr_scheduler.MultiStepLR(optimizer, milestones=[80, 120], gamma=0.1)
        
        for iter in range(args.epochs):
            for batch_idx, (images, labels) in enumerate(ldr_train):
                images, labels = images.to(args.device), labels.to(args.device)
                net_local.zero_grad()
                log_probs = net_local(images)

                loss = criterion(log_probs, labels)
                loss.backward()
                optimizer.step()
                
            scheduler.step()
            
            acc_test, loss_test = test_img_local(net_local, dataset_test, args, user_idx=user, idxs=dict_users_test[user])
            if best_acc is None or acc_test > best_acc:
                best_acc = acc_test
                net_best = copy.deepcopy(net_local)
                torch.save(net_local_list[user].state_dict(), model_save_path)
            
        net_local_list[user] = net_best
        
        
    acc_test_mean, acc_test_std, loss_test = test_img_local_all(net_local_list, args, dataset_test, dict_users_test, return_all=False)

    print('Test loss {:.3f}, Test accuracy (mean): {:.2f}, Test accuracy (std): {:.2f}'.format(loss_test, acc_test_mean, acc_test_std))

    final_results = np.array([[loss_test, acc_test_mean, acc_test_std]])
    final_results = pd.DataFrame(final_results, columns=['loss_test', 'acc_test(mean)', 'acc_test(std)'])
    final_results.to_csv(results_save_path, index=False)