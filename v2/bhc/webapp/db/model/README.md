# 모델 배포, 추론 수행 및 시각화
사용하고자 하는 모델을 목표한 노드에 배포합니다.<br>
삽입된 데이터에 대한 추론을 수행합니다.<br>
모든 과정을 원격으로 수행합니다.<br>
과정 중 필요한 데이터에 대한 로깅을 수행합니다<br>
모든 과정에 대한 시각화를 수행합니다.<br>

## get_model.py

```bash
python get_model.py \
--playbook \
--hosts_file \
--registry \
--host \
--tag
```
노드에 모델을 배포하기 위한 코드입니다.<br>

### ```get_model_info(registry, conn):```
레지스트리 서버에 등록된 모델의 목록을 불러옵니다.<br>

### ```get_desc(host, tag, conn):```
배포하고자 한 모델의 description 정보를 불러옵니다.<br>

### ```model_download(playbook, hosts_file, registry, hosts, tag):```
선택한 모델 이미지를 다운로드하고 컨테이너를 생성합니다.<br>


## run_model.py

```bash
mv test.jpg /var/www/html/tmp/test.jpg

python run_model.py
```

모델 컨테이너 내부에 데이터를 복사하고 추론을 수행합니다.<br>

### ```input_to_db(host, path, conn):```
서버에 저장된 이미지 정보를 불러와 db에 저장합니다.<br>
신규 저장된 이미지에 대한 정보만 저장합니다.<br>

### ```get_input(playbook, hosts_file, input, host):```
서버에 저장된 데이터를 대상 노드의 모델 컨테이너 내부에 복사, 저장합니다.<br>
(playbook ```run_model.yaml``` 참고)<br>

### ```get_pred(playbook, hosts_file, host, input, conn):```
모델을 실행하여 데이터에 대한 추론 정보를 출력합니다.<br>
추론 결과를 db에 저장합니다.<br>

## run_model.yaml
원격 명령 수행을 위한 ansible-playbook입니다.<br>
tags 인자로 태스크를 구분합니다.

### tags: distsrb
모델 배포를 위한 명령을 수행합니다.<br>
* docker pull : 이미지 다운로드
* docker run : 컨테이너 생성

### tags: search
배포 결과 관측을 위한 명령입니다.<br>
* docker images : 로컬 내 이미지 목록
* docker ps -a : 생성된 컨테이너 목록

### tags: input
인풋으로 사용할 데이터를 운반하기 위한 명령입니다.<br>
* ansible copy module : 서버 -> 노드
* docker cp : 노드 -> 모델

### tags: pred
모델을 실행시키기 위한 명령입니다.<br>
* docker exec : 컨테이너 내부 환경에 명령어를 전달
