# (VnV) 경량 엣지 분석기반 추론 지연시간 개선율 (안)

- 현재 "초안" 입니다.


## 문서의 개요
- 본 문서는 개발한 cloud-edge-framework 를 기반으로 VnV(Verification and Validation)를 수행하기 위한 절차 및 관련 코드를 설명합니다.

## 요약
- 이기종의 에지 디바이스 연동 플랫폼 성능을 검증하고자 합니다.
- 연동 플랫폼의 성능은 추론 지연시간을 측정하여 정량적으로 평가합니다.




## 평가환경

### 기본 인프라

- 추론(분석)으로 인해 발생하는 종단 간 지연시간의 평균 개선율을 측정하기 위해 다음과 같이 클라우드-엣지 환경을 설정합니다.

#### 환경

- 제어용 컴퓨터 : {MacbookPro14}
- 프레임워크 서버 : {RTX3080ti GPU 서버}
- 에지 디바이스 : {RPI, TX2} + $\alpha$




### 평가 조건

- 이기종의 네트워크 대역폭 및 불안정한 Backgroud Utilization 환경을 고려하며, 엣지 단독 추론 및 병행추론 등 다양한 유형의 분석 방식 채택 가능합니다.

### 기준 알고리즘
- 주어진 태스크와 목적에 부합하는 딥러닝 모델 중 가장 우수한 정확도를 제공하는 모델을 엣지 추론을 위한 모델로 선정하는 Greedy Model Selection Algorithm 기준 알고리즘으로 선정합니다.

### 추론 Budget
- 엣지 추론을 위해 모델 선별 시 허용 가능한 추론 지연시간을 일종의 예산(Budget)개념으로 활용합니다.




### 사용할 Dataset은 다음과 같습니다.
---------------------------------------------------

- https://www.cs.toronto.edu/~kriz/cifar.html

- Cifar10 : 32x32 컬러 이미지, 10개의 분류객체, 클래스당 6000장(5000장 학습, 1000장 시험), 총 60000장(50000장 학습셋 + 10000장 시험셋)



## 기초 실험 결과 

### Cifar10 데이터셋에 대한 에지 기기별 동작 유무, 시간

- 수행 시간 및 정확도 (TX2의 경우 VGG19 inference)


```csv

model, RTX3080ti(GPU), RTX3080ti(CPU), TX2(CPU), RPI(CPU)
VGG19, 1.194, 35.162
SimpleDLA, 1.276, 



```


### (참고) 모델 크기

- (참고) https://github.com/albanie/convnet-burden

```csv
model,	input size,	param mem
resnet18,	224 x 224,	45 MB
resnet34,	224 x 224,	83 MB
resnet-50,	224 x 224,	98 MB
resnet-101,	224 x 224,	170 MB
```

### (참고) 임베디드 디바이스별 머신러닝 모델 동작

- 출처 : https://qengineering.eu/deep-learning-with-raspberry-pi-and-alternatives.html

![img](img4doc/device_chart.png)


















### 주요 참고문헌

```bibtex
@article{mathur2021device,
  title={On-device federated learning with flower},
  author={Mathur, Akhil and Beutel, Daniel J and de Gusmao, Pedro Porto Buarque and Fernandez-Marques, Javier and Topal, Taner and Qiu, Xinchi and Parcollet, Titouan and Gao, Yan and Lane, Nicholas D},
  journal={arXiv preprint arXiv:2104.03042},
  year={2021}
}
```