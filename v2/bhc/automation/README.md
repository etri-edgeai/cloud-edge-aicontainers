# 모델 자동화 및 사용자화
각 노드가 모델을 구축하고 명령을 수행하는 과정을 간소화, 자동화합니다.<br>
그 외 작업의 편의성을 확보하기 위한 모든 기술과 방법론을 포함합니다.

## 1. shell script
```$ sh run-model.sh```<br>
레지스트리 서버로부터 이미지를 다운로드 받고 컨테이너를 빌드하고 모델 코드를 실행하는 과정을 작성한 스크립트입니다.<br>

  **※ 정상 작동을 위해 모델 코드의 path 단을 수정해야 합니다.**
  ```python
    ## load_model.py
    weights_dir = './home/best_model'
    
    ## classifier.py
    data_path = './home/data/'
  ```
### 수행 절차
- 레지스트리 서버로부터 이미지 풀(pull)
  - ```$ docker image pull```
- 다운로드한 이미지로 컨테이너 생성
  - ```$ docker run```
- 컨테이너의 커널을 통한 작업 명령 수행
  - ```$ docker exec```
### 정상 작동 확인 11/02
로컬 환경에서 실험되었습니다.<br>
![capture](./capture/run.png)
