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
from models.Update import LocalUpdateAvg
from models.test import test_img_local, test_img_local_all_avg, test_img_global
import os

import pdb
import sys
import random
import time

import logging


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
    
    assert args.local_upt_part in ['body','full'] 
    args.device = torch.device('cuda:{}'.format(args.gpu) if torch.cuda.is_available() and args.gpu != -1 else 'cpu')
    
    print(args)
    
    if args.hetero_option=="shard":
        base_dir = './save/full_and_body/{}_iid{}_num{}_C{}_le{}_m{}_wd{}/shard{}/'.format(
            args.model, args.iid, args.num_users, args.frac, args.local_ep, args.momentum, args.wd, args.shard_per_user)
    elif args.hetero_option=="lda":
        base_dir = './save/full_and_body/{}_iid{}_num{}_C{}_le{}_m{}_wd{}/alpha{}/'.format(
            args.model, args.iid, args.num_users, args.frac, args.local_ep, args.momentum, args.wd, args.alpha)

    algo_dir = '{}/fn_{}/seed_{}/local_upt_{}_lr_{}'.format(args.fl_alg, args.fn, args.seed, args.local_upt_part, args.lr)
    
    print("base_dir:", base_dir)
    print("algo_dir:", algo_dir)
    if not os.path.exists(os.path.join(base_dir, algo_dir)):
        os.makedirs(os.path.join(base_dir, algo_dir), exist_ok=True)#exist_ok=True: 디렉토리가 없으면 새로 만들고 없으면 아무 일 없는거임!!
        
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
    net_glob = get_model(args) #global model 그자체!!
    net_glob.train()

    # build local models
    net_global_storage = []
    net_global_storage.append(copy.deepcopy(net_glob))
    
    # training
    results_save_path = os.path.join(base_dir, algo_dir, 'results.csv')

    loss_train = []
    net_best = None
    best_loss = None
    best_acc = None
    best_epoch = None

    lr = args.lr
    results = []
    
    for iter in range(args.epochs):
        
        w_glob = None
        loss_locals = []
        data_size=[]
        
        # Client Sampling
        m = max(int(args.frac * args.num_users), 1)
        idxs_users = np.random.choice(range(args.num_users), m, replace=False)
        print("Round {}, lr: {:.6f}, {}".format(iter, lr, idxs_users))

        # Local Updates
        
        for idx in idxs_users:
            local = LocalUpdateAvg(args=args, dataset=dataset_train, idxs=dict_users_train[idx])
            net_local = copy.deepcopy(net_global_storage[0])
            
            if args.local_upt_part == 'body':
                w_local, loss, train_size = local.train(net=net_local.to(args.device), body_lr=lr, head_lr=0.)
            if args.local_upt_part == 'head':
                w_local, loss, train_size = local.train(net=net_local.to(args.device), body_lr=0., head_lr=lr)
            if args.local_upt_part == 'full':
                w_local, loss, train_size = local.train(net=net_local.to(args.device), body_lr=lr, head_lr=lr)
                
            loss_locals.append(copy.deepcopy(loss))
            data_size.append(train_size)

            if w_glob is None:
                w_glob = copy.deepcopy(w_local)
                for k in w_local.keys():
                    w_glob[k] *=train_size

            else:
                for k in w_glob.keys():
                    w_glob[k] += w_local[k]*train_size
        
        # Aggregation
        for k in w_glob.keys():
            w_glob[k] = torch.div(w_glob[k], sum(data_size))##global model의 state_dict!!
        
        
        # Broadcast
        net_global_storage[0].load_state_dict(w_glob, strict=True)
            
        
        if (iter + 1) in [args.epochs//2, (args.epochs*3)//4]:
            lr *= 0.1

        # print loss
        loss_avg = sum(loss_locals) / len(loss_locals)
        loss_train.append(loss_avg)#selected된 클라이언트들의 whole train dataset기준 averaged된 loss  기재!!

        if (iter + 1) % args.test_freq == 0:
            if args.hetero_option=="lda":
                acc_test, loss_test = test_img_global(net_global_storage[0], dataset_test, args)
            else: 
                acc_test, loss_test = test_img_local_all_avg(net_global_storage, args, dataset_test, dict_users_test, return_all=False)
                        
            print('Round {:3d}, Average loss {:.3f}, Test loss {:.3f}, Test accuracy: {:.2f}'.format(
                iter, loss_avg, loss_test, acc_test))

            if best_acc is None or acc_test > best_acc:
                net_best = copy.deepcopy(net_glob)
                best_acc = acc_test
                best_epoch = iter
                
                best_save_path = os.path.join(base_dir, algo_dir, 'best_model.pt')
                
                torch.save(net_global_storage[0].state_dict(), best_save_path)
                
            results.append(np.array([iter, loss_avg, loss_test, acc_test, best_acc]))
            final_results = np.array(results)
            final_results = pd.DataFrame(final_results, columns=['epoch', 'loss_avg', 'loss_test', 'acc_test', 'best_acc'])
            final_results.to_csv(results_save_path, index=False)
            
            

    print('Best model, iter: {}, acc: {}'.format(best_epoch, best_acc)) #finetuning은 아직 안한 상태!!
