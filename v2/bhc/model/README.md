# 예측 테스트 모델 제작

### Image Classification Pre-Trained Models
```bash
## how to start
$ python classifier.py
```
- Pytorch Hub의 ResNet, EfficientNet, MobileNet을 사용했습니다.
- CIFAR10 Dataset으로 학습되었습니다.
  - 10개의 클래스를 예측할 수 있습니다.
    - classes : plane, car, bird, cat, deer, dog, frog, horse, ship, truck
- device CPU만 동작합니다.

### structures
#### classifier.py
- 데이터 전처리를 수행합니다.
- 예측 수행 및 결과 출력을 수행합니다.
- ArgumentParser를 선언하여 인자를 전달 받습니다.

#### load_model.py
- Pytorch Hub로부터 base-model을 수신합니다.
- base-model에 학습된 가중치를 적용합니다.
- model의 output-layer를 data에 맞게 수정합니다.

#### requirements.txt
``` pip install -r requirements.txt ```
- 모델 동작을 위한 package 목록입니다.
  
#### data
- 예측 수행 테스트를 위한 이미지 파일
- 해당 디렉터리 하위에 원하는 데이터를 삽입하여 예측을 테스트할 수 있습니다.
  - ```--input {file_name}```

### args
ArgumentParser를 사용해 원하는 모델과 데이터를 명시할 수 있습니다.
```bash
--help
```
>모델에 대한 기본 정보, 사용한 가능한 모델 목록, 전달 가능한 인자를 출력합니다.
<br>

```bash
--model_type
```
>모델의 종류를 지정합니다.
>- resnet
>- efficientnet
>- mobilenet

<br>

```bash
--model_name
```
>정확한 모델명을 지정합니다. ( --help 에서 출력되는 model-list 참조 )

<br>

```bash
--input
```
>Inferencing을 수행할 데이터를 지정합니다.

<br>
