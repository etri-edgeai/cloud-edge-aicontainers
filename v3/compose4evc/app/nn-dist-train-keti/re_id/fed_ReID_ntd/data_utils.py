from torch.utils.data import Dataset
from PIL import Image
from torchvision import datasets, transforms
import os
import json
import torch
from random_erasing import RandomErasing
import sys
class ImageDataset(Dataset): #transform에 대한 옵션을 추가로 주기 위한 용도!!
    def __init__(self, imgs,  transform = None):
        self.imgs = imgs
        self.transform = transform

    def __len__(self):
        return len(self.imgs)

    def __getitem__(self, index):
        data,label = self.imgs[index]
        return self.transform(Image.open(data)), label


class Data():
    def __init__(self, datasets, data_dir, batch_size, erasing_p, color_jitter, train_all):
        self.datasets = datasets.split(',')
        self.batch_size = batch_size
        self.erasing_p = erasing_p
        self.color_jitter = color_jitter
        self.data_dir = data_dir
        self.train_all = '_all' if train_all else ''
        
    def transform(self):
        transform_train = [
                transforms.Resize((256,128), interpolation=3),
                transforms.Pad(10),
                transforms.RandomCrop((256,128)),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                ]

        transform_val = [
                transforms.Resize(size=(256,128),interpolation=3),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                ]

        if self.erasing_p > 0:
            transform_train = transform_train + [RandomErasing(probability=self.erasing_p, mean=[0.0, 0.0, 0.0])]

        if self.color_jitter:
            transform_train = [transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0)] + transform_train

        self.data_transforms = {
            'train': transforms.Compose(transform_train),
            'val': transforms.Compose(transform_val),
        }        



    def preprocess_one_train_dataset(self, dataset): # 한 클라이언트의 train dataset, train loader를 output으로 내놓는다.
        """preprocess a training dataset, construct a data loader.
        """
        data_path = os.path.join(self.data_dir, dataset, 'pytorch')#data/dataset/pytorch
        data_path = os.path.join(data_path, 'train' + self.train_all)#data/dataset/pytorch/train
        image_dataset = datasets.ImageFolder(data_path)#id별로 계층화 된 것!!

        loader = torch.utils.data.DataLoader(
            ImageDataset(image_dataset.imgs, self.data_transforms['train']), 
            batch_size=self.batch_size,
            shuffle=True, 
            num_workers=2, 
            pin_memory=False)

        return loader, image_dataset

    def preprocess_train(self): #모든 client의 train data 정보들을 저장!!
        """preprocess training data, constructing train loaders
        """
        self.train_loaders = {}
        self.train_dataset_sizes = {}
        self.train_class_sizes = {}
        self.client_list = []
        
        for dataset in self.datasets:
            self.client_list.append(dataset)
          
            loader, image_dataset = self.preprocess_one_train_dataset(dataset)

            self.train_dataset_sizes[dataset] = len(image_dataset) #dataset내의 이미지 갯수
            self.train_class_sizes[dataset] = len(image_dataset.classes) #dataset내의 id 갯수(폴더 갯수), ImageFolder의 장점!!
            self.train_loaders[dataset] = loader
            
        print('Train dataset sizes:', self.train_dataset_sizes)#각 데이타 셋 별로 이미지 갯수 나열한 리스트를 반환.
        print('Train class sizes:', self.train_class_sizes) #각 데이타 셋 별로 id 갯수 나열한 리스트를 반환.
        
    def preprocess_test(self):
        """preprocess testing data, constructing test loaders
        """
        self.test_loaders = {}
        self.gallery_meta = {}
        self.query_meta = {}

        for test_dir in self.datasets:
            test_dir = 'data/'+test_dir+'/pytorch' #test_dir은 dataset name!!
            dataset = test_dir.split('/')[1]#[data, test_dir, pytorch] 중 1st index return. 즉 데이타 셋 폴더명 리턴!! 
            gallery_dataset = datasets.ImageFolder(os.path.join(test_dir, 'gallery'))
            query_dataset = datasets.ImageFolder(os.path.join(test_dir, 'query'))
            gallery_dataset = ImageDataset(gallery_dataset.imgs, self.data_transforms['val'])#transformation 옵션 추가, dataloader에 쓰임, gallery_dataset.imgs는 리스트 안에 튜플들의 집합으로 튜플은 input image 파일, 그리고 image 파일에 해당하는 상위 라벨 폴더 이름의 꼴로 구성됨.

            query_dataset = ImageDataset(query_dataset.imgs, self.data_transforms['val'])#transformation 옵션 추가, dataloader에 쓰임

            self.test_loaders[dataset] = {key: torch.utils.data.DataLoader(
                                                dataset, 
                                                batch_size=self.batch_size,
                                                shuffle=False, 
                                                num_workers=8, 
                                                pin_memory=True) for key, dataset in {'gallery': gallery_dataset, 'query': query_dataset}.items()} #test_loader에는 gallery, query 두개의 item으로 구성된 dictionary로 구성됨
        

            gallery_cameras, gallery_labels = get_camera_ids(gallery_dataset.imgs)
#             a=list(set(gallery_cameras))
#             b=list(set(gallery_labels))

            self.gallery_meta[dataset] = {
                'sizes':  len(gallery_dataset),
                'cameras': gallery_cameras,
                'labels': gallery_labels
            }

            query_cameras, query_labels = get_camera_ids(query_dataset.imgs)
            self.query_meta[dataset] = {
                'sizes':  len(query_dataset),
                'cameras': query_cameras,
                'labels': query_labels
            }
#             c=list(set(gallery_cameras))
#             d=list(set(gallery_labels))
            
#             print(a is c)
#             print(b is d)
            print('Dataset:{}'.format(dataset))
            print('Query Sizes:', self.query_meta[dataset]['sizes'])
            print('Gallery Sizes:', self.gallery_meta[dataset]['sizes'])

    def preprocess(self):
        self.transform() #self.transform 형성!!
        self.preprocess_train()#ImageDataset 통해 transformation
        self.preprocess_test()#ImageDataset 통해 transformation

def get_camera_ids(img_paths):
    """get camera id and labels by image path
    """
    camera_ids = []
    labels = []
    for path, v in img_paths:# path는 jpg file 객체, v는 그 위의 id 폴더명
        filename = os.path.basename(path)
        if filename[:3]!='cam':#e.g.) path-> data/Market/pytorch/gallery/-1/-1_c1s1_000401_03.jpg, filename-> -1_c1s1_000401_03.jpg
            label = filename[0:4]#-1_c
            camera = filename.split('c')[1]#1s1~
            camera = camera.split('s')[0]#1
        else:#e.g.) path->data/cuhk01/pytorch/gallery/1/cam_1_00001_00000.png, filename->cam_1_00001_00000.png
            label = filename.split('_')[2]#00001
            camera = filename.split('_')[1]#1
        if label[0:2]=='-1':#-1_c1s1_000401_03.jpgs는 여기 또 걸림!!
            labels.append(-1)
        else:
            labels.append(int(label))
        camera_ids.append(int(camera[0]))
    return camera_ids, labels
