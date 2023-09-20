import scipy.io
import torch
import numpy as np
import os
import argparse


parser = argparse.ArgumentParser(description='Training')
parser.add_argument('--result_dir', default='.', type=str)
parser.add_argument('--dataset', default='no_dataset', type=str)
args = parser.parse_args()

#######################################################################
# Evaluate
def evaluate(qf, ql, qc, gf, gl, gc): #q는 imagel 1개
    
#Model Dependent!!   
    query = qf.view(-1, 1)#qf dimension 하나 더 늘림, 밑의 matrix 연산을 위한 용도 (512,1)
    score = torch.mm(gf, query)#cosine similarity 반환!! #(gallery size,1) 이 반환
    score = score.squeeze(1).cpu()#의미없는 dimension 줄임.
    score = score.numpy() #주어진 query에 대한 각 gallery image와 cosine similarity 모아놓음.
    # predict index
    index = np.argsort(score)  #from small to large
    index = index[::-1] #large to small(역순 출력), score 내림차순으로 index 매김

    
#Model independent but query dependent!!   
    # good index
    query_index = np.argwhere(gl==ql) #주어진 query와 label이 같은 gallery index 표시
    camera_index = np.argwhere(gc==qc) #주어진 query와 camera label이 같은 gallery index 표시

    good_index = np.setdiff1d(query_index, camera_index, assume_unique=True)#query_index \ camera_index i.e. query와 동일한 id인 gallery이미지 중 다른 카메라에 찍힌 index들만 추림, assume_unique는 input을 set 처리함!!, good_index가 index의 상단으로 가도록 학습을 유도해야함!!
    junk_index1 = np.argwhere(gl==-1) #label이 -1인 것은 redundant 한 것!!
    junk_index2 = np.intersect1d(query_index, camera_index) #주어진 query와 cameri_index, label_index 모두 같은 무의미한 gallery image index들
    junk_index = np.append(junk_index2, junk_index1) #.flatten())
    
    CMC_tmp = compute_mAP(index, good_index, junk_index)
    return CMC_tmp


def compute_mAP(index, good_index, junk_index):#index: query와 유사한 순으로 나열, good_index: index가 지향해야 할 것, junk_index: index가 지향하면 안되는 것 
    ap = 0
    cmc = torch.IntTensor(len(index)).zero_()#gallery size
    if good_index.size==0:   # if empty
        cmc[0] = -1
        return ap,cmc #cmc=[-1, 0, 0, 0,...,0]으로 return!!

    # remove junk_index
    mask = np.in1d(index, junk_index, invert=True)#https://runebook.dev/ko/docs/numpy/reference/generated/numpy.in1d
    #index의 각 element가 junk_index에 속하지 않으면 True!!
    index = index[mask] #True인 것만 추려냄(junk는 없애고 시작!!)

    # find good_index index
    ngood = len(good_index)
    mask = np.in1d(index, good_index)#index의 각 element가 good_index에 속하면 True!!
    rows_good = np.argwhere(mask==True)#junk 추려낸 것에서 good_index가 포함된 order(position)만 뽑아냄!!
    rows_good = rows_good.flatten()#element마다 list씌운것들을 list에 보관, 오름차순으로 될 것임. good_index가 index의 부분집합이었던 상황!!
    
    cmc[rows_good[0]:] = 1 #good index를 최초로 찾아낸 index 이후부터는 다 1로 처리!! dirac delta fct!! 
    for i in range(ngood): #rows_good[i]=i+1이길 바라는 상황!!
        d_recall = 1.0/ngood
        precision = (i+1)*1.0/(rows_good[i]+1)#rows_good[i]=i+1이길 바라는 상황!!, rows_good size는 ngood과 같은상황.지향하는 것은 rows_good=range(ngood)가 optimal
        if rows_good[i]!=0:
            old_precision = i*1.0/rows_good[i]
        else:
            old_precision=1.0
        ap = ap + d_recall*(old_precision + precision)/2

    return ap, cmc

######################################################################

if __name__ == '__main__':


    result = scipy.io.loadmat(args.result_dir + '/pytorch_result.mat')

    query_feature = torch.FloatTensor(result['query_f'])
    query_cam = result['query_cam'][0] #리스트 안에 리스트가 있어서
    query_label = result['query_label'][0] #리스트 안에 리스트가 있어서
    gallery_feature = torch.FloatTensor(result['gallery_f'])
    gallery_cam = result['gallery_cam'][0] #리스트 안에 리스트가 있어서
    gallery_label = result['gallery_label'][0] #리스트 안에 리스트가 있어서

    query_feature = query_feature.cuda()
    gallery_feature = gallery_feature.cuda()

    print(query_feature.shape)


    CMC = torch.IntTensor(len(gallery_label)).zero_() #gally_labe size와 같으며 다 0으로 채운 torch tensor, dtype=int.
    ap = 0.0

    for i in range(len(query_label)): #각 query image마다 iteration
        ap_tmp, CMC_tmp = evaluate(query_feature[i], query_label[i], query_cam[i], gallery_feature, gallery_label, gallery_cam)
        if CMC_tmp[0]==-1:
            continue
        CMC = CMC + CMC_tmp
        ap += ap_tmp

    CMC = CMC.float()
    CMC = CMC/len(query_label) #average CMC,CMC[i]: correct match가 k번째 ranking 안에 포함되는 비율
    print(args.dataset+' Rank@1:%f Rank@5:%f Rank@10:%f mAP:%f'%(CMC[0], CMC[4], CMC[9], ap/len(query_label)))
    print('-'*15)
    print()
