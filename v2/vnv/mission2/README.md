# (VnV) 경량 엣지 분석기반 추론 지연시간 개선율 (안)

- 현재 "초안" 입니다.


---------------------------------------------------
## 문서의 개요
- 본 문서는 개발한 cloud-edge-framework 를 기반으로 VnV(Verification and Validation)를 수행하기 위한 절차 및 관련 코드를 설명합니다.

## 요약
- 이기종의 에지 디바이스 연동 플랫폼 성능을 검증하고자 합니다.
- 연동 플랫폼의 성능은 추론 지연시간을 측정하여 정량적으로 평가합니다.


<img src="img4doc/00_system.png" width=450>


<img src="img4doc/00_system4vnv.png" width=450>


---------------------------------------------------
## 평가시 고려사항 (사업계획서)

### 기본 인프라

- 추론(분석)으로 인해 발생하는 종단 간 지연시간의 평균 개선율을 측정하기 위해 다음과 같이 클라우드-엣지 환경을 설정합니다. [출처: 사업계획서] 

### 평가 환경 및 조건

- 이기종의 네트워크 대역폭 및 불안정한 Backgroud Utilization 환경을 고려하며, 엣지 단독 추론 및 병행추론 등 다양한 유형의 분석 방식 채택 가능합니다. [출처: 사업계획서] 

### 기준 알고리즘
- 주어진 태스크와 목적에 부합하는 딥러닝 모델 중 가장 우수한 정확도를 제공하는 모델을 엣지 추론을 위한 모델로 선정하는 Greedy AI Model Selection Algorithm을 기준 알고리즘으로 선정합니다. [출처: 사업계획서] 

### 추론 Budget
- 엣지 추론을 위해 모델 선별 시 허용 가능한 추론 지연시간을 일종의 예산(Budget)개념으로 활용합니다. [출처: 사업계획서] 


---------------------------------------------------
## (KETI 초안) 시험 방법

- 에지 환경 추론에 따른 성능 개선을 확인하기 위해, 성능 확인에 영향을 주는 변인들은 가급적 통제하여 평가를 실시합니다.
- 상세하게는 다음과 같은 2가지 시험 구성 {Baseline, Advanced}에 따라 평가를 진행합니다.
- {Baseline}과 {Advanced}의 시험 구성에 따른 추론 지연시간을 각각 $t_{b}$, $t_{a}$ 와 같이 측정합니다.
- 이를 비교하여 추론 지연시간 개선율을 계산합니다.

$$  \Delta {t} = \frac{1}{n} \sum_{i=1}^{n} \frac{ t_{b} -  t_{a} }{ t_{b} } $$

- {Baseline}과 {Advanced}의 주요 차이점은 추론 모델 선택에 있습니다.
- (1) {Baseline}은 가용 모델 중, 가장 성능이 우수한 분석 모델을 선택하는 <b>{Greedy AI Model Selection}</b> 을 사용합니다.
- (2) {Advanced}는 장치의 {연산량, 연산자원, 네트워크 대역폭} 등을 고려하여 10% 이내의 정확도 열화를 Latency Budget으로 사용하여 추론 모델을 선택하는 <b>{Advanced AI Model Selection}</b> 을 사용합니다. 
- 상기 2가지 시험 구성을 분리하여 설명했으나, 세부 시험 구성요소는 변인통제를 위해 서로 공유가 가능합니다.
- 일례로, {Control Node, Inference Node, Model Repository}는 추론지연시간 측정을 위해 그 기능을 공유합니다.
- 에지 디바이스의 종류는 1개를 기본으로 하고 그 이상으로 확장될 수 있습니다.


### 시험 방법




- 시험방법은 다음의 python 문법 형식의 의사코드로 표현할 수 있습니다.

```python

methods = ['baseline', 'advanced']
edges = [ 'RTX3080TI'] # ['RTX3080TI', 'NUC', 'MACMINI', 'RPI']
models = ['resnet18', 'resnet34', 'resnet50', 'resnet101', 'resnet152']
measured_time = []

# 가용 에지 디바이스들에 대해서 실험을 수행합니다.
for edge in edges:
    
    # 선택된 에지 디바이스의 상태정보를 얻습니다.
    device_status = getDeviceStatus(edge)

    # baseline 실험을 위한 모델을 선택합니다.
    model_baseline = greedModelSelection(models, device_status)
    
    # advanced 실험을 위한 모델을 선택합니다.
    model_advanced = advancedModelSelection(models, device_status)

    # 선택된 에지 디바이스에서 model_baseline을 수행합니다. 
    start_time = getTime()
    accuracy1 = runModel(model_baseline, edge)
    finish_time = getTime()
    dtime1 = finish_time - start_time

    # 선택된 에지 디바이스에서 model_advanced를 수행합니다. 
    start_time = getTime()
    accuracy2 = runModel(model_advanced, edge)
    finish_time = getTime()
    dtime2 = finish_time - start_time

    # 추론지연 절감율 측정
    latency_saving_rate = (dtime1 - dtime2) / dtime1
    diff_accuracy = accuracy1 - accuracy2
    
```

- diff_accuracy 가 10% 이내 인지 확인합니다.
- latency_saving_rate 가 20% 이상인지 확인합니다.


### 시험 구성 1 (Baseline)

- {Baseline}에서는 종래의 가장 성능이 우수한 모델을 선택하는 방식을 사용하는 {Greedy AI Model Selection} 방법을 사용하는 것을 특징으로 합니다.

- 주요 시험 구성요소는 다음과 같습니다.

  (1) Control Node (제어노드) : {MacbookPro14} --> <b>{Greedy AI Model Selection}</b> 적용

  (2) Model Repository (인공신경망 모델 리포지토리)

  (3) Inference Node (추론 노드) : {e.g. NUC GPU Edge Device, RTX3080Ti GPU Server, Macbook, RPI}


<img src="img4doc/01_baseline.png" width=500>



<img src="img4doc/expr01.png" width=200>


<img src="img4doc/expr02.png" width=200>




### 시험 구성 2 (Advanced)

- {Advanced}는 장치의 {연산량, 연산자원, 네트워크 대역폭} 등을 고려하여 10% 이내의 정확도 열화를 Latency Budget으로 사용하여 추론 모델을 선택하는 <b>{Advanced Model Selection}</b> 을 사용하는 것을 특징으로 합니다.

- 주요 시험 구성요소는 다음과 같습니다.

  (1) Control Node (제어노드) : {MacbookPro14} --> <b>{Advanced AI Model Selection}</b> 적용

  (2) Model Repository (인공신경망 모델 리포지토리)

  (3) Inference Node (추론 노드) : {e.g. NUC GPU Edge Device, RTX3080Ti GPU Server, Macbook, RPI}


<img src="img4doc/02_advanced.png" width=500>




### 사용 Dataset

- imagenet-mini 데이터셋 중에서 validatation 셋 (1,000개의 분류객체, 클래스당 약 3장씩, 3,923장)


```bash
  . https://www.kaggle.com/datasets/ifigotin/imagenetmini-1000
```

<img src="img4doc/ILSVRC2012_val_00003382.jpg" width=300>

<img src="img4doc/ILSVRC2012_val_00010218.jpg" width=300>



### 사용 모델

- Resnet 모델을 사용중입니다.
- Resnet 모델 테스트 완료후, EfficientNet 계열의 모델을 추가할 계획입니다. 
- 향후 지식증류 모델을 적용하는 것도 고려할 수 있습니다.
- 일례로, {Baseline}실험은 RESNET101을 사용했다면, {Advanced}에서는 RESNET18을 사용하여 모델 전송에 드는 오버헤드를 줄이고, 추론시간을 줄이고 가용 자원을 효율적으로 사용하는 것이 바람직합니다.


- 참고 자료 출처 : https://pytorch.org/hub/pytorch_vision_resnet/

```csv
Model structure,	Top-1 error,	Top-5 error
resnet18,	30.24,	10.92
resnet34,	26.70,	8.58
resnet50,	23.85,	7.13
resnet101,	22.63,	6.44
resnet152,	21.69,	5.94
```


- Resnet 모델의 크기

| model | input size | param mem | feat. mem | flops | src | performance |
|-------|------------|--------------|----------------|-------|-----|-------------|
| [resnet18](reports/resnet18.md) | 224 x 224 | 45 MB | 23 MB | 2 GFLOPs | PT | 30.24 / 10.92 |
| [resnet34](reports/resnet34.md) | 224 x 224 | 83 MB | 35 MB | 4 GFLOPs | PT | 26.70 / 8.58 |
| [resnet-50](reports/resnet-50.md) | 224 x 224 | 98 MB | 103 MB | 4 GFLOPs | MCN | 24.60 / 7.70 |
| [resnet-101](reports/resnet-101.md) | 224 x 224 | 170 MB | 155 MB | 8 GFLOPs | MCN | 23.40 / 7.00 |
| [resnet-152](reports/resnet-152.md) | 224 x 224 | 230 MB | 219 MB | 11 GFLOPs | MCN | 23.00 / 6.70 |



## (진행중) 장치별 기초 실험 

- Cifar10, test set 10,000장에 대한 에지 기기별 추론 시간 및 정확도
- 현재는 서로 다른 환경에서 만든 전이학습 모델을 사용중임 --> 동일한 전이학습 모델로 추론 하도록 실험 수정할 것임



- 추론 정확도 budget

```csv
model, RTX3080ti(GPU), RTX3080ti(CPU), NUC(GPU), NUC(CPU),
resnet18, 91.04, todo, 86.72, todo,
resnet34, 92.84, todo, 88.19, todo,
resnet-50, 93.37, todo, 89.38, todo,
resnet-101, 94.4, todo, 91.73, todo,
resnet-152, 95.11, todo, 91.3, todo,
```

<img src="experiments/resnet_infer_accuracy.png" width="600">

- 추론 지연시간 budget


<img src="experiments/resnet_infer_time.png" width="600">

<img src="experiments/time_cpu.png" width="600">

<img src="experiments/time_gpu.png" width="600">


```csv

model, RTX3080ti(GPU), RTX3080ti(CPU), NUC(GPU), NUC(CPU),
resnet18, 16.803656101226807, 169.54597854614258, 23.278241872787476, todo,
resnet34, 17.141077518463135, 280.5474326610565, 31.52906036376953, todo,
resnet-50, 19.997405767440796, 523.9516932964325, 43.629743814468384, todo,
resnet-101, 25.875438451766968, 805.4357748031616, 65.02895927429199, todo,
resnet-152, 30.793837785720825, 1121.0137231349945, 87.38637733459473, todo,
```


### (참고) 임베디드 디바이스별 분석모델 처리 속도

- 그림 출처 : https://qengineering.eu/deep-learning-with-raspberry-pi-and-alternatives.html

![img](img4doc/device_chart.png)



### (참고) RESNET 구조

- Resnet18
<img src="img4doc/resnet18.png" height="300">

- Resnet34
<img src="img4doc/resnet34.png" height="300">


- Resnet50
<img src="img4doc/resnet50.png" height="300">


- Resnet101
<img src="img4doc/resnet101.png" height="300">

- Resnet152
<img src="img4doc/resnet152.png" height="300">


### (참고) 모델의 크기

. 참고 자료 출처 : https://github.com/albanie/convnet-burden


| model | input size | param mem | feat. mem | flops | src | performance |
|-------|------------|--------------|----------------|-------|-----|-------------|
| [alexnet](reports/alexnet.md) | 227 x 227 | 233 MB | 3 MB | 727 MFLOPs | MCN | 41.80 / 19.20 |
| [caffenet](reports/caffenet.md) | 224 x 224 | 233 MB | 3 MB | 724 MFLOPs | MCN | 42.60 / 19.70 |
| [squeezenet1-0](reports/squeezenet1-0.md) | 224 x 224 | 5 MB | 30 MB | 837 MFLOPs | PT | 41.90 / 19.58 |
| [squeezenet1-1](reports/squeezenet1-1.md) | 224 x 224 | 5 MB | 17 MB | 360 MFLOPs | PT | 41.81 / 19.38 |
| [vgg-f](reports/vgg-f.md) | 224 x 224 | 232 MB | 4 MB | 727 MFLOPs | MCN | 41.40 / 19.10 |
| [vgg-m](reports/vgg-m.md) | 224 x 224 | 393 MB | 12 MB | 2 GFLOPs | MCN | 36.90 / 15.50 |
| [vgg-s](reports/vgg-s.md) | 224 x 224 | 393 MB | 12 MB | 3 GFLOPs | MCN | 37.00 / 15.80 |
| [vgg-m-2048](reports/vgg-m-2048.md) | 224 x 224 | 353 MB | 12 MB | 2 GFLOPs | MCN | 37.10 / 15.80 |
| [vgg-m-1024](reports/vgg-m-1024.md) | 224 x 224 | 333 MB | 12 MB | 2 GFLOPs | MCN | 37.80 / 16.10 |
| [vgg-m-128](reports/vgg-m-128.md) | 224 x 224 | 315 MB | 12 MB | 2 GFLOPs | MCN | 40.80 / 18.40 |
| [vgg-vd-16-atrous](reports/vgg-vd-16-atrous.md) | 224 x 224 | 82 MB | 58 MB | 16 GFLOPs | N/A | - / -  |
| [vgg-vd-16](reports/vgg-vd-16.md) | 224 x 224 | 528 MB | 58 MB | 16 GFLOPs | MCN | 28.50 / 9.90 |
| [vgg-vd-19](reports/vgg-vd-19.md) | 224 x 224 | 548 MB | 63 MB | 20 GFLOPs | MCN | 28.70 / 9.90 |
| [googlenet](reports/googlenet.md) | 224 x 224 | 51 MB | 26 MB | 2 GFLOPs | MCN | 34.20 / 12.90 |
| [resnet18](reports/resnet18.md) | 224 x 224 | 45 MB | 23 MB | 2 GFLOPs | PT | 30.24 / 10.92 |
| [resnet34](reports/resnet34.md) | 224 x 224 | 83 MB | 35 MB | 4 GFLOPs | PT | 26.70 / 8.58 |
| [resnet-50](reports/resnet-50.md) | 224 x 224 | 98 MB | 103 MB | 4 GFLOPs | MCN | 24.60 / 7.70 |
| [resnet-101](reports/resnet-101.md) | 224 x 224 | 170 MB | 155 MB | 8 GFLOPs | MCN | 23.40 / 7.00 |
| [resnet-152](reports/resnet-152.md) | 224 x 224 | 230 MB | 219 MB | 11 GFLOPs | MCN | 23.00 / 6.70 |
| [resnext-50-32x4d](reports/resnext-50-32x4d.md) | 224 x 224 | 96 MB | 132 MB | 4 GFLOPs | L1 | 22.60 / 6.49 |
| [resnext-101-32x4d](reports/resnext-101-32x4d.md) | 224 x 224 | 169 MB | 197 MB | 8 GFLOPs | L1 | 21.55 / 5.93 |
| [resnext-101-64x4d](reports/resnext-101-64x4d.md) | 224 x 224 | 319 MB | 273 MB | 16 GFLOPs | PT | 20.81 / 5.66 |
| [inception-v3](reports/inception-v3.md) | 299 x 299 | 91 MB | 89 MB | 6 GFLOPs | PT | 22.55 / 6.44 |
| [SE-ResNet-50](reports/SE-ResNet-50.md) | 224 x 224 | 107 MB | 103 MB | 4 GFLOPs | SE | 22.37 / 6.36 |
| [SE-ResNet-101](reports/SE-ResNet-101.md) | 224 x 224 | 189 MB | 155 MB | 8 GFLOPs | SE | 21.75 / 5.72 |
| [SE-ResNet-152](reports/SE-ResNet-152.md) | 224 x 224 | 255 MB | 220 MB | 11 GFLOPs | SE | 21.34 / 5.54 |
| [SE-ResNeXt-50-32x4d](reports/SE-ResNeXt-50-32x4d.md) | 224 x 224 | 105 MB | 132 MB | 4 GFLOPs | SE | 20.97 / 5.54 |
| [SE-ResNeXt-101-32x4d](reports/SE-ResNeXt-101-32x4d.md) | 224 x 224 | 187 MB | 197 MB | 8 GFLOPs | SE | 19.81 / 4.96 |
| [SENet](reports/SENet.md) | 224 x 224 | 440 MB | 347 MB | 21 GFLOPs | SE | 18.68 / 4.47 |
| [SE-BN-Inception](reports/SE-BN-Inception.md) | 224 x 224 | 46 MB | 43 MB | 2 GFLOPs | SE | 23.62 / 7.04 |
| [densenet121](reports/densenet121.md) | 224 x 224 | 31 MB | 126 MB | 3 GFLOPs | PT | 25.35 / 7.83 |
| [densenet161](reports/densenet161.md) | 224 x 224 | 110 MB | 235 MB | 8 GFLOPs | PT | 22.35 / 6.20 |
| [densenet169](reports/densenet169.md) | 224 x 224 | 55 MB | 152 MB | 3 GFLOPs | PT | 24.00 / 7.00 |
| [densenet201](reports/densenet201.md) | 224 x 224 | 77 MB | 196 MB | 4 GFLOPs | PT | 22.80 / 6.43 |
| [mcn-mobilenet](reports/mcn-mobilenet.md) | 224 x 224 | 16 MB | 38 MB | 579 MFLOPs | AU | 29.40 / - |



### (참고) 데이터셋

- Cifar10 데이터셋

```bash
  . https://www.cs.toronto.edu/~kriz/cifar.html

  . Cifar10 : 32x32 컬러 이미지, 10개의 분류객체, 클래스당 6,000장(5000장 학습, 1000장 시험), 총 60,000장(50,000장 학습셋 + 10,000장 시험셋)

```










### 주요 참고문헌

```bibtex
@article{mathur2021device,
  title={On-device federated learning with flower},
  author={Mathur, Akhil and Beutel, Daniel J and de Gusmao, Pedro Porto Buarque and Fernandez-Marques, Javier and Topal, Taner and Qiu, Xinchi and Parcollet, Titouan and Gao, Yan and Lane, Nicholas D},
  journal={arXiv preprint arXiv:2104.03042},
  year={2021}
}

@article{liu2022unifed,
  title={UniFed: A Benchmark for Federated Learning Frameworks},
  author={Liu, Xiaoyuan and Shi, Tianneng and Xie, Chulin and Li, Qinbin and Hu, Kangping and Kim, Haoyu and Xu, Xiaojun and Li, Bo and Song, Dawn},
  journal={arXiv preprint arXiv:2207.10308},
  year={2022}
}
```