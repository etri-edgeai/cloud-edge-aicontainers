import os
import random
import argparse
from collections import OrderedDict, defaultdict
from pathlib import Path
from typing import Dict, Callable, Optional, Tuple
import traceback
import tqdm
import math
import bisect
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence

import flwr as fl
from flwr.common.typing import Scalar
import ray
from sacrebleu.metrics import BLEU, CHRF, TER

import transformers
from transformers import (
    AdamW,
    AutoConfig,
    BertConfig,
    AutoModelForCausalLM,
    AutoTokenizer,
    BertTokenizer,
    DistilBertTokenizer,
    SchedulerType,
    default_data_collator,
    get_scheduler,
    MT5Model,
    T5Tokenizer,
    MBartForCausalLM,
    DistilBertForSequenceClassification,
    XLMRobertaForMaskedLM,
    XLMRobertaForSequenceClassification,
    XLMForSequenceClassification,
    BartForCausalLM,
    BertForMaskedLM,
    BertForSequenceClassification,
    DistilBertForSequenceClassification,
    logging,
    DistilBertForMaskedLM,
    M2M100ForConditionalGeneration,
    M2M100Tokenizer,
    AutoModelForSequenceClassification,
    AlbertForMaskedLM,
    AlbertForSequenceClassification,
    XmodForSequenceClassification,
    DistilBertForSequenceClassification,
    BartForSequenceClassification,
    BartTokenizer,
    RobertaForSequenceClassification,
    AlbertConfig,
    BertForMultipleChoice
)
    
    
bleu = BLEU()

import warnings
warnings.filterwarnings("ignore")
logging.set_verbosity_error() # hides warning about CasualLM not loading encoder

from dataset_utils import (
    LineByLineTextDataset,
    get_dataset,
    get_random_id_splits,
    make_collate_fn_wlang,
    make_collate_fn,
    get_dataloader,
    do_fl_partitioning_brown,
    do_fl_partitioning,
    MultilingualDataset,
    get_dataset_type,
    MTDataset,
)
    
from constants import *

BIG_FILE_CACHE = "./cache"

## Global Vars that are set under `if __name__ == "__main__"`
ACCUM_STEPS = 1
BATCH_SIZE = 2
CUDA_COUNT = 0 # need to keep track for clients, iterative take the next one
RANDOM_INIT = False
MODEL_NAME = ""
DATA = ""
client_resources = {"num_gpus": 0, "num_cpus": 1} # NOTE: can do fractional GPUs, this is per process/client
GPU_MAPPING = {}
EVAL_NUM = 0
NUM_SKIP_EVAL = 1
PREV_LOSS = -1.0
tokenizer = None
LEARNING_RATE = None
LANG_MIX = None
CACHE_STR = None
ALL_OPTIMIZERS = {}
TOP_N_SCORES = []
GLOBAL_LANG_MAP = None

def set_seed(args):
    print(args.seed)
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if args.n_gpus > 0:
        torch.cuda.manual_seed_all(args.seed)
    
    
# borrowed from Pytorch quickstart example
def train(net, trainloader, epochs, optimizer, device: str, cid: str = "", get_accuracy: bool = False):
    """Train the network on the training set."""
    global ACCUM_STEPS
    global tokenizer
    set_seed(args_parsed)
    net.train()
    net.zero_grad()
    losses = []
    total, correct = 0,0
    for i in range(epochs):
        print('epoch:', i)
        for batch_idx, batch in enumerate(trainloader):
            input_ids = batch["input_ids"]
            label_ids = batch["labels"]
            attn_mask = batch["attention_mask"]
            #start = batch['start']
            #end = batch['end']

            label_ids = label_ids.to(device)
            #start=start.to(device)
            #end=end.to(device)
            input_ids = input_ids.to(device)
            attn_mask = attn_mask.to(device)

            x = {"input_ids": input_ids, "labels": label_ids, "attention_mask": attn_mask}
            #x = {"input_ids": input_ids, "start":start, "end":end, "attention_mask": attn_mask}
            #x = {"input_ids": input_ids, "attention_mask": attn_mask}
            output = net(**x)
            loss = output.loss / ACCUM_STEPS
            loss.backward() 
            losses.append(output.loss.cpu().detach().repeat(len(batch)))

            label_ids = label_ids.cpu()
            '''
            start = start.cpu()
            end = end.cpu()
            '''
            attn_mask = attn_mask.cpu()
            
            if get_accuracy:
                pred_labels = output.logits.argmax(dim=-1).cpu()
                truth_labels = label_ids.squeeze(-1).cpu()
                correct += torch.sum(torch.eq(pred_labels, truth_labels)).cpu().detach().item()
                total += len(pred_labels)
            
                
                
            if (batch_idx + 1) % ACCUM_STEPS == 0:  
                optimizer.step()
                net.zero_grad()
                loss = 0

    net = net.cpu()
    loss = 0
    net.zero_grad()
    label_ids = label_ids.to("cpu")
    #start = start.to("cpu")
    #end = end.to("cpu")
    attn_mask = attn_mask.to("cpu")
    mean_loss = torch.cat(losses).mean()
    #wandb.log({"TRAIN/Loss": mean_loss, "round": num_rounds})
    if get_accuracy:
        print(f"TRAIN Accuracy for is {correct/total}")
    
        #print("language sample:", tokenizer.decode(trainloader[0]['input_ids'])
    
    (f"Got a TRAIN PPL value of {mean_loss.detach().item()} and {torch.exp(mean_loss).detach().item()} \
            for cid={cid}, label={batch['langs'][0].item()}")

def test(net, testloader, device: str, get_accuracy: bool = False):
    global num_rounds
    global tokenizer
    """Validate the network on the entire test set."""
    net.eval()
    losses = []
    correct = 0
    total = 0
    labels_to_losses = defaultdict(list)
    labels_to_accuracies = defaultdict(dict)
    with torch.no_grad():
        for idx, batch in enumerate(testloader):
            input_ids = batch["input_ids"]
            label_ids = batch["labels"]
            attn_mask = batch["attention_mask"]
            
            input_ids = input_ids.to(device)
            #print('input_ids:', tokenizer.decode(input_ids[0]))
            #print('input_ids:', input_ids[0])
            attn_mask = attn_mask.to(device)
            label_ids = label_ids.to(device)
            #print(label_ids)
            x = {"input_ids": input_ids, "labels": label_ids, "attention_mask": attn_mask}
            output = net(**x)
            if get_accuracy:
                pred_labels = output.logits.argmax(dim=-1).cpu()
                truth_labels = label_ids.squeeze(-1).cpu()
                correct += torch.sum(torch.eq(pred_labels, truth_labels)).item()
                total += len(pred_labels)
                
            loss = output.loss
            
            try:
                assert len(set(batch["langs"].numpy().tolist())) == 1, set(batch["langs"].numpy().tolist())
                labels_to_losses[batch["langs"][0].item()].append(output.loss.item())
                if "correct" not in labels_to_accuracies[batch["langs"][0].item()]:
                    labels_to_accuracies[batch["langs"][0].item()]["correct"] = 0
                    labels_to_accuracies[batch["langs"][0].item()]["total"] = 0
                labels_to_accuracies[batch["langs"][0].item()]["correct"] += torch.sum(torch.eq(pred_labels, truth_labels)).item()
                labels_to_accuracies[batch["langs"][0].item()]["total"] += len(pred_labels)
            except Exception as e:
                print(f"Cant make lang ppls unless entire batch is the same: use a round num for batch size: {e}")
            losses.append(loss.repeat(len(batch)))

    # from https://github.com/huggingface/transformers/blob/master/examples/pytorch/language-modeling/run_clm_no_trainer.py
    mean_loss = torch.cat(losses).mean()
    #wandb.log({"EVAL/Loss": mean_loss, "round": num_rounds})
    max_num = max(list(labels_to_losses.keys()))
    for label in range(max_num+1):
        print(f"For EVAL Label {label} the average PPL is {np.exp(np.mean(labels_to_losses[label]))}")
        print(f"For EVAL Label {label} the average accuracy is {labels_to_accuracies[label]['correct'] / labels_to_accuracies[label]['total']}")
        #wandb.log({"Client/Acc": {labels_to_accuracies[label]['correct'] / labels_to_accuracies[label]['total']}, "round": num_rounds})
    net = net.to("cpu")
    if get_accuracy:
        print(f"EVAL Accuracy is {correct/total}")
        #wandb.log({"Eval/Acc": {correct/total}, "round": num_rounds})
    label_ids = label_ids.to("cpu")
    label_ids = label_ids.to("cpu")
    attn_mask = attn_mask.to("cpu")
    return mean_loss.item(), torch.exp(mean_loss).detach().item()


def test_mt(net, testloader, device: str, get_accuracy: bool = False):
    """Validate the network on the entire test set."""
    net.eval()
    generated = []
    targets = []
    is_long_enough = lambda x: len(x) > 3
    make_list_long = lambda x: [item for item in x if is_long_enough(item)]
    def compute_bleu(generated, targets):
        assert len(generated) == len(targets)
        final_gen = []
        final_targ = []
        for idx in range(len(generated)):
            if is_long_enough(generated[idx]) and is_long_enough(targets[idx]):
                final_gen.append(generated[idx])
                final_targ.append(targets[idx])

        return bleu.corpus_score(final_gen, final_targ).score
        
    labels_to_generated = defaultdict(list)
    labels_to_targets = defaultdict(list)
    with torch.no_grad():
        print(len(testloader))
        for idx, batch in enumerate(testloader):
            input_ids = batch["input_ids"]
            label_ids = batch["labels"]
            assert len(set(batch["labels"][:, 0].tolist())) == 1 # handling multiple languages is tricky with the forced BOS
            attn_mask = batch["attention_mask"]            
            input_ids = input_ids.to(device)
            attn_mask = attn_mask.to(device)
            label_ids = label_ids.to(device)
            x = {"input_ids": input_ids, "attention_mask": attn_mask}
            output = net.generate(**x, forced_bos_token_id=batch["labels"][:, 0][0].item())
            try:
                assert len(set(batch["langs"].numpy().tolist())) == 1
                labels_to_generated[batch["langs"][0].item()].extend(tokenizer.batch_decode(output, skip_special_tokens=True))
                labels_to_targets[batch["langs"][0].item()].extend(tokenizer.batch_decode(label_ids, skip_special_tokens=True))
            except Exception as e:
                print("Cant make lang ppls unless entire batch is the same: use a round num for batch size")
                raise e

    max_num = max(list(labels_to_targets.keys()))
    all_gen = []
    all_trg = []
    for label in range(max_num+1):
        with open(MODEL_NAME.replace(".pt", "") + f".label.{label}.pred", "w") as fout:
            for sent in labels_to_generated[label]:
                fout.write(sent + "\n")
        with open(MODEL_NAME.replace(".pt", "") +  f".label.{label}.trg", "w") as fout:
            for sent in labels_to_targets[label]:
                fout.write(sent + "\n")        
        print(f"For Label {label} the average BLEU is {compute_bleu(labels_to_generated[label], labels_to_targets[label])}")    
        all_gen.extend(labels_to_generated[label])
        all_trg.extend(labels_to_targets[label])
    bleu_score = compute_bleu(all_gen, all_trg)
    print(f"Total overall BLEU across langs is {bleu_score}")
    exit(1)

    net = net.to("cpu")
    label_ids = label_ids.to("cpu")
    label_ids = label_ids.to("cpu")
    attn_mask = attn_mask.to("cpu")
    return bleu_score, bleu_score # keep same format, but uneeded


# Flower client that will be spawned by Ray
# Adapted from Pytorch quickstart example
class RayClient(fl.client.NumPyClient):
    def __init__(self, cid: str, fed_dir_data: str, optimizer, net):
        global CUDA_COUNT
        global GPU_MAPPING 
        global LEARNING_RATE
        global EPOCH

        self.cid = cid
        self.fed_dir = Path(fed_dir_data)
        self.properties: Dict[str, Scalar] = {"tensor_type": "numpy.ndarray"}

        # instantiate model
        self.net = net
        self.optimizer = optimizer

        # determine device
        cuda_available = torch.cuda.is_available()
        device_str = f"cuda:0" if cuda_available else "cpu" # CUDA zero defaults to CUDA_VISIBLE_DEVICES
        self.device = torch.device(device_str)
        
        
    def get_parameters(self):
        return [val.cpu().numpy() for _, val in self.net.state_dict().items()]

    def get_properties(self, ins):
        return self.properties

    def set_parameters(self, parameters):
        params_dict = zip(self.net.state_dict().keys(), parameters)
        state_dict = OrderedDict(
            {k: torch.from_numpy(np.copy(v)) for k, v in params_dict}
        )
        self.net.load_state_dict(state_dict, strict=True)

    def fit(self, parameters, config):
        global DATA
        global BATCH_SIZE
        self.set_parameters(parameters)
        global tokenizer

        try:
            print('partition_number:',self.cid)
            # load data for this client and get trainloader
            num_workers = len(ray.worker.get_resource_ids()["CPU"])
            trainloader = get_dataloader(
                self.fed_dir,
                self.cid,
                is_train=True,
                batch_size=BATCH_SIZE,
                workers=num_workers,
                data=DATA,
                tokenizer=tokenizer,
                shuffle=True,
                lang_mix=LANG_MIX,
            )

            # send model to device
            self.net.to(self.device)

            # train
            train(self.net, trainloader, int(config["epochs"]), self.optimizer, device=self.device, 
                    cid=self.cid, get_accuracy=("pawsx" in DATA or "nc" in DATA or "xnli" in DATA or "mnli" in DATA, 'ag' in DATA))
        
        except Exception as e:
            print(f"Error failed in train was `{e}`")
            print(traceback.format_exc())
            raise e

        # return local model and statistics
        return self.get_parameters(), len(trainloader.dataset), {}

    def evaluate(self, parameters, config):
        global tokenizer_list
        self.set_parameters(parameters)

        # load data for this client and get trainloader
        num_workers = len(ray.worker.get_resource_ids()["CPU"])
        valloader = get_dataloader(
            self.fed_dir, self.cid, is_train=False, batch_size=BATCH_SIZE, workers=num_workers, 
            tokenizer=tokenizer, shuffle=False, lang_mix=LANG_MIX
        )

        # send model to device
        self.net.to(self.device)

        # evaluate
        loss, accuracy = test(self.net, valloader, device=self.device, get_accuracy=("pawsx" in DATA or "nc" in DATA or "xnli" in DATA or "mnli" in DATA or "ag" in DATA))
        self.net.to("cpu")

        # return statistics
        return float(loss), len(valloader.dataset), {f"perplexity_{self.cid}": float(accuracy)}


def fit_config(rnd: int) -> Dict[str, str]:
    """Return a configuration with static batch size and (local) epochs."""
    global BATCH_SIZE
    config = {
        "epoch_global": str(rnd),
        "epochs": str(EPOCH),
        "batch_size": str(BATCH_SIZE),
    }
    return config


class TopItem:
    # to manage saving the top_N items
    def __init__(self, score: float, path: str):
        self.score = score
        self.path = path
    
    def __lt__(self, other) -> bool:
        return self.score < other.score

    def to_str(self) -> str:
        return f"Score: {self.score} at Path: {self.path}"


def set_weights(model: torch.nn.ModuleList, weights: fl.common.Weights) -> None:
    """Set model weights from a list of NumPy ndarrays."""
    state_dict = OrderedDict(
        {
            k: torch.Tensor(np.atleast_1d(v))
            for k, v in zip(model.state_dict().keys(), weights)
        }
    )
    model.load_state_dict(state_dict, strict=True)


def get_eval_fn(
    testset, lang_mix: float
) -> Callable[[fl.common.Weights], Optional[Tuple[float, float]]]:
    """Return an evaluation function for centralized evaluation."""

    def evaluate(weights: fl.common.Weights) -> Optional[Tuple[float, float]]:
        """Use the entire test set for evaluation."""
        global CUDA_COUNT
        global BATCH_SIZE
        global DATA
        global GPU_MAPPING
        global EVAL_NUM
        global MODEL_NAME
        global tokenizer
        global PREV_LOSS
        global NUM_SKIP_EVAL
        global TOP_N_SCORES
        global EPOCH
        global num_rounds
        KEEP_PILE = 2
        '''
        if EVAL_NUM % NUM_SKIP_EVAL !=0: # after every epoch basically
            print(f"Skipping with EVAL_NUM={EVAL_NUM} and NUM_SKIP_EVAL={NUM_SKIP_EVAL}")
            EVAL_NUM += 1
            return PREV_LOSS, {"perplexity": math.exp(PREV_LOSS)}
        '''
        model = make_huggingface_model()
        
        #model_list = make_huggingfacemodels()
        #for i, model in enumerate(model_list):
            #print('model:', model.state_dict().keys())
        set_weights(model, weights)
        

        # determine device        
        if os.environ.get("CUDA_VISIBLE_DEVICES") is None:
            cuda_is_available = False
        else:
            cuda_is_available = torch.cuda.is_available()
        device_str = f"cuda:{GPU_MAPPING['server']}" if cuda_is_available else "cpu"
        #print('eval_device_str:',device_str)
        device = torch.device(device_str)
        model.to(device)

        if len(GPU_MAPPING) == 1: 
            if "_mt_" in DATA or "mtnt" in DATA:
                # MT Eval only
                print("Running Eval on MT")
                test_fn = test_mt
                batch_size = 1
            else:
                test_fn = test
                batch_size = BATCH_SIZE                
        else:
            test_fn = test
            batch_size = BATCH_SIZE

        testloader = get_dataloader(
            testset, -1, is_train=False, batch_size=batch_size, workers=3, 
            tokenizer=tokenizer, shuffle=False, data=DATA, lang_mix=LANG_MIX
        )

        
        loss, accuracy = test_fn(model, testloader, device=device, get_accuracy=("pawsx" in DATA or "nc" in DATA or "xnli" in DATA or "mnli" in DATA, "ag" in DATA))

        if len(TOP_N_SCORES) < KEEP_PILE or loss < TOP_N_SCORES[-1].score:
            if "_cont" in CACHE_STR:
                save_path = f"{BIG_FILE_CACHE}/{MODEL_NAME.split('/')[-1][-3]}/{CACHE_STR}/"
            else:
                save_path = f"{BIG_FILE_CACHE}/{MODEL_NAME.split('/')[-1]}/{CACHE_STR}/"

            bisect.insort(TOP_N_SCORES, TopItem(loss, save_path + f"{EVAL_NUM}.pt"))
            print([item.to_str() for item in TOP_N_SCORES])
            TOP_N_SCORES, to_remove = TOP_N_SCORES[:KEEP_PILE], TOP_N_SCORES[KEEP_PILE:]

            for top_item in to_remove:
                print(f"Removing {top_item.to_str()}")
                os.remove(top_item.path)

            if not os.path.isdir(save_path):
                os.makedirs(save_path)

        
            torch.save(model, f"{save_path}/{EVAL_NUM}.pt")


        EVAL_NUM += 1

        PREV_LOSS = loss

        # return statistics
        return loss, {"perplexity": accuracy}

    return evaluate


def make_tokenizer(model_name: str):
    global tokenizer    
    if 'xmod' in model_name:
        tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base", use_fast=False)    
    if 'tiny' in model_name:
        tokenizer = AutoTokenizer.from_pretrained('albert-base-v1',use_fast=False)
    else:
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
        print(len(tokenizer))
    return tokenizer

def make_tokenizers():
    global tokenizer
    model_names=['roberta-base',
                 'skimai/spanberta-base-cased',
                 'benjamin/roberta-base-wechsel-french',
                 'benjamin/roberta-base-wechsel-german']
    tokenizer_list=[]
    for model_name in model_names:
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
        tokenizer_list.append(tokenizer)
    return tokenizer_list
    



def make_huggingface_model():
    global CACHE_STR
    '''
    try:
        config = AutoConfig.from_pretrained(MODEL_NAME)
    except Exception as e:
        pass # loading model doesn't need this
    '''
    warnings.filterwarnings("ignore")
    logging.set_verbosity_error() # hides warning about CasualLM not loading encoder
    if ".pt" in MODEL_NAME[-3:]:
        print(f"Loading model {MODEL_NAME}")
        model = torch.load(MODEL_NAME)
        CACHE_STR = MODEL_NAME.split("/")[-2] + "_cont"
    elif not RANDOM_INIT:
        #print("Finetuning with pretrained model")
        if "gpt2" in MODEL_NAME:
            model = AutoModelForCausalLM.from_pretrained(
                MODEL_NAME,
                from_tf=False,
                cache_dir=f"{BIG_FILE_CACHE}/huggingface_cache/"
            )
        elif "bart" in MODEL_NAME:
            model = BartForSequenceClassification.from_pretrained(
                MODEL_NAME,
                cache_dir=f"{BIG_FILE_CACHE}/huggingface_cache/",
                num_labels=3
            )
            
        elif "xlm" in MODEL_NAME:
            try:
                model = XLMRobertaForSequenceClassification.from_pretrained(
                    MODEL_NAME,
                    cache_dir=f"{BIG_FILE_CACHE}/huggingface_cache/",
                    num_labels=3
                )
                
            except Exception as e:
                breakpoint()
                print(e)  
        elif "distil" in MODEL_NAME:
            model = DistilBertForSequenceClassification.from_pretrained(
                MODEL_NAME,
                cache_dir=f"{BIG_FILE_CACHE}/huggingface_cache/",
                num_labels=3
            )        
        elif "roberta" in MODEL_NAME:
            model = RobertaForSequenceClassification.from_pretrained(
                MODEL_NAME,
                cache_dir=f"{BIG_FILE_CACHE}/huggingface_cache/",
                num_labels=3
            )   
        elif "bert" in MODEL_NAME:
            model = BertForSequenceClassification.from_pretrained(
                MODEL_NAME,
                cache_dir=f"{BIG_FILE_CACHE}/huggingface_cache/",
                num_labels=4
            )
        elif "albert" in MODEL_NAME:
            model = AlbertForSequenceClassification.from_pretrained(
                MODEL_NAME,
                cache_dir=f"{BIG_FILE_CACHE}/huggingface_cache/",
                num_labels=3
            )
        
            #model.resize_token_embeddings(len(tokenizer))
        elif "tiny" in MODEL_NAME:
            '''
            model = BertForSequenceClassification.from_pretrained(
                'bert-base-uncased',
                cache_dir=f"{BIG_FILE_CACHE}/huggingface_cache/",
                num_labels=3
            )
            '''
            config_mlm = XLMRobertaConfig(max_position_embeddings=514, type_vocab_size=1)
            config_cls = XLMRobertaConfig(num_labels=3)

            model_mlm = XLMRobertaForMaskedLM(config_mlm)
            model_cls = XLMRobertaForSequenceClassification(config_cls)
            checkpoint= torch.load('snapshot_sw.pt')
            model_mlm.load_state_dict(checkpoint['MODEL_STATE'])
            model_cls.roberta=model_mlm.roberta
            model=model_cls
            
        elif "m2m" in MODEL_NAME:
            model = M2M100ForConditionalGeneration.from_pretrained(
                MODEL_NAME,
                cache_dir=f"{BIG_FILE_CACHE}/huggingface_cache/"
            )
        else:
            raise NotImplementedError(f"Haven't impleneted model={MODEL_NAME}")
            
    else:
        print("Training new model from scratch")
        if "xlm" in MODEL_NAME:
            config.num_labels = 3
            model = XLMRobertaForSequenceClassification(
                config
            )
        elif "bert" in MODEL_NAME:
            model = DistilBertForMaskedLM(config)
        elif "m2m" in MODEL_NAME:
            model = M2M100ForConditionalGeneration(config)

    return model

def make_huggingfacemodels():
    global CACHE_STR
    try:
        config = AutoConfig.from_pretrained(MODEL_NAME)
    except Exception as e:
        pass # loading model doesn't need this

    model_names=['roberta-base',
                 'skimai/spanberta-base-cased',
                 'benjamin/roberta-base-wechsel-french',
                 'benjamin/roberta-base-wechsel-german']
    model_list=[]
    for model_name in model_names:
        model = AutoModelForSequenceClassification.from_pretrained(
                model_name,
                cache_dir=f"{BIG_FILE_CACHE}/huggingface_cache/",
                num_labels=10)
        model_list.append(model)
    return model_list
               
        


# Start Ray simulation (a _default server_ will be created)
# This example does:
# 1. Prepares the data
# 2. Partitions the dataset into N splits, where N is the total number of
#    clients. We refere to this as `pool_size`. The partition can be IID or non-IID
# 4. Starts a Ray-based simulation where a % of clients are sample each round.
# 5. After the M rounds end, the global model is evaluated on the entire testset.
#    Also, the global model is evaluated on the valset partition residing in each
#    client. This is useful to get a sense on how well the global model can generalise
#    to each client's data.
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, help="dataset path to use", required=True)
    parser.add_argument("--model", type=str, help="The model name to use", required=True)
    parser.add_argument("--n_cpus", type=float, help="The number of CPUs to use PER MACHINE", default=-1)
    parser.add_argument("--n_gpus", type=float, help="The number of GPUs to use TOTAL", default=0.0)
    parser.add_argument("--frac_fit", type=float, help="The percent of nodes to sample each time", default=1.0)
    parser.add_argument("--epoch", type=int, help="number of local iteration", default=2)
    parser.add_argument("--batch_size", type=int, default=16, help="The batch size to use")
    parser.add_argument("--batch_accum", type=int, default=8, help="The batch accumulation steps to do")
    parser.add_argument("--n_iterations", type=int, default=120, help="The number of iterations to do")
    parser.add_argument("--lang_mix", type=float, default=0.0, help="The lang mixture to use (0 for separate, 1 for uniform)")
    parser.add_argument("--lr", type=float, default=5e-5, help="The learning rate to use for the optimizer")
    parser.add_argument("--random_init", action="store_true", help="Whether to load a random intialized model")
    parser.add_argument("--load_model", type=str, help="whether to load a saved model path")
    parser.add_argument("--centralized", action="store_true", help="Whether to run with a centralized run instead")
    parser.add_argument("--test", type=int, default=0, help="Whether to load small data instead")
    parser.add_argument('--seed', type=int, default=0,help='seed number')
    parser.add_argument('--skip_evalnum', type=int, default=10, help='skip eval number')
    #parser.add_argument("--gpu",  nargs='+', type=int, help="designate gpu index")
    args_parsed = parser.parse_args()
    BATCH_SIZE = args_parsed.batch_size
    RANDOM_INIT = args_parsed.random_init
    MODEL_NAME = args_parsed.model if args_parsed.load_model is None else args_parsed.load_model
    EPOCH = args_parsed.epoch
    DATA = args_parsed.data
    ACCUM_STEPS = args_parsed.batch_accum
    num_rounds = args_parsed.n_iterations
    LEARNING_RATE = args_parsed.lr
    LANG_MIX = args_parsed.lang_mix
    pool_size = POOL_SIZE[args_parsed.data]# number of dataset partions (= number of total clients)
    #seed_val = args_parsed.seed
    print('model:',MODEL_NAME)

    '''
    wandb.init(
        project="multilingual_fl", entity="etri_2022_practice",
        name="translate_train_all"+str(num_rounds)+"-m"+str(MODEL_NAME)+ "-e" + str(EPOCH) + "-lr" + str(LEARNING_RATE)+ "-client_number" + str(pool_size)+ "-partition_method" + str(LANG_MIX),
    )
    '''
    if args_parsed.centralized:
        pool_size = 1
        print('centralized')

    cache_str = str(args_parsed.lang_mix) + "_" + str(args_parsed.lr) + f"_{DATA}" if pool_size != 1 else f"centralized_{DATA}_" + str(args_parsed.lr)
    if args_parsed.random_init:
        cache_str += "_random"
    CACHE_STR = cache_str
    
    if args_parsed.n_gpus != 0.0:
        N_GPUS = args_parsed.n_gpus
        if num_rounds == 0:
            GPU_MAPPING["server"] = 0
        else:
            '''
            if N_GPUS < 2 and num_rounds != 0:
                print(f"Given N_GPUs={N_GPUS}, need 2+ for client(s) and server to have separate GPUs. Use CPU instead otherwise")
                exit(1)
                '''
            #num_iter_for_epoch = pool_size // (N_GPUS-1) if pool_size % (N_GPUS - 1) == 0 else (pool_size // (N_GPUS-1)) + 1
            num_iter_for_epoch = pool_size // (N_GPUS) if pool_size % (N_GPUS) == 0 else (pool_size // (N_GPUS)) + 1
            #args_parsed.frac_fit = 1 / num_iter_for_epoch
            # TODO implement fractional GPU options if desired
            #num_rounds = int(num_rounds * num_iter_for_epoch)
            #client_resources["num_gpus"] = args_parsed.frac_fit
            client_resources["num_gpus"] = 1.0
            #print(f"Using 1 GPU per client with {args_parsed.frac_fit} clients sampled per round out of {pool_size} clients")
          
            #gpus="2,3"
            #os.environ["CUDA_VISIBLE_DEVICES"]=gpus
            #gpu_list=gpus.split(',')
            #num_of_gpus_per_round = int(pool_size // num_iter_for_epoch) #5//1
            gpu_lists=[0,0,0,1,1]
            #NUM_SKIP_EVAL = num_skip_eval
            GPU_MAPPING["server"] = 1
            '''
            for cid in range(pool_size):
                #cid_gpu_idx = int(cid % num_of_gpus_per_round)
                #cid_gpu_idx = int(cid // num_iter_for_epoch)
                #GPU_MAPPING[cid] = int(gpu_list[cid_gpu_idx])
     
                GPU_MAPPING[cid] = gpu_lists[cid]
            print(f"GPU mapping is: {GPU_MAPPING}")
            '''
    if args_parsed.n_cpus != -1:
        client_resources["num_cpus"] = args_parsed.n_cpus
    
    tokenizer = make_tokenizer(args_parsed.model)
    #tokenizer_list = make_tokenizers()
    file_path_data = DATA_TO_FILE_PATHS[args_parsed.data]
    GLOBAL_LANG_MAP = MAP_LANG_MAP[file_path_data]
    
    set_seed(args_parsed)

    if args_parsed.data == "brown":
        trainset = LineByLineTextDataset(tokenizer, f"{file_path_data}/train.txt", test_flag=args_parsed.test)
        testset = LineByLineTextDataset(tokenizer, f"{file_path_data}/dev.txt", test_flag=args_parsed.test)
        fed_dir = do_fl_partitioning_brown(
            f"{file_path_data}/train.txt", trainset.examples, pool_size=pool_size, val_ratio=0.0
        )
    else:
        '''
        for i,tokenizer in enumerate(tokenizer_list):
            dataset_type = get_dataset_type(file_path_data)
            trainset = dataset_type(tokenizer, file_path_data, split="train", test_flag=args_parsed.test)
            split_name = "dev" if num_rounds != 0 else "test"
            print("Eval set is", split_name)
            testset = dataset_type(tokenizer, file_path_data, split=split_name, test_flag=args_parsed.test)
            fed_dir = do_fl_partitioning(
                file_path_data, trainset.examples, pool_size=pool_size, lang_mix=args_parsed.lang_mix, 
                cache_str=cache_str, val_ratio=0.0 # we manually do test
            )
        
        '''
        dataset_type = get_dataset_type(file_path_data)
        trainset = dataset_type(tokenizer, file_path_data, split="train", test_flag=args_parsed.test)
        #split_name = "dev" if num_rounds != 0 else "test"
        split_name = "test"
        print("Eval set is", split_name)
        testset = dataset_type(tokenizer, file_path_data, split=split_name, test_flag=args_parsed.test)
        fed_dir = do_fl_partitioning(
            file_path_data, trainset.examples, pool_size=pool_size, lang_mix=args_parsed.lang_mix, 
            cache_str=cache_str, val_ratio=0.0 # we manually do test
        )
        
    print('partition end')
    # configure the strategy
    strategy = fl.server.strategy.FedAvg(
        fraction_fit=args_parsed.frac_fit,
        min_fit_clients=1,
        min_available_clients=pool_size,  # All clients should be available
        on_fit_config_fn=fit_config,
        eval_fn=get_eval_fn(testset, args_parsed.lang_mix if not args_parsed.centralized else "central"),  # centralised testset evaluation of global model
    )

    def client_fn(cid: str, optimizers=ALL_OPTIMIZERS):
        net = make_huggingface_model()
        # create a single client instance
        if cid not in optimizers:
            # Split weights in two groups, one with weight decay and the other not.
            no_decay = ["bias", "LayerNorm.weight"]
            weight_decay = 0
            learning_rate = LEARNING_RATE
            optimizer_grouped_parameters = [
                {
                    "params": [p for n, p in net.named_parameters() if not any(nd in n for nd in no_decay)],
                    "weight_decay": weight_decay,
                },
                {
                    "params": [p for n, p in net.named_parameters() if any(nd in n for nd in no_decay)],
                    "weight_decay": 0.0,
                },
            ]
            optimizers[cid] = AdamW(optimizer_grouped_parameters, lr=learning_rate)

            
        return RayClient(cid, fed_dir, optimizers[cid], net)
    
    def client_fn_model_hetero(cid: str, optimizers=ALL_OPTIMIZERS):
        models = make_huggingfacemodels()
        # create a single client instance
        for index, net in enumerate(models):
            if cid not in optimizers:
                no_decay = ["bias", "LayerNorm.weight"]
                weight_decay = 0
                learning_rate = LEARNING_RATE
                optimizer_grouped_parameters = [
                {
                    "params": [p for n, p in net.named_parameters() if not any(nd in n for nd in no_decay)],
                    "weight_decay": weight_decay,
                },
                {
                    "params": [p for n, p in net.named_parameters() if any(nd in n for nd in no_decay)],
                    "weight_decay": 0.0,
                },
            ]
           
            optimizers[cid] = AdamW(optimizer_grouped_parameters, lr=learning_rate)

            
        return RayClient(cid, fed_dir, optimizers[cid], models[index])

            
    # (optional) specify ray config
    ray_config = {"include_dashboard": True}

    # start simulation
    fl.simulation.start_simulation(
        client_fn=client_fn,
        num_clients=pool_size,
        client_resources=client_resources,
        num_rounds=num_rounds,
        strategy=strategy,
        ray_init_args=ray_config,
    )
