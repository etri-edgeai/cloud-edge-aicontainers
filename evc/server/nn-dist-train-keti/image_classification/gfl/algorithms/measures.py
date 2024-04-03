import torch
import torch.nn.functional as F
from .utils import *

__all__ = ["evaluate_model", "evaluate_model_classwise", "get_round_personalized_acc"]


@torch.no_grad()
def evaluate_model(model, dataloader, device="cuda:0"):
    """Evaluate model accuracy for the given dataloader"""
    model.eval()
    model.to(device)

    running_count = 0
    running_correct = 0

    for data, targets in dataloader:
        data, targets = data.to(device), targets.to(device)

        logits = model(data)
        pred = logits.max(dim=1)[1]

        running_correct += (targets == pred).sum().item()
        running_count += data.size(0)

    accuracy = 100*float(running_correct) / running_count

    return accuracy


@torch.no_grad()#보유하지 않는 class에 대해서는 1로 찍는가?
def evaluate_model_classwise(
    model, dataloader, num_classes=10, device="cuda:0",
):
    """Evaluate class-wise accuracy for the given dataloader."""

    model.eval()
    model.to(device)

    classwise_count = torch.Tensor([0 for _ in range(num_classes)]).to(device)
    classwise_correct = torch.Tensor([0 for _ in range(num_classes)]).to(device)

    for data, targets in dataloader:
        data, targets = data.to(device), targets.to(device)

        logits = model(data)
        preds = logits.max(dim=1)[1]#[0]은 value [1]은 index 뽑아냄

        for class_idx in range(num_classes):
            class_elem = (targets == class_idx) #batch 내에서 target이 class_idx에 해당하는지 여부에 대한 boolean!!
            classwise_count[class_idx] += class_elem.sum().item()
            classwise_correct[class_idx] += (targets == preds)[class_elem].sum().item()#targets == preds의 batchsize의 boolean 결과 중 class_elem에서 true인 index만 추출한 것이 (targets == preds)[class_elem]이다. 즉 이것의 dimension은 class_elem.sum() 과 일치!!

    classwise_accuracy = (classwise_correct / classwise_count)*100 #각 class별로 갯수 같으니까(balanced test data) simple mean해도 상관 없음!!
    accuracy = round(classwise_accuracy.mean().item(), 4)

    return classwise_accuracy.cpu(), accuracy


@torch.no_grad()
def get_round_personalized_acc(round_results, server_results, data_distributed):#round_results: 해당 라운드에 selected된 client들의 statistic 기술한 dictionary(local train accuracy, classwise testaccuracy, test accuracy)
    """Evaluate personalized FL performance on the sampled clients."""

    sampled_clients = server_results["client_history"][-1]
    #Sampled client 한정해서 client 내의 classwise empirical distribution, client내의 train data 수 반환!!
    local_dist_list, local_size_list = sampled_clients_identifier(
        data_distributed, sampled_clients
    )

    local_cwa_list = round_results["classwise_accuracy"]##Sampled client 한정해서 client 내의 balanced global test data 기준 classwise test accuracy

    result_dict = {}

    in_dist_acc_list, out_dist_acc_list = [], []
    local_size_prop = F.normalize(torch.Tensor(local_size_list), dim=0, p=1)##Sampled client 한정해서 보유한 train data 수 기준 normalize

    for local_cwa, local_dist_vec in zip(local_cwa_list, local_dist_list):#select된 client list내의 각 client 별로 실행
        local_dist_vec = torch.Tensor(local_dist_vec)#classwise in-distribution
        inverse_dist_vec = calculate_inverse_dist(local_dist_vec) #classwise ood-distribution
        in_dist_acc = torch.dot(local_cwa, local_dist_vec) #classwise in-distribution 기준의 accuracy output(balanced test data accuracy 기반으로 계산)
        in_dist_acc_list.append(in_dist_acc)
        out_dist_acc = torch.dot(local_cwa, inverse_dist_vec)#classwise out-of-distribution 기준의 accuracy output(balanced test data accuracy 기반으로 계산)
        out_dist_acc_list.append(out_dist_acc)

    round_in_dist_acc = torch.Tensor(in_dist_acc_list)#select된 client list들의 정보
    round_out_dist_acc = torch.Tensor(out_dist_acc_list)
    
    result_dict["in_dist_acc_prop"] = torch.dot(
        round_in_dist_acc, local_size_prop
    ).item()#select된 client list의 data size를 고려해 weight sum 적용한 in-distribution accuracy
    result_dict["in_dist_acc_mean"] = (round_in_dist_acc).mean().item()#select된 client들의 simple averaged in-distribution accuracy
    result_dict["in_dist_acc_std"] = (round_in_dist_acc).std().item()
    result_dict["out_dist_acc_prop"] = torch.dot(round_out_dist_acc, local_size_prop).item()#select된 client list의data size를 고려해 weight sum 적용한 out-of-distribution accuracy
    result_dict["out_dist_acc_mean"] = (round_out_dist_acc).mean().item()
    result_dict["out_dist_acc_std"] = (round_out_dist_acc).std().item()

    return result_dict


@torch.no_grad()
def calculate_inverse_dist(dist_vec):#1-empirical classwise in-distribution
    """Get the out-local distribution"""
    inverse_dist_vec = (1 - dist_vec) / (dist_vec.nelement() - 1)

    return inverse_dist_vec
