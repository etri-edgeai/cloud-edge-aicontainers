# .yaml 구성 파일을 활용한 EVC 조작
사용자가 자신의 목적에 맞게 직접 configuration file을 작성하고 요구사항에 맞게 EVC에 전달합니다.<br>
EVC는 정의된 내용에 맞게 작업을 수행합니다.<br>
<br>
사용자가 불필요하게 인터페이스에 접근하거나 사용 방법을 숙지하고 소스 코드를 수정할 필요가 없습니다.<br>
타 시스템에 이식하거나 독자적인 시스템으로 개발하고자 하는 사용자가 구조를 파악하기 용이합니다.<br>


## YOLOv8 CarPlate-Detector
> **from ultralytics**

config file을 통한 EVC 실행에서 편의성이 가장 두드러지는 지점은 모델 구축, 배포 절차입니다.<br>
해당 관점에서 구현을 테스트하기 위한 테스트용 AI model입니다.<br>
yolov8s 모델을 추가 학습한 차량 번호판 추적기 모델입니다.<br>
<br>

모델 실행용 소스코드,<br>
기학습 가중치를 포함한 모델 파일,<br>
이미지 구축을 위한 Dockerfile 스크립트,<br>
모델 작동 테스트를 위한 인풋 이미지로 구성되어 있습니다.<br>
<br>
### AI model constitution
> * model.py
> * pd_base.pt
> * Dockerfile
> * data/test.jpg

## ActivationConfig.yaml
> **```test.yaml```**

EVC 실행을 위해 필요한 정보를 정의할 수 있는 구성 파일입니다.<br>
yaml 데이터의 구조체는 dictionary와 list를 함께 사용하는 형태입니다.<br>
<br>
실행하고자 하는 작업, 실행할 위치, 필요한 각종 파일의 경로, 필요한 인자 등으로 구성됩니다.<br>

## Configuration Test
> **```config_test.py```**

동작과 실행 인자를 정의한 configuration.yaml file을 해석합니다.<br>
전달받은 데이터를 올바르게 파싱하고 EVC에 다시 전달합니다.<br>
구성을 유연하게 정의할 수 있도록 연결부와 EVC 실행부를 고도화합니다.<br>
다중 명령을 전달할 수 있도록 고도화합니다.<br>
<br>
구조체 파악 및 구동 절차 고도화를 위한 테스트 코드입니다.<br>


## RunEVC.py
> **```runEVC_cfg.py```**

구성 파일 내부의 데이터를 파싱합니다.<br>
해당 데이터와 EVC를 연결하고 정의된 작업 절차를 수행합니다.<br>
<br>
configy.yaml에서 정의된 key값을 토대로 데이터를 파싱합니다.<br>
인터페이스의 model_manager 모듈을 호출하여 데이터를 삽입해 명령을 전달하고 작업을 실행합니다.<br>



