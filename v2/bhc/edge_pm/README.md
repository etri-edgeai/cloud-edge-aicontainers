# PM selection
원하는 태스크에 맞는 사전학습모델(pretrained-model)을 로드하여 바로 예측 수행에 사용할 수 있는 코드 작성

## Keras Applications
ImageNet dataset을 통해 학습된 가중치를 활용할 수 있는 다양한 vision 계열 모델을 저장한 라이브러리입니다.<br>
```https://keras.io/api/applications/```<br>

### ImageNet dataset
시각적 객체 인식이라는 대형 프로젝트의 일환으로 사용되는 데이터베이스입니다.<br>
본래 수만 개의 categories를 가지고 있으며 2010년 이후 매년 개최되는 ILSVRC(ImageNet Large Scale Visual Recognition Challenge)에서 최대한 겹치지 않는 1000개의 클래스 분류를 테스트하고 있습니다.<br>
keras.applications에서 학습된 가중치는 이 1000개 클래스에 해당하는 dataset을 통해 학습된 가중치입니다.<br>
```https://www.anishathalye.com/media/2017/07/25/imagenet.json``` 에서 전체 label 정보를 확인할 수 있습니다.

## test.ipynb
test code 작성 및 출력 확인을 위해 작성된 ipython 파일입니다.<br>
라이브러리 내 각 모델의 정상 작동여부 확인 및 파싱을 위한 코드를 테스트하였습니다.<br>
정상 작동되지 않는 모델에 대한 원인 분석 및 구조 변경 등을 테스트하였습니다.<br>
model list를 파싱하여 원하는 모델을 다운로드하는 과정을 테스트하였습니다.<br>
>일부 모델(convnext 계열 등)의 경우 layer 구조 변경 시 정상 로드되지 않습니다.<br>

## model.py
커맨드라인에서의 사용을 위해 정리된 코드입니다.<br>
```bash
python model.py
```
* model_type : 최초 원하는 모델의 이름을 정확히 입력하여야 합니다. <br>
  ```python
  model_type = str(input())
  ```
  ( 지원모델 참고 : https://keras.io/api/applications/ ) <br> ( 일부 모델이 정상 작동하지 않는 문제를 발견하였습니다. )
* img_path : 테스트하고자 하는 이미지의 경로입니다.<br>
  ```python
  img_path = './data/dog.jpeg'
  ```
* 불필요한 에러 내용 출력을 제거하였습니다.<br>
  ```python
  import warnings
  import os

  os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'

  import tensorflow as tf

  tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
  warnings.filterwarnings("ignore")
  ```
* 추론 수행 시 원본 이미지를 팝업시킵니다.<br>
  ```python
  import webbrowser
  webbrowser.open(path)
  ```
