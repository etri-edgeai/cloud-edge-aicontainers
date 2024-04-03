import os
import time
import glob
import json
import random
import pandas as pd
import numpy as np

from constants import LANG_MAP_XNLI
np.random.seed(1)
random.seed(1)

labels = {
    "finance": 0,
    "entertainment": 1,
    "sports": 2,
    "news": 3,
    "autos": 4,
    "video": 5,
    "lifestyle": 6,
    "travel": 7,
    "health": 8,
    "foodanddrink": 9,
}

label ={
    "entailment":0,
    "neutral":1,
    "contradiction":2,
    "contradictory":2
}

def read_tsv(file_path: str, skip_first=False):
    data = []
    with open(file_path, "r") as fin:
        for idx, line in enumerate(fin):
            #print(idx,line)
            if skip_first and not idx:
                continue
            skip_flag = False
            segments = line.strip().split("\t")
            assert len(segments) == 5, segments
            if not skip_flag:
                data.append({
                    "input": segments[2] + segments[3], # combine news title with news body
                    "label": label[segments[4]],
                })
    return pd.DataFrame(data)

def read_xnli(file_path: str, skip_first=False):
    data = []
    with open(file_path, "r") as fin:
        print(file_path)
        for idx, line in enumerate(fin):
            #print(idx,line)
            if skip_first and not idx:
                continue
            skip_flag = False
            segments = line.strip().split("\t")
            assert len(segments) == 3, segments
            if not skip_flag:
                data.append({
                    "input": segments[0] + segments[1], # combine news title with news body
                    "label": label[segments[2].replace('"','')],
                })
    return pd.DataFrame(data)


def read_txt(file_path: str, skip_first=False):
    data = []
    with open(file_path, "r") as fin:
        for idx, line in enumerate(fin):
            if skip_first and not idx:
                continue
            skip_flag = False
            segments = line.strip().split("\t")
            assert len(segments) == 3, segments
            if not skip_flag:
                data.append({
                    "input": segments[0] + segments[1], # combine news title with news body
                    "label": label[segments[2].replace('"','')],
                })
    return pd.DataFrame(data)


# query \t news title \t news body \t news category
def gather_data():
    #num_for_train = 2000
    #num_for_dev_test = 500
    save_path = "splits_data"
    train_datasets = []
    dev_datasets = []
    test_datasets = []
    #lang_ids = ["de", "en", "es", "fr", "ru"]
    os.chdir('./create_data/make_xnli_data')
    print(os.getcwd())
    
    lang_ids =["ar","bg","de","el","en","es","fr","hi","ru","sw","th","tr","ur","vi","zh"]
    '''
    lang_ids =["ar1","ar2","ar3","ar4","bg1","bg2","bg3","bg4","de1","de2","de3","de4","el1","el2","el3","el4","en1","en2","en3","en4","es1","es2","es3","es4","fr1","fr2","fr3","fr4","hi1","hi2","hi3","hi4","ru1","ru2","ru3","ru4","sw1","sw2","sw3","sw4","th1","th2","th3","th4","tr1","tr2","tr3","tr4","ur1","ur2","ur3","ur4","vi1","vi2","vi3","vi4","zh1","zh2","zh3","zh4"]
    
        lang_ids =["ar1","ar2","ar3","ar4","ar5","ar6","ar7","ar8","bg1","bg2","bg3","bg4","bg5","bg6","bg7","bg8","de1","de2","de3","de4","de5","de6","de7","de8","el1","el2","el3","el4","el5","el6","el7","el8","en1","en2","en3","en4","en5","en6","en7","en8","es1","es2","es3","es4","es5","es6","es7","es8","fr1","fr2","fr3","fr4","fr5","fr6","fr7","fr8","hi1","hi2","hi3","hi4","hi5","hi6","hi7","hi8","ru1","ru2","ru3","ru4","ru5","ru6","ru7","ru8","sw1","sw2","sw3","sw4","sw5","sw6","sw7","sw8","th1","th2","th3","th4","th5","th6","th7","th8","tr1","tr2","tr3","tr4","tr5","tr6","tr7","tr8","ur1","ur2","ur3","ur4","ur5","ur6","ur7","ur8","vi1","vi2","vi3","vi4","vi5","vi6","vi7","vi8","zh1","zh2","zh3","zh4","zh5","zh6","zh7","zh8"]
    '''
    for lang_id in lang_ids:
    #for lang_id in LANG_MAP_XNLI.keys():
        train = read_xnli(f"xnli_translate_train/{lang_id}.train",skip_first=True)
        dev = read_xnli(f"xnli_dev/{lang_id}.dev")# test doesn't have labels / no train for other langs
        test = read_xnli(f"xnli_test/{lang_id}.test")
        
        train_datasets.append(train)
        dev_datasets.append(dev)
        test_datasets.append(test)
        
    # downsample training sets to simulate FL scenario
    for i, lang_id in enumerate(lang_ids):
    #for i, lang_id in enumerate(LANG_MAP_XNLI.keys()):
        print(lang_id, "saving to file")
        save_path = f"xnli/{lang_id}"
        if not os.path.isdir("xnli"):
            os.makedirs("xnli")

        #all_train_data = dev.sample(frac=1)
        #all_test_data = test.sample(frac=1)
        #train_sampled = all_train_data.iloc[:num_for_train]
        #dev = all_train_data.iloc[num_for_train:]
        
        
        train = train_datasets[i]
        dev = dev_datasets[i]
        test = test_datasets[i]
        
        train.to_csv(save_path + "_train.csv", index=None)
        dev.to_csv(save_path + "_dev.csv", index=None)
        test.to_csv(save_path + "_test.csv", index=None)
        
        #train_sampled.to_csv(save_path + "_train.csv", index=None)
        
        print(f"train_sampled shape {train.shape}")
        print(f"dev shape {dev.shape}")
        print(f"test shape {test.shape}")
        
    return {}

def gathering_data():
    #num_for_train = 61600
    #num_for_dev_test = 7700
    save_path = "splits_data"
    datasets = []
    #lang_ids = ["de", "en", "es", "fr", "ru"]
    lang_ids =["gov","tel","travel","slate","fic"]
    for lang_id in lang_ids:
        train = read_txt(f"./MNLI/{lang_id}.train",skip_first=True)# test doesn't have labels / no train for other langs
        datasets.append((lang_id, train))

    # downsample training sets to simulate FL scenario
    for (lang_id, train) in datasets:
        print(lang_id, "saving to file")
        save_path = f"mnli/{lang_id}"
        if not os.path.isdir("mnli"):
            os.makedirs("mnli")

        all_train_data = train.sample(frac=1)
        #all_test_data = test.sample(frac=1)
        train_sampled = all_train_data.iloc[:num_for_train]
        dev = all_train_data.iloc[num_for_train:num_for_train+num_for_dev_test]
        test = all_train_data.iloc[num_for_train+num_for_dev_test:]
        dev.to_csv(save_path + "_dev.csv", index=None)
        test.to_csv(save_path + "_test.csv", index=None)
        train_sampled.to_csv(save_path + "_train.csv", index=None)

        print(f"train_sampled shape {train_sampled.shape}")
        print(f"dev shape {dev.shape}")
        print(f"test shape {test.shape}")

    return {}


if __name__ == "__main__":
    data_w_text = gather_data()
