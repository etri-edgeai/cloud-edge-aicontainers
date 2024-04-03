import os
import glob
import random
import pickle
import copy
from collections import OrderedDict
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
import shutil

import numpy as np
import pandas as pd
import torch
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader

from transformers import DataCollatorForLanguageModeling, set_seed

set_seed(1)

from constants import MBART_MAP, MAP_LANG_MAP


class LineByLineTextDataset(torch.utils.data.Dataset):
    """
    Deprecated Huggingface Dataset
    """

    def __init__(self, tokenizer, file_path: str, block_size: int = 512, test_flag: int = 0, examples = None):
        if examples is not None:
            self.examples =  [torch.tensor(e, dtype=torch.long) for e in examples]
        else:
            if os.path.isfile(file_path) is False:
                raise ValueError(f"Input file path {file_path} not found")

            with open(file_path, encoding="utf-8") as f:
                lines = [line for line in f.read().splitlines() if (len(line) > 0 and not line.isspace())]
                if test_flag:
                    lines = lines[:test_flag]

            batch_encoding = tokenizer(lines, add_special_tokens=True, truncation=True, max_length=block_size)
            self.examples = batch_encoding["input_ids"]
            self.examples = [torch.tensor(e, dtype=torch.long) for e in self.examples]

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, i) -> Dict[str, torch.tensor]:
        return self.examples[i]


class MultilingualDataset(LineByLineTextDataset):
    """
    Loads CSV files in a directory where each file is a separate language
        Can be loaded by passing in `examples` where examples is a tuple of list of integers representing words and the language string
    """
    def __init__(self, tokenizer, file_path: str, split: str = "train", block_size: int = 512, test_flag: int = 0, examples = None, skip_langs: list = []):
        LANG_MAP = MAP_LANG_MAP[file_path]
        skip_langs = []
        if examples is not None:
            self.examples =  [(torch.tensor(e, dtype=torch.long), lang) for e, lang in examples if lang not in skip_langs]
        else:
            if os.path.isdir(file_path) is False:
                raise ValueError(f"Input file directory {file_path} not found")

            self.examples = []
            for lang_file_path in glob.glob(os.path.join(file_path, f"*_{split}.csv")):
                lang = lang_file_path.split("/")[-1].split("_")[0]
                if os.path.isfile(lang_file_path.replace(".csv", ".pkl")):
                    with open(lang_file_path.replace(".csv", ".pkl"), "rb") as fin:
                        examples = pickle.load(fin)
                else:
                    lines = pd.read_csv(lang_file_path, header=0, index_col=None)["text"].tolist()
                    if test_flag:
                        lines = lines[:test_flag]

                    batch_encoding = tokenizer(lines, add_special_tokens=True, truncation=True, max_length=block_size)
                    examples = batch_encoding["input_ids"]
                    # cache the tokenization to save time
                    with open(lang_file_path.replace(".csv", ".pkl"), "wb") as fout:
                        pickle.dump(examples, fout)
                
                examples = [(torch.tensor(e, dtype=torch.long), LANG_MAP[lang]) for e in examples]
                self.examples.extend(examples)


class MTDataset(LineByLineTextDataset):
    """
    Loads CSV files in a directory where each file is a separate language
        Can be loaded by passing in `examples` where examples is a tuple of two lists of integers representing words and the language string
    """
    def __init__(self, tokenizer, file_path: str, split: str = "train", block_size: int = 512, test_flag: int = 0, examples = None, skip_langs: list = []):
        LANG_MAP = MAP_LANG_MAP[file_path]
        skip_langs = []
        if examples is not None:
            self.examples =  [([torch.tensor(e, dtype=torch.long), torch.tensor(l, dtype=torch.long)], lang) for ((e, l), lang) in examples if lang not in skip_langs]
        else:
            if os.path.isdir(file_path) is False:
                raise ValueError(f"Input file directory {file_path} not found")

            self.examples = []
            for lang_file_path in glob.glob(os.path.join(file_path, f"*_{split}.csv")):
                lang = lang_file_path.split("/")[-1].split("_")[0]
                if os.path.isfile(lang_file_path.replace(".csv", ".pkl")):
                    with open(lang_file_path.replace(".csv", ".pkl"), "rb") as fin:
                        examples = pickle.load(fin)
                else:
                    data = pd.read_csv(lang_file_path, header=0, index_col=None)
                    if test_flag:
                        lines = lines[:test_flag]

                    all_examples = []

                    # order them according to direction we want
                    col_order = data.columns
                    for col_name in col_order:
                        tokenizer.src_lang = col_name
                        batch_encoding = tokenizer(data[col_name].tolist(), add_special_tokens=True, truncation=True, max_length=block_size)
                        examples = batch_encoding["input_ids"]
                        all_examples.append(examples)
                    
                    assert len(all_examples[0]) == len(all_examples[1])
                    examples = list(zip(*all_examples)) # both langs in each instance
                    # cache the tokenization to save time
                    with open(lang_file_path.replace(".csv", ".pkl"), "wb") as fout:
                        pickle.dump(examples, fout)
                
                examples = [([torch.tensor(e, dtype=torch.long), torch.tensor(l, dtype=torch.long)], LANG_MAP[lang]) for (e, l) in examples]
                self.examples.extend(examples)

class PAWSDataset(LineByLineTextDataset):
    """
    Loads CSV files in a directory where each file is a separate language
        Can be loaded by passing in `examples` where examples is a tuple of two lists of integers representing words and the language string
    """
    def __init__(self, tokenizer, file_path: str, split: str = "train", block_size: int = 512, test_flag: int = 0, examples = None, skip_langs: list = []):
        LANG_MAP = MAP_LANG_MAP[file_path]
        skip_langs = []
        if examples is not None:
            self.examples =  [([torch.tensor(e, dtype=torch.long), torch.tensor(l, dtype=torch.long)], lang) for ((e, l), lang) in examples if lang not in skip_langs]
        else:
            if os.path.isdir(file_path) is False:
                raise ValueError(f"Input file directory {file_path} not found")

            self.examples = []
            for lang_file_path in glob.glob(os.path.join(file_path, f"*_{split}.csv")):
                lang = lang_file_path.split("/")[-1].split("_")[0]
                if os.path.isfile(lang_file_path.replace(".csv", ".pkl")):
                    with open(lang_file_path.replace(".csv", ".pkl"), "rb") as fin:
                        examples = pickle.load(fin)
                else:
                    data = pd.read_csv(lang_file_path, header=0, index_col=None)
                    all_examples = []
                    # order them according to direction we want
                    sents1 = data["sentence1"].tolist()
                    sents2 = data["sentence2"].tolist()
                    for idx in range(len(data)):
                        tokenizer.src_lang = lang
                        encoding = tokenizer(sents1[idx], sents2[idx], add_special_tokens=True, truncation=True, max_length=block_size)
                        examples = encoding["input_ids"]
                        label = data.iloc[idx].label
                        all_examples.append((examples, int(label)))
                    
                    # cache the tokenization to save time
                    with open(lang_file_path.replace(".csv", ".pkl"), "wb") as fout:
                        pickle.dump(all_examples, fout)
                    examples = all_examples
                


                examples = [([torch.tensor(e, dtype=torch.long), torch.tensor(l, dtype=torch.long).unsqueeze(0)], LANG_MAP[lang]) for (e, l) in examples]
                self.examples.extend(examples)

        if test_flag:
            print(f"Using a debug run of {test_flag} examples")
            self.examples = self.examples[:test_flag]



class ClassificationDataset(LineByLineTextDataset):
    """
    Loads CSV files in a directory where each file is a separate language
        Can be loaded by passing in `examples` where examples is a tuple of two lists of integers representing words and the language string
    """
    def __init__(self, tokenizer, file_path: str, split: str = "train", block_size: int = 512, test_flag: int = 0, examples = None, skip_langs: list = []):
        LANG_MAP = MAP_LANG_MAP[file_path]
        skip_langs = []
        if examples is not None:
            self.examples =  [([torch.tensor(e, dtype=torch.long), torch.tensor(l, dtype=torch.long)], lang) for ((e, l), lang) in examples if lang not in skip_langs]
        else:
            if os.path.isdir(file_path) is False:
                raise ValueError(f"Input file directory {file_path} not found")

            self.examples = []
            for lang_file_path in glob.glob(os.path.join(file_path, f"*_{split}.csv")):
                lang = lang_file_path.split("/")[-1].split("_")[0]
                if os.path.isfile(lang_file_path.replace(".csv", ".pkl")):
                    with open(lang_file_path.replace(".csv", ".pkl"), "rb") as fin:
                        examples = pickle.load(fin)
                else:
                    data = pd.read_csv(lang_file_path, header=0, index_col=None)
                    all_examples = []

                    # order them according to direction we want
                    tokenizer.src_lang = lang
                    labels = data["label"].tolist()
                    sent = data["input"].tolist()
                    encoding = tokenizer(sent, add_special_tokens=True, truncation=True, max_length=block_size)
                    
                    #print(encoding1['input_ids'])
                    all_examples = list(zip(encoding["input_ids"], labels))
                    
                    # cache the tokenization to save time
                    with open(lang_file_path.replace(".csv", ".pkl"), "wb") as fout:
                        pickle.dump(all_examples, fout)
                    examples = all_examples
                examples = [([torch.tensor(e, dtype=torch.long), torch.tensor(l, dtype=torch.long).unsqueeze(0)], LANG_MAP[lang]) for (e,l) in examples]
                self.examples.extend(examples)
                
        if test_flag:
            print(f"Using a debug run of {test_flag} examples")
            self.examples = self.examples[:test_flag]

def get_dataset_type(path_to_data):
    is_multilingual = "wmt" in str(path_to_data) or "un_corpus" in str(path_to_data)
    is_mt = "mt_corpus" in str(path_to_data)
    is_paws = "pawsx" in str(path_to_data)
    is_qa = "qa" in str(path_to_data)
    if is_paws:
        dataset_type = PAWSDataset
    elif "nc" in str(path_to_data):
        dataset_type = ClassificationDataset
    elif "xnli" in str(path_to_data):
        dataset_type = ClassificationDataset
    elif "mnli" in str(path_to_data):
        dataset_type = ClassificationDataset
    elif "ag" in str(path_to_data):
        dataset_type = ClassificationDataset
    elif is_multilingual:
        dataset_type = MultilingualDataset
    elif is_mt:
        dataset_type = MTDataset
    elif is_qa:
        dataset_type = QuestionAnswerDataset
    else:
        dataset_type = LineByLineTextDataset
    return dataset_type


def get_dataset(path_to_data: Path, cid: str, partition: str):
    # generate path to cid's data
    path_to_data = path_to_data / cid / (partition + ".npy")
    data = np.load(path_to_data, allow_pickle=True)
    dataset_type = get_dataset_type(str(path_to_data))
    return dataset_type(None, "/".join(str(path_to_data).split("/")[:2]), examples=data.tolist())


def get_random_id_splits(total: int, val_ratio: float, shuffle: bool = True):
    """splits a list of length `total` into two following a
    (1-val_ratio):val_ratio partitioning.

    By default the indices are shuffled before creating the split and
    returning.
    """

    if isinstance(total, int):
        indices = list(range(total))
    else:
        indices = total

    split = int(np.floor(val_ratio * len(indices)))
    if not split:
        split = 1 # need at least 1 validation instance
    if shuffle:
        np.random.shuffle(indices)
    return indices[split:], indices[:split]


def make_collate_fn(tokenizer):
    def collate_fn(batch):
        tensors = pad_sequence(batch, batch_first=True, padding_value=tokenizer.pad_token_id)
        attn_mask = torch.ones_like(tensors)
        is_padding = tensors == tokenizer.pad_token_id
        attn_mask[is_padding] = 0 # is padding
        data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm_probability=0.15)
        output_batch = data_collator(tuple(tensors))
        output_batch["attention_mask"] = attn_mask
        return output_batch
    return collate_fn

def make_collate_fn_wlang(tokenizer):
    def collate_fn_wlang(batch):
        langs = torch.tensor([lang for (_, lang) in batch])
        batched_tensors = pad_sequence([num for (num, _) in batch], batch_first=True, padding_value=tokenizer.pad_token_id)
        attn_mask = torch.ones_like(batched_tensors)
        is_padding = batched_tensors == tokenizer.pad_token_id
        attn_mask[is_padding] = 0
        data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm_probability=0.15)
        output_batch = data_collator(tuple(batched_tensors))
        output_batch["langs"] = langs
        output_batch["attention_mask"] = attn_mask
        return output_batch
    return collate_fn_wlang

def make_collate_fn_mt_wlang(tokenizer):
    def collate_fn_mt_wlang(batch):
        langs = torch.tensor([lang for (_, lang) in batch])
        
        batched_input_tensors = pad_sequence([e for ((e,l), _) in batch], batch_first=True, padding_value=tokenizer.pad_token_id)
        
        attn_mask = torch.ones_like(batched_input_tensors)
        is_padding = batched_input_tensors == tokenizer.pad_token_id
        attn_mask[is_padding] = 0
        '''
        batched_input_tensor = torch.split(batched_input_tensors, 4)
        batched_input_tensor = torch.stack(batched_input_tensor)
        attn_mask = torch.split(attn_mask, 4)
        attn_mask = torch.stack(attn_mask)
        '''
        #batched_input_tensors=[batched_input_tensors1, batched_input_tensors2, batched_input_tensors3, batched_input_tensors4]
        
        #attn_mask = [attn_mask1, attn_mask2, attn_mask3, attn_mask4]
        batched_label_tensors = pad_sequence([l for ((e,l), _) in batch], batch_first=True, padding_value=tokenizer.pad_token_id)
        '''
        batched_label_tensor = []
        for index in range(int(len(batched_label_tensors)/4)):
            batched_label_tensor.append(batched_label_tensors[4*index][0])
        batched_label_tensor = torch.stack(batched_label_tensor)
        '''
        #attn_mask = torch.ones_like(batched_input_tensors)
        #is_padding = batched_input_tensors == tokenizer.pad_token_id
        #attn_mask[is_padding] = 0
        output_batch = {
            "langs": langs,
            "attention_mask": attn_mask,
            "labels": batched_label_tensors,
            "input_ids": batched_input_tensors
        }
        return output_batch
    return collate_fn_mt_wlang

def flatten(t):
    return [item for sublist in t for item in sublist]

class EvenClassSampler:
    def __init__(self, classes):
        self.classes = classes
        self.class_idxs = [[] for _ in range(len(set(self.classes)))]
        [self.class_idxs[class_num].append(i) for i, class_num in enumerate(self.classes)]
        for i in range(len(self.class_idxs)):
            random.shuffle(self.class_idxs[i])
        self.new_indexes = flatten(list(zip(*self.class_idxs)))

    def __iter__(self):
        return iter(self.new_indexes)


def get_collate_fn(data, tokenizer):
    if data == "brown":
        return make_collate_fn(tokenizer)
    elif data in ["un_mt_corpus", "mtnt", "mtnt_mt_corpus", "pawsx", "nc","xnli","mnli", "ag"]:
        return make_collate_fn_mt_wlang(tokenizer)    
    else:
        return make_collate_fn_wlang(tokenizer)

def get_dataloader(
    path_to_data: str, cid: str, is_train: bool, batch_size: int, workers: int, data: str,
    tokenizer, shuffle: bool = False, lang_mix: int = -1
):
    """Generates trainset/valset object and returns appropiate dataloader."""
    partition = "train" if is_train else "val"
    if type(path_to_data) not in [MultilingualDataset, torch.utils.data.Dataset, LineByLineTextDataset, \
                                        MTDataset, PAWSDataset, ClassificationDataset]:
        dataset = get_dataset(Path(path_to_data), cid, partition)
    else:
        dataset = path_to_data

    # we use as number of workers all the cpu cores assigned to this actor
    kwargs = {"num_workers": workers, "pin_memory": True, "drop_last": False}
    if lang_mix == 1.0:
        kwargs["sampler"] = EvenClassSampler([item[1] for item in dataset])
    elif shuffle:
        kwargs["shuffle"] = True

    c_func = get_collate_fn(data, tokenizer)
    return DataLoader(dataset, batch_size=batch_size, collate_fn=c_func, **kwargs)

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def do_fl_partitioning_brown(path_to_dataset, dataset, pool_size, val_ratio=0.0):
    dataset = [item.numpy() for item in dataset] # need to use numpy to save since PyTorch wants same sized batch
    random.shuffle(dataset)
    partitions = list(split(dataset, pool_size))

    # now save partitioned dataset to disk
    # first delete dir containing splits (if exists), then create it
    splits_dir = Path(path_to_dataset).parent / "federated"
    if splits_dir.exists():
        shutil.rmtree(splits_dir)
    Path.mkdir(splits_dir, parents=True)

    for p in range(pool_size):
        cur_data = np.array(partitions[p], dtype=object)
        # create dir
        Path.mkdir(splits_dir / str(p))

        if val_ratio > 0.0:
            # split data according to val_ratio
            train_idx, val_idx = get_random_id_splits(len(cur_data), val_ratio)
            val_cur_data = cur_data[np.array(val_idx)]
            np.save(splits_dir / str(p) / "val.npy", val_cur_data)

            # remaining for training
            cur_data = cur_data[np.array(train_idx)]
        # save train set
        np.save(splits_dir / str(p) / "train.npy", cur_data)

    return splits_dir


def convert_to_np(item) -> list:
    if type(item) == list:
        return [i.numpy() for i in item]
    else:
        return item.numpy()


def do_fl_partitioning(path_to_dataset: str, dataset, pool_size: int, cache_str: str,
                           lang_mix: float = 0.0, val_ratio=0.0):
    # NOTE: tensor may be a list of tensors if seq to seq or something
    dataset = [(convert_to_np(tensor_item), lang_id) for (tensor_item, lang_id) in dataset]
    dataset_df = pd.DataFrame(dataset, columns=["tensor", "lang_id"])
    sample_df = dataset_df.copy()

    if pool_size == 1: # centralized
        partitions = [dataset]
    else: # distributed
        partition_size = len(dataset_df) // pool_size

        same_lang_num = int(partition_size * (1 - lang_mix)) # floored
        if lang_mix == 1.0:
            same_lang_num = int(partition_size) # get them separated then zip them later
        partitions = [[] for x in range(len(dataset_df.lang_id.unique()))]

        # start by making partitions by lang only, sampling lang_mix
        for (lang, lang_df) in dataset_df.groupby(["lang_id"]):
            sampled_for_lang = lang_df.sample(n=same_lang_num)
            sampled_idx = sampled_for_lang.index
            sample_df = sample_df.drop(sampled_idx)
            for (idx, row) in sampled_for_lang.iterrows():
                partitions[lang].append((row["tensor"], row["lang_id"]))

        # now sample the rest from the great pool of available instances
        for partition_idx in range(len(partitions)):
            left_over_sampling = partition_size - same_lang_num
            sampled_for_lang = sample_df.sample(n=left_over_sampling)
            sampled_idx = sampled_for_lang.index
            sample_df = sample_df.drop(sampled_idx)
            for (idx, row) in sampled_for_lang.iterrows():
                partitions[partition_idx].append((row["tensor"], row["lang_id"]))

        if lang_mix == 1.0:
            # we want the batches to be perfectly split with each language
            # zip them together - creates a batch of each one
            partition_list = list(zip(*partitions))
            num_batches_per_partition = len(partition_list) // len(partitions)
            # now divide it into an almost equal number of batches per device
            for partition_num in range(len(partitions)):
                start_batch = partition_num * num_batches_per_partition
                end_batch = (partition_num + 1) * num_batches_per_partition
                if partition_num == (len(partitions) - 1):
                    end_batch = len(partition_list)
                batches_for_partition = partition_list[start_batch:end_batch]
                all_items_in_batches = []
                [all_items_in_batches.extend(list(batch)) for batch in batches_for_partition]
                partitions[partition_num] = all_items_in_batches

        zero_partitions_langs = pd.Series([item[1] for item in partitions[0]]).value_counts(normalize=True)
        print(f"The 0th partition has lang id mapping percent:\n{zero_partitions_langs} with {len(partitions[0])} instances")
        
    # now save partitioned dataset to disk
    # first delete dir containing splits (if exists), then create it
    splits_dir = Path(path_to_dataset) / ("federated_" + cache_str)
    if splits_dir.exists():
        shutil.rmtree(splits_dir)
    Path.mkdir(splits_dir, parents=True)

    for p in range(pool_size):
        cur_data = np.array(partitions[p], dtype=object)
        # create dir
        Path.mkdir(splits_dir / str(p))

        if val_ratio > 0.0:
            # split data according to val_ratio
            train_idx, val_idx = get_random_id_splits(len(cur_data), val_ratio)
            val_cur_data = cur_data[np.array(val_idx)]
            np.save(splits_dir / str(p) / "val.npy", val_cur_data)

            # remaining for training
            cur_data = cur_data[np.array(train_idx)]
        # save train set
        np.save(splits_dir / str(p) / "train.npy", cur_data)

    return splits_dir