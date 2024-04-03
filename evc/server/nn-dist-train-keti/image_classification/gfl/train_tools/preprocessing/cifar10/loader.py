import torch
import torch.utils.data as data
import torchvision.transforms as transforms
import numpy as np

from torchvision.datasets import CIFAR10

from torch.utils.data import DataLoader, Dataset

class DatasetSplit(Dataset):
    def __init__(self, dataset, idxs):
        self.dataset = dataset
        self.idxs = list(idxs)

    def __len__(self):
        return len(self.idxs)

    def __getitem__(self, item):
        image, label = self.dataset[self.idxs[item]]
        return image, label


def _data_transforms_cifar10():
    CIFAR_MEAN = [0.485, 0.456, 0.406]
    CIFAR_STD = [0.229, 0.224, 0.225]

    train_transform = transforms.Compose(
        [
            transforms.RandomCrop(32, padding=4),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize(CIFAR_MEAN, CIFAR_STD),
        ]
    )


    valid_transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize(CIFAR_MEAN, CIFAR_STD),]
    )

    return train_transform, valid_transform




def get_all_targets_cifar10(root, train=True):
    dataset = CIFAR10(root=root, train=train, download=False)
    all_targets = np.array(dataset.targets)
    return all_targets






def get_dataloader_cifar10(root, train=True, batch_size=50, dataidxs=None):
    train_transform, valid_transform = _data_transforms_cifar10()

    if train:
        dataset =CIFAR10(root=root, train=True, transform=train_transform, download=False)
        if dataidxs is not None:
            dataloader = DataLoader(DatasetSplit(dataset, dataidxs), batch_size=batch_size, shuffle=False)
        else:
            dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
            

    else:
        dataset = CIFAR10(root, train=False, transform=valid_transform, download=False)
        if dataidxs is not None:
            dataloader = DataLoader(DatasetSplit(dataset, dataidxs), batch_size=batch_size, shuffle=False)
        else:
            dataloader = DataLoader(dataset, batch_size=50, shuffle=False)
            
    return dataloader

