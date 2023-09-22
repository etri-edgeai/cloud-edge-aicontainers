#------------------------------------------------------
# VnV (ver. 3)
#------------------------------------------------------

## - by JPark
## - 모델 추가
## - 지연 시간 측정을 위한 코드 통합

#------------------------------------------------------
# Config
#------------------------------------------------------

from glob import iglob
# sample execution (requires torchvision)
from PIL import Image
from torchvision import transforms
import time
from tqdm import tqdm
import numpy as np
import torch
import argparse
import time

import socket
from collections import OrderedDict
from redis_connector import redis_connector
rcon = redis_connector()

def arg_parser():
    parser = argparse.ArgumentParser(description='KETI V&V 2023')
    parser.add_argument('--model', 
                        type=str, 
                        default='resnet18', 
                        metavar='N', 
                        help='neural network')
    parser.add_argument('--mode', 
                        type=str, 
                        default='baseline', 
                        metavar='N', 
                        help='{baseline, advanced}')
    parser.add_argument('--device', 
                        type=str, 
                        default='cuda', 
                        help='running device. e.g. {cpu, cuda, mps, ...}')
    parser.add_argument('--N', 
                        type=int, 
                        default=0, 
                        help='# of inference images')
    
    return parser
    
    print('-' * 50)
    print('ok')
    print('-' * 50)


def update_edge_result(od, mode):
    hostname = socket.gethostname()
    rcon.set_ordered_dict(f'vnv:edge:{mode}:{hostname}', od)
    print('output = ', rcon.get_ordered_dict(f'vnv:edge:{mode}:{hostname}'))
    
    
def run_main(model_names=['resnet152'], devices=['mps'], N=0, mode='baseline'):
    
    #---------------------------------------------------
    st_total = time.time()
    #---------------------------------------------------

    print ('hohoho')
    return 


    # Test images
    zip_images_url = 'http://keticmr.iptime.org:22080/edgeai/images/imagenet-mini-val.zip'
    zip_images = 'imagenet-mini-val.zip'
    dataset_root = './dataset'
    fpath_zip_images = dataset_root + '/' + zip_images
    fpath_testimages = dataset_root + '/imagenet-mini-val/'

    # Models
    urlroot = 'http://keticmr.iptime.org:22080/edgeai/models_jpark/'
    modeldir = './checkpoint/'

    model_names_resnet = [ 
        'resnet18',
        'resnet34',
        'resnet50',
        'resnet101',
        'resnet152',
    ]
    repo_resnet = 'pytorch/vision:v0.10.0'

    model_names_mobnet = [
        'mobilenet_v3_small',
        'mobilenet_v3_large',
    ]
    repo_mobnet = 'pytorch/vision:v0.10.0'

    model_names_effnet = [ 
        'nvidia_efficientnet_b0',
        'nvidia_efficientnet_b4',
        'nvidia_efficientnet_widese_b0',
        'nvidia_efficientnet_widese_b4',
    ]
    repo_effnet = 'NVIDIA/DeepLearningExamples:torchhub'


    #model_names = model_names_resnet + model_names_effnet + model_names_mobnet
    pth_names = [ model_name + '-dict.pth' for model_name in model_names ]

    urlmodels = []
    for pth_name in pth_names:
        urlmodels.append(urlroot + pth_name)

    model_fpaths = []
    for pth_name in pth_names:
        model_fpaths.append(modeldir + pth_name)

    ## load test images
    '''
    # read test files
    testfiles = []
    for fname in sorted( iglob(fpath_testimages + '**/*.JPEG', recursive=True) ):
        testfiles.append(fname)
    '''

    idx_gt = []
    idx = 0
    testfiles = []
    for d in sorted( iglob(fpath_testimages + 'n*', recursive=False) ):
        for fname in sorted( iglob(d + '/*.JPEG', recursive=True) ):
            testfiles.append(fname)
            idx_gt.append( idx )
        idx += 1


    # Read the categories
    with open("imagenet_classes.txt", "r") as f:
        categories = [s.strip() for s in f.readlines()]
        
        
        
    '''
    # Define transforms for the evaluation phase
    preprocess = transforms.Compose([transforms.Resize(256),
                                          transforms.CenterCrop(224),
                                          transforms.ToTensor(),
                                          transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
                                    ])
    '''

    preproc = ['method1', 'method2']
    preproc_method = 'method1'

    #devices = ['cuda', 'cpu']
    #devices = ['mps']
    models = []

    if N > 0:
        nn = min( len(testfiles), N )
        testset = testfiles[:nn]
    else:
        testset = testfiles[:]
        
    n = len(testset)
    
    # 디바이스별 반복
    for device in devices: 
        print('-'*50)
        print('[d] device = ', device, flush=True)
        print('-'*50)
        print('')
        
        # 모델별 반복
        for model_idx, model_name in enumerate(model_names):
            start = time.time() # strt timer        
            print(f'[d] model = {model_names[model_idx]}', flush=True)

            # 모델 템플릿 다운로드 (from torch.hub)
            if model_name in model_names_resnet:
                model = torch.hub.load(repo_resnet, model_name) #, pretrained=False)
            elif model_name in model_names_mobnet:
                model = torch.hub.load(repo_mobnet, model_name) #, pretrained=False)
            elif model_name in model_names_effnet:
                model = torch.hub.load(repo_effnet, model_name) #, pretrained=False)
            else:
                pass

            # 모델 가중치 다운로드 (from AI 모델 리포지토리)
            if False:    
                # 방법 1
                pass

                # torch.hub.download_url_to_file(urlroot+pthnames[model_idx], modeldir+pthnames[model_idx])
                # model.load_state_dict(torch.hub.load_state_dict_from_url(checkpoint, progress=False))
                # model.eval()
            else:
                # 방법 2
                checkpoint = urlmodels[model_idx]
                model.load_state_dict(torch.hub.load_state_dict_from_url(checkpoint, progress=False))
                model.eval().to(device) # change model to evauation mode (e.g. disable Dropout, BatchNorm)
                models.append(model)


            # 시험용 입력 영상
            top1_cnt = 0
            top5_cnt = 0
            top1_catids = []

            # 시험용 입력 영상 전처리 (크기 및 컬러채널)
            if preproc_method == preproc[0]:
                preprocess = transforms.Compose([
                    transforms.Resize(256),
                    transforms.CenterCrop(224),
                    transforms.ToTensor(),
                    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
                ])
            else:
                preprocess = transforms.Compose([
                    transforms.Resize(256),
                    transforms.CenterCrop(224),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
                ])

            # 시험영상별 반복
            imgidx = 0
            #for fpath in tqdm( testset ):
            for fpath in testset:
                #print( fpath )
                input_image = Image.open(fpath)

                try:
                    input_tensor = preprocess(input_image)
                except:
                    # gray scale to color
                    input_image = Image.open(fpath).convert("RGB")
                    input_tensor = preprocess(input_image)

                input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model

                # 디바이스 설정
                if device == 'cuda':
                    if torch.cuda.is_available():
                        # cuda
                        input_batch = input_batch.to('cuda')
                        model.to('cuda')
                    else:
                        input_batch = input_batch.to('cpu')
                        model.to('cpu')
                elif device == 'mps':
                    # mac
                    try:
                        input_batch = input_batch.to('mps')
                        model.to('mps')
                    except:
                        input_batch = input_batch.to('cpu')
                        model.to('cpu')
                else:
                    input_batch = input_batch.to('cpu')
                    model.to('cpu')

                with torch.no_grad():
                    output = model(input_batch)

                # Tensor of shape 1000, with confidence scores over Imagenet's 1000 classes
                #print(output[0])

                # The output has unnormalized scores. To get probabilities, you can run a softmax on it.
                probabilities = torch.nn.functional.softmax(output[0], dim=0)
                #print(probabilities)

                # Show top categories per image
                top5_prob, top5_catid = torch.topk(probabilities, 5)
                for i in range(top5_prob.size(0)):
                    #print(top5_catid[i])
                    #print(imgidx, ' ', categories[top5_catid[i]], top5_prob[i].item())

                    if( top5_catid[i] == idx_gt[imgidx] ):
                        top5_cnt += 1

                # Show top categories per image
                top1_prob, top1_catid = torch.topk(probabilities, 1)
                if( top1_catid[0] == idx_gt[imgidx] ):
                    top1_cnt += 1

                imgidx += 1

            end = time.time() # end timer

            print('-' * 70)
            print('GT')
            print('-' * 70)
            for idx, cid in enumerate(idx_gt):
                print(f'{idx:04d} = {cid}')

            print('-' * 70)
            print('Top1 category IDs')
            print('-' * 70)
            for idx, cid in enumerate(top1_catids):
                print(f'{idx:04d} = {int(cid)}')

            
            print('-' * 70)
            print('Precision')
            print('-' * 70)
            
            print('n = ', n)
            print('top1_cnt = ', top1_cnt)
            print('top1_acc = ', top1_cnt/n)
            print('top5_cnt = ', top5_cnt)
            print('top5_acc = ', top5_cnt/n)
            print('time = ', end - start)
            print('')

    #---------------------------------------------------
    et_total = time.time()
    #---------------------------------------------------
    
    od = OrderedDict()
    T = et_total - st_total
    od['total_inference_time'] = T
    update_edge_result(od, mode)

        
import sys
if __name__ == "__main__":
    
    # total arguments
    n = len(sys.argv)
    for i in range(1, n):
        print(sys.argv[i], end = " ")

    # arguments
    parser = arg_parser()
    args = parser.parse_args()
    
    # set argument
    model_names=[]
    model_names.append( args.model )
    devices=[]
    devices.append( args.device )
    N = int( int(args.N) )
    
    # core
    run_main(model_names=model_names, devices=devices, N = N )

#------------------------------------------------------
# End of this file
#------------------------------------------------------
