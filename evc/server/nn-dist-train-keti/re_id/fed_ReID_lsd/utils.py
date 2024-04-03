import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import os
from model import ft_net
from torch.autograd import Variable

from torchvision import datasets, transforms

def set_random_seed(seed):
    random.seed(seed)
    np.random.seed(seed**2)
    torch.manual_seed(seed**3)
    torch.cuda.manual_seed(seed**4)

def get_optimizer(model, lr):
    ignored_params = list(map(id, model.classifier.parameters() ))
    base_params = filter(lambda p: id(p) not in ignored_params, model.parameters())
    optimizer_ft = optim.SGD([
            {'params': base_params, 'lr': 0.1*lr},
            {'params': model.classifier.parameters(), 'lr': lr}
        ], weight_decay=5e-4, momentum=0.9, nesterov=True)
    return optimizer_ft

# def get_optimizer(model, lr):
#     ignored_params = list(map(id, model.classifier.parameters() ))
#     base_params = filter(lambda p: id(p) not in ignored_params, model.parameters())
#     optimizer_ft = optim.SGD([
#             {'params': base_params, 'lr': lr},
#             {'params': model.classifier.parameters(), 'lr': lr}
#         ], weight_decay=5e-4, momentum=0.9, nesterov=True)
#     return optimizer_ft


def save_network(network, cid, epoch_label, project_dir, name, gpu_ids):
    save_filename = 'net_%s.pth'% epoch_label
    dir_name = os.path.join(project_dir, 'model', name, cid)
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    save_path = os.path.join(project_dir, 'model', name, cid, save_filename)
    torch.save(network.cpu().state_dict(), save_path)
    if torch.cuda.is_available():
        network.cuda(gpu_ids[0])

def get_model(class_sizes, drop_rate, stride):
    model = ft_net(class_sizes, drop_rate, stride)
    return model

# functions for testing federated model
def fliplr(img):
    """flip horizontal
    """
    inv_idx = torch.arange(img.size(3)-1,-1,-1).long()  # N x C x H x W, img.size()->[32,3,256,128], img.size(3)->128, [127,126,...,0]이 출력됨
    img_flip = img.index_select(3,inv_idx)#-img의 3번째 차원인 range(128)을 flpi한 [127,126, ...,0]의 형태로 오른쪽으로 뒤집은 이미지 내놓는다.
    return img_flip

def extract_feature(model, dataloaders, ms, device): #.cuda() 때문에 다른 device에 들어감!!
    features = torch.FloatTensor()
    for data in dataloaders:
        img, label = data
        n, c, h, w = img.size()
#         ff = torch.FloatTensor(n, 512).zero_().cuda()
        ff = torch.FloatTensor(n, 512).zero_().to(device) #(32,512), 여기서 32는 batch size, 512는 model의 feature vector size
        for i in range(2): #배치 내의 이미지와 오른쪽으로 뒤집은 것들의 feature vector output을 더한다
            if(i==1):
                img = fliplr(img)
            input_img = Variable(img.to(device))
            for scale in ms:
#                 if scale != 1: 일어나지 않음!!
#                     # bicubic is only  available in pytorch>= 1.1
#                     input_img = nn.functional.interpolate(input_img, scale_factor=scale, mode='bicubic', align_corners=False)
                outputs = model(input_img)
                ff += outputs #(32,512)짜리 끼리 더한다
        # norm feature
        fnorm = torch.norm(ff, p=2, dim=1, keepdim=True) #(32,1) size!! 이미지 각각에 대해 2 norm 구함
        ff = ff.div(fnorm.expand_as(ff))#(32,1) size인 fnorm을 ff size인 (32,512)사이즈에 맞게 복제하면서 강제로 (32,512)사이즈 벡터로 만듬, 그리고 ff (32,512) 사이즈를 elementwise하게 나눔!! 즉 각 이미지들의 feature vector를 normalize한다!!
        

        features = torch.cat((features,ff.data.cpu()), 0) #매 batch마다 (32,512) 사이즈를 concatenate한다. 최종적으로 얻어지는 것은 (# of data, 512) 사이즈가 되겠다.
    return features



