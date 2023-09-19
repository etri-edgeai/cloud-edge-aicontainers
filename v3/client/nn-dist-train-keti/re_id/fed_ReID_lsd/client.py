import time
import torch
from utils import get_optimizer, get_model
import torch.nn as nn
from torch.optim import lr_scheduler
import torch.nn.functional as F
from torch.autograd import Variable
import copy
from optimization import Optimization
from criterion import *

class Client():
    def __init__(self, cid, data, device, project_dir, model_name, local_epoch, lr, batch_size, drop_rate, stride, tau, beta):#drop_rate, stride는 모델에 대한 설정!!
        self.cid = cid
        self.project_dir = project_dir
        self.model_name = model_name
        self.data = data
        self.device = device
        self.local_epoch = local_epoch
        self.lr = lr
        self.batch_size = batch_size
        
        self.dataset_sizes = self.data.train_dataset_sizes[cid]
        self.train_loader = self.data.train_loaders[cid]
        self.full_model = get_model(self.data.train_class_sizes[cid], drop_rate, stride).to(self.device) #output: model
        self.classifier = self.full_model.classifier.classifier #model의 classifier 부분!!
        self.full_model.classifier.classifier = nn.Sequential() #empty!!
        self.model = self.full_model #self.full_model 중 feature extrator만 해당!!
        self.tau=tau
        self.beta=beta
        
        
    def train(self, federated_model, use_cuda, lr):        
        self.y_err = []
        self.y_loss = []
        self.model.load_state_dict(federated_model) #feature-extractor part!!

        self.model.classifier.classifier = self.classifier #client model에서 feature-extractor, classifier 연결!!
        self.model = self.model.to(self.device)

        optimizer = get_optimizer(self.model, lr)
        scheduler = lr_scheduler.StepLR(optimizer, step_size=40, gamma=0.1) #40 epoch마다 lr decay인데 local epoch수는 1이라 의미 없는듯
        class_num= self.data.train_class_sizes[self.cid]
        criterion = LSD_Loss(class_num, self.tau, self.beta)

        since = time.time()
        
        dg_model=copy.deepcopy(self.model)

        print('Client', self.cid, 'start training')
        for epoch in range(self.local_epoch):
            print('Epoch {}/{}, lr {}'.format(epoch, self.local_epoch - 1, optimizer.param_groups[0]['lr']))
            print('-' * 10)

            scheduler.step()
            self.model.train(True)
            running_loss = 0.0
            running_corrects = 0.0
            
            for data in self.train_loader:
                inputs, labels = data
                b, c, h, w = inputs.shape
                if b < self.batch_size:
                    continue
                if use_cuda:
                    inputs = Variable(inputs.to(self.device).detach())
                    labels = Variable(labels.to(self.device).detach())
                else:
                    inputs, labels = Variable(inputs), Variable(labels)
                
                optimizer.zero_grad()

                outputs, dg_logits = self.model(inputs), dg_model(inputs)
                _, preds = torch.max(outputs.data, 1)
                loss = criterion(outputs, labels, dg_logits)
                loss.backward()

                optimizer.step()

                running_loss += loss.item() * b
                running_corrects += float(torch.sum(preds == labels.data))

            used_data_sizes = (self.dataset_sizes - self.dataset_sizes % self.batch_size)
            epoch_loss = running_loss / used_data_sizes
            epoch_acc = running_corrects / used_data_sizes

            print('{} Loss: {:.4f} Acc: {:.4f}'.format(
                'train', epoch_loss, epoch_acc))

            self.y_loss.append(epoch_loss) #local epoch이 1이라 의미 없어진듯
            self.y_err.append(1.0-epoch_acc) #local epoch이 1이라 의미 없어진듯


        time_elapsed = time.time() - since #local iteration 하는데 걸린 시간
        print('Client', self.cid, 'Training complete in {:.0f}m {:.0f}s'.format(
            time_elapsed // 60, time_elapsed % 60))

        
        self.classifier = self.model.classifier.classifier
        self.model.classifier.classifier = nn.Sequential()



    def get_model(self):
        return self.model.cpu().state_dict()

    def get_data_sizes(self):
        return self.dataset_sizes

    def get_train_loss(self):
        return self.y_loss[-1]

