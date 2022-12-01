# 그래픽 사용자 인터페이스 개발
**사용자 인터페이스를 통한 조회, 배포 등 조작, 정보 및 결과 조회**<br>

### 조회 정보 | 수행 명령
> 실제 코드와 커맨드는 달라질 수 있습니다.<br>
- registry list
  - curl
- model existance verification
  - curl | grep
  - return boolean
- model build | distribution
  - if True : pull
  - if False : build && push && pull
- test model prediction
  - run
  - pred()

## PyQt5
GUI programming을 지원하는 python 라이브러리입니다.<br>

### VcXsrv
Linux 환경의 경우(WSL 포함) GUI Display를 기본적으로 연결해주지 않기 때문에 GUI를 지원하는 가상 서버 어플리케이션을 설치합니다.<br>
<br>
> **install VcXsrv**<br>
> https://sourceforge.net/projects/vcxsrv/

installation 수행 후
```bash
$ export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0

## VcXsrv 재실행 ( window 환경에서 ) ( 실행 시 additional parameter "-ac" 확인 )

## wsl 재실행 ( powershell에서 )
$ wsl --list --verbose
$ wsl --shutdown Ubuntu-20.04

## test VcXsrv
$ xeyes
```

### Qt Designer
**PyQt GUI 레이아웃 편집기**<br>
.ui 포맷(XML 문서)으로 저장하여 불러와 사용하거나 .py 포맷으로 변환하여 사용할 수 있습니다.<br>
```bash
## python 파일로 변환
python -m PyQt5.uic.pyuic -x test.ui -o test.py
```

## test
PyQt5의 클래스 구조와 기능 구현에 필요한 내용 이해를 위해 테스트중인 코드입니다.<br>
> 지속 테스트 작업 중에 있습니다.

## main.py
demonstration application의 메인 화면으로 사용될 예정인 GUI 레이아웃입니다.<br>
> 지속 고도화 작업 중에 있으며 레이아웃 및 화면 구성은 변경될 수 있습니다.

