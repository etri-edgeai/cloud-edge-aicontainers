# Docker를 활용한 AI Model 구현과 배포
**AI model dockerizing &amp; distribution**

- 참고자료
  - 1. https://ethicsense.notion.site/Inference-model-generation-f7983c1c539b469ca3128caef6c48eb6<br>
  - 2. https://www.notion.so/ethicsense/Automatic-distribution-run-f04da7cdfece46f39b11287bdec96e06<br>

해당 자료는 작업, 실험 서사 및 내용을 직접 기록한 문서입니다.

## 1. MODEL
**예측 모델 제작**<br>
<br>
>Pytorch python code를 사용하여 구현된 inference testing model 입니다.<br>
이미지 계열 Pre-trained Model을 다수 활용하였으며 ArgParse를 통해 조작합니다.<br>
<br>
상세 내용을 ./model 내부에 기재합니다.

## 2. Dockerizing
**모델 코드를 포함한 환경 구성 전체를 도커 이미지화 한 과정입니다.**<br>
<br>
>도커 허브의 파이썬 베이스 이미지를 컨테이너로 빌드한 후 모델 코드 삽입 및 환경 구성, 컨테이너를 커밋하여 모든 세팅을 포함한 이미지를 추출하는 과정으로 진행하였습니다.<br>
<br>
상세 내용을 ./dockerizing 내부에 기재합니다.

## 3. Registry ( feat. Distribution )
**Docker registry를 활용해 image를 노드에 배포하는 방법에 대하여**<br>
<br>
>도커 허브의 레지스트리 베이스 이미지를 컨테이너로 빌드, 레지스트리의 기본적인 조작과 정보 조회, 이미지 push || pull, 목적 노드에 다운로드 후 이미지의 정상 빌드 확인 등 실험 및 검증을 수행했습니다.<br>
<br>
상세 내용을 ./registry 내부에 기재합니다.

## 4. Rebuilding-RPI-Image
**다중 아키텍처 가용 이미지에 관하여**<br>
<br>
>노드의 CPU architecture와 이미지에 명시된 architecture가 다를 경우 해당 이미지가 정상 작동하지 않는 문제를 해결하는 과정입니다.<br>
멀티 스테이지 빌드 테스트, 아키텍쳐 별 이미지를 별도 제작하여 각기 배포, 차후 멀티 스테이지 빌드를 위한 Dockerfile 제작에 대한 고찰 내용을 포함합니다.<br>
<br>
상세 내용을 ./rebuilding_rpi_image 내부에 기재합니다.

## 5. Automation
**모델 이미지 배포, 빌드, 코드 수행 자동화**<br>
<br>
>가상 환경 이미지를 레지스트리로부터 받고, 컨테이너를 빌드하여 작업 명령을 수행하는 과정을 자동화하기 위한 기술, 방법론을 강구합니다.<br>
Ansible을 통한 네트워크 구성, 각 노드를 제어하는 제어 노드 구축, 맞춤형 스크립트 출력 및 시스템의 시각화를 위한 Front 구현 등이 추가될 수 있습니다.<br>
<br>
상세 내용을 ./automation 내부에 기재합니다.
