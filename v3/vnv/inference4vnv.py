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

from model_selector import ModelSelection
from device_info import get_model4infer, get_device_info
from job_allocator import job_allocator

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
    parser.add_argument('--fpath_testimages', 
                        type=str, 
                        default='', 
                        metavar='N', 
                        help='fpath_testimages')
    return parser
    
    print('-' * 50)
    print('ok')
    print('-' * 50)

        
def set_edge_done_frames(cnt, mode):
    hostname = socket.gethostname()
    
    if mode == 'getinfo':
        pass
    else:
        rcon.set_data(f'vnv:edge:{mode}:{hostname}:done_frames', cnt)


            
def set_cluster_frame_result(ods, model_name, mode, start_frame):
    hostname = socket.gethostname()
    
    #print('=' * 55)
    #print(f'ods = {ods}')
    
    if mode == 'getinfo':
        pass
    else:
        for idx, od in enumerate(ods):
            #fnum = idx + start_frame
            fnum = int(od['idx'])
            rcon.hmset(f'vnv:edge:advanced:cluster_frame:{fnum:04d}', od)
            #print('output = ', rcon.hgetall(f'vnv:edge:{mode}:{hostname}:frame:{idx:04d}'))

def set_edge_frame_result(ods, model_name, mode):
    hostname = socket.gethostname()
    
    #print(f'ods = {ods}')
    if mode == 'getinfo':
        pass
    else:
        for idx, od in enumerate(ods):
            fnum = int(od['idx'])
            rcon.hmset(f'vnv:edge:{mode}:{hostname}:frame:{fnum:04d}', od)
            #print('output = ', rcon.hgetall(f'vnv:edge:{mode}:{hostname}:frame:{idx:04d}'))
    
def set_edge_stat_result(od, model_name, mode):
    hostname = socket.gethostname()
    
    if mode == 'getinfo':
        rcon.hmset(f'vnv:edge:ministat:{hostname}:{model_name}', od)
        #print('output = ', rcon.hgetall(f'vnv:edge:info:{hostname}:{model_name}'))
    else:
        rcon.hmset(f'vnv:edge:{mode}:{hostname}:stat', od)
        #print('output = ', rcon.hgetall(f'vnv:edge:{mode}:{hostname}:stat'))


def run_main(model_names=['mobilenet_v3_small'], mode='baseline', fpath_testimages=''):
    hostname = socket.gethostname()
    
    #---------------------------------------------------
    # EVC에서 에지 디바이스별로 맞춤 설정한 정보에 따라 추론 수행
    #---------------------------------------------------

    device_info = get_device_info()

    #print('-'*45)
    #print(f'device_info = {device_info}')
    #print(f'type(device_info) = {type(device_info)}')
    #print('-'*45)


    #----------------------------------
    # 추론을 위한 AI 모델을 선택합니다.
    #----------------------------------
    model_selector = ModelSelection()
    if mode == 'baseline':
        model_selector.greedModelSelection()
    elif mode == 'advanced':
        model_selector.advancedModelSelection()

    
    if int(device_info[b'num_of_cuda_devices']) > 0:
        device = 'cuda'
    else: 
        device = 'cpu'
        
    if mode == 'getinfo':
        # 간단한 모델을 실행하여 디바이스별 상대적 성능정보를 얻습니다.
        model_names = ['mobilenet_v3_small',
                       'mobilenet_v3_large',
                       'resnet18',
                       'resnet34',
                       'resnet50',
                       'resnet101',
                       'resnet152',
                       'nvidia_efficientnet_b0',
                       'nvidia_efficientnet_b4',
                       'nvidia_efficientnet_widese_b0',
                       'nvidia_efficientnet_widese_b4',
                      ]
    else:
        s = device_info[b'model4infer'].decode('utf-8')
        model_names = [ s ]

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

    model_yolo = [
        'yoloX.pt',
        'yoloL.pt',
        'yoloM.pt',
        'yoloN.pt',
        'yoloS.pt',
        'cocoX.pt',
        'cocoL.pt',
        'cocoM.pt',
        'cocoN.pt',
        'cocoS.pt',
    ]


    #model_names = model_names_resnet + model_names_effnet + model_names_mobnet
    pth_names = [ model_name + '-dict.pth' for model_name in model_names ]

    urlmodels = []
    for pth_name in pth_names:
        urlmodels.append(urlroot + pth_name)
    #print('*'*55)
    #print(f'urlmodels = {urlmodels}')
    #print('*'*55)
    
    model_fpaths = []
    for pth_name in pth_names:
        model_fpaths.append(modeldir + pth_name)

    # Load images
    idx_gt = []
    idx = 0
    testfiles = []
    for d in sorted( iglob(fpath_testimages + 'n*', recursive=False) ):
        for fname in sorted( iglob(d + '/*.JPEG', recursive=True) ):
            testfiles.append(fname)
            idx_gt.append( idx )
        idx += 1

    # Read the categories
    with open("./config/imagenet_classes.txt", "r") as f:
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

 
    #if N > 0:
    #    nn = min( len(testfiles), N )
    #    testset = testfiles[:nn]
    #else:
    
    
    if True:
        for model_idx, model_name in enumerate(model_names):

            start = time.time() # strt timer        
            print(f'[d] model_name = {model_names[model_idx]}', flush=True)

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
                #models.append(model)


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

            # imgidx_start = ja.start
            # imgidx_end = len(testfiles)
            n = len(testfiles)

            if mode == 'advanced':
                ja = job_allocator()
                imgidx_start, imgidx_end = ja.get_job(hostname)
            else:
                imgidx_start = 0
                imgidx_end = n
            
            #print(f'imgidx_start = {imgidx_start}')
            #print(f'imgidx_end = {imgidx_end}')
            #print('='*55)
            
            icnt = 0
            imgidx = imgidx_start
            for fpath in testfiles[imgidx_start:imgidx_end]:
   
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
                    
                top1_catids.append( {'idx' : imgidx,
                                     'idx_gt' : int(idx_gt[imgidx]),
                                     'top1_catid' : int(top1_catid), 
                                     'is_true' : str(int(idx_gt[imgidx]) == int(top1_catid)), 
                                     'top1_prob' : float(top1_prob)}
                                  )

                icnt += 1
                imgidx = imgidx_start + icnt

                # 임시
                if mode == 'getinfo':
                    #pass
                    if icnt > 100:
                        break
                else:
                    #pass
                    if icnt > 10:
                        break
                        
                        
                if (icnt)%10 == 0:
                    set_edge_done_frames(icnt, mode)
                
            end = time.time() # end timer
            time_duration = end - start
            num_of_test_images = imgidx
            
            #print('-' * 70)
            #print('GT')
            #print('-' * 70)
            #for fidx, cid in enumerate(idx_gt):
            #    print(f'{fidx:04d} = {cid}')
            
            print('-' * 70)
            print('Precision')
            print('-' * 70)
            
            print('n = ', n)
            print('top1_cnt = ', top1_cnt)
            print('top1_acc = ', top1_cnt/num_of_test_images)
            print('top5_cnt = ', top5_cnt)
            print('top5_acc = ', top5_cnt/num_of_test_images)
            print('time_duration = ', time_duration)
            od_stat_result = OrderedDict({
                           'n':n,
                           'num_of_test_images':num_of_test_images,
                           'top1_cnt':top1_cnt, 
                           'top1_acc':top1_cnt/num_of_test_images, 
                           'top5_cnt':top5_cnt, 
                           'top5_acc':top5_cnt/num_of_test_images,
                           'model_name':model_name,
                           'time_duration':time_duration,
                           'device':device
                        })
            set_edge_stat_result(od_stat_result, model_name, mode)
            set_edge_frame_result(top1_catids, model_name, mode)
            set_cluster_frame_result(top1_catids, model_name, mode, imgidx_start)

            print('OK')

        
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
    mode = args.mode
    fpath_testimages = args.fpath_testimages
    
    # core
    run_main(model_names = model_names, 
             mode = mode, 
             fpath_testimages = fpath_testimages )

#------------------------------------------------------
# End of this file
#------------------------------------------------------
