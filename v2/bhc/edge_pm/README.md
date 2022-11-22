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

## 
