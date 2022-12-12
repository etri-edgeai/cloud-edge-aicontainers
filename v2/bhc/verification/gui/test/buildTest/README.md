# 기능 통합, GUI 환경 구성
**GUI 어플리케이션에서의 distribution 기능 수행**<br>
<br>
구성된 배포 기능을 어플리케이션 내부에서 사용할 수 있도록 고도화하고 GUI와 기능을 연결합니다.<br>
수행 간 편의성을 확보합니다.<br>
수행 절차를 인터페이스로 확인할 수 있도록 레이아웃 구현 및 수정, 시각화를 진행합니다.<br>
>**최종적으로 모든 기능을 수행할 수 있는 데모 어플리케이션을 제작합니다.**<br><br>
>이 문서는 최종 목표에서 가장 핵심적인 기능인 <모델 구축 및 배포> 기능을 어플리케이션에 연결하는 과정입니다.

## 수행 기능
데모 어플리케이션이 제공하고자 하는 기능은 아래와 같습니다.
- 레지스트리가 현재 보유한 모델 목록 출력
- cpu architecture와 tag 정보를 통한 모델 검색
- 보유한 모델에 대한 pulling command 안내
- **미보유 모델에 대한 이미지 구축 및 배포 수행**
- 모델 구축 과정에서 test inferencing 수행 및 결과 출력

## test codes
**기능 구성 및 동작 테스트**
환명 구성, 시그널 연결 및 동작 내용을 테스트하기 위한 코드들입니다.<br>

### build.py
ansible-playbook script를 동작시킵니다.<br>
**동작 과정에서 필요한 인자값을 받아( ``` -e ``` ) 전달합니다.**<br>
```python
## example
# copy
os.system('ansible-playbook copy.yaml -e "Dockerfile_path={Dockerfile_path}
                                          zipModel_path={zipModel_path}"
                                          '.format(Dockerfile_path=Dockerfile_path, zipModel_path=zipModel_path)
                                          )

# build & dsitribution
os.system('ansible-playbook autorun.yaml -e "tag={tag} registry={reg_url}"'.format(tag=tag, reg_url=reg_url))
```

### upload.py
system 내에 있는 파일, 폴더를 선택할 수 있는 QFileDialog 기능을 사용합니다.<br>
파일을 경로를 리스트로 저장하여 필요에 따라 사용합니다.<br>
```python
fname = QFileDialog.getOpenFileNames(self)
        for f in fname[0]:
            if 'Dockerfile' in f:
                Dockerfile_path = f
            else:
                zipModel_path = f
        print(Dockerfile_path)
        print(zipModel_path)
```
<br>

**상기 코드에 선언된 변수가 스크립트 동작 시 인자값으로 활용됩니다.**<br>
각 변수는 어플리케이션을 통해 사용자가 선택, 입력할 수 있도록 구현합니다.
<br>

- copy.yaml
```yaml
  vars:
    Dockerfile_path: None
    zipModel_path: None
```

- autorun.yaml
```yaml
  vars:
    image_name: "{{ ansible_facts['architecture'] }}-model"
    registry: None
    tag: None
```
