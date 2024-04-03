from .models import *

__all__ = ["create_models"]

MODELS = {
    "fedavg_cifar": fedavgnet.FedAvgNetCIFAR,
    "mobile": mobilenet.MobileNetCifar,
    "vgg": vgg.vgg11
}

NUM_CLASSES = {
    "cifar10": 10,
    "cifar100": 100,
}


def create_models(model_name, dataset_name, **kwargs):
    """Create a network model"""

    num_classes = NUM_CLASSES[dataset_name]
    model = MODELS[model_name](num_classes=num_classes)

    return model
