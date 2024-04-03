#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6

import copy
import pickle
import numpy as np
import pandas as pd
import torch

from utils.options import args_parser
from utils.train_utils import get_data, get_model, record_net_data_stats
from models.Update import LocalUpdate, LocalUpdatePerFedAvg
from models.test import test_img, test_img_local, test_img_local_all
from models.Fed import FedAvg
import os
import logging
import random
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
    algo_dir = "per_fedavg"
    
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


    # build a global model
    net_glob = get_model(args)
    net_glob.train()

    # build local models
    net_local_list = []
    for user_idx in range(args.num_users):
        net_local_list.append(copy.deepcopy(net_glob))
    
    # training
    results_save_path = os.path.join(base_dir, algo_dir, 'results.csv')

    loss_train = []
    net_best = None
    best_loss = None
    best_acc = None
    best_epoch = None

    lr = args.lr
    results = []
    w_glob = None
    
    for iter in range(args.epochs):
        loss_locals = []
        m = max(int(args.frac * args.num_users), 1)
        idxs_users = np.random.choice(range(args.num_users), m, replace=False)
        # print("Round {}, lr: {:.6f}, {}".format(iter, lr, idxs_users))
        
        w_locals = []

        # local updates
        for idx in idxs_users:
            local = LocalUpdatePerFedAvg(args=args, dataset=dataset_train, idxs=dict_users_train[idx])
            w, loss = local.train(net=copy.deepcopy(net_glob).to(args.device), lr=lr, beta=0.1)
            w_locals.append(copy.deepcopy(w))
            loss_locals.append(copy.deepcopy(loss))
            
        # update global weights
        w_glob = FedAvg(w_locals)
        net_glob.load_state_dict(w_glob)
        
        # -- Evaluation -- #
        # copy weight to net_glob (broadcast)
        for user_idx in range(args.num_users):
            net_local_list[user_idx].load_state_dict(w_glob, strict=False)
        
        if (iter + 1) in [args.epochs//2, (args.epochs*3)//4]:
            lr *= 0.1
            
        # print loss
        loss_avg = sum(loss_locals) / len(loss_locals)
        loss_train.append(loss_avg)
        
        # SGD one step with testset
        for user_idx in range(args.num_users):
            local = LocalUpdatePerFedAvg(args=args, dataset=dataset_test, idxs=dict_users_test[idx])
            w = local.one_sgd_step(net=copy.deepcopy(net_local_list[user_idx]).to(args.device), lr=lr, beta=0.1)
            net_local_list[user_idx].load_state_dict(w)

        # fine-tuning
        if args.fine_tuning:
            local_ep_backup = args.local_ep
            args.local_ep = args.ft_ep
            
            for user_idx in range(args.num_users):
                local = LocalUpdate(args=args, dataset=dataset_train, idxs=dict_users_train[idx])
                w, loss = local.train(net=copy.deepcopy(net_local_list[user_idx]).to(args.device), body_lr=lr, head_lr=lr)
                net_local_list[user_idx].load_state_dict(w)
            
            args.local_ep = local_ep_backup
        

        if (iter + 1) % args.test_freq == 0:
            acc_test_mean, acc_test_std, loss_test = test_img_local_all(net_local_list, args, dataset_test, dict_users_test, return_all=False)
            
            print('Round {:3d}, Test loss {:.3f}, Test accuracy (mean): {:.2f}, Test accuracy (std): {:.2f}'.format(
                iter, loss_test, acc_test_mean, acc_test_std))

            if best_acc is None or acc_test_mean > best_acc:
                net_best = copy.deepcopy(net_glob)
                best_acc = acc_test_mean
                best_epoch = iter
                
#                 for user_idx in range(args.num_users):
#                     best_save_path = os.path.join(base_dir, algo_dir, 'best_local_{}.pt'.format(user_idx))
#                     torch.save(net_local_list[user_idx].state_dict(), best_save_path)

            results.append(np.array([iter, loss_test, acc_test_mean, acc_test_std, best_acc]))
            final_results = np.array(results)
            final_results = pd.DataFrame(final_results, columns=['epoch', 'loss_test', 'acc_test(mean)', 'acc_test(std)', 'best_acc'])
            final_results.to_csv(results_save_path, index=False)
        
        # rollback global model
        for user_idx in range(args.num_users):
            net_local_list[user_idx].load_state_dict(w_glob, strict=False)

    print('Best model, iter: {}, acc: {}'.format(best_epoch, best_acc))