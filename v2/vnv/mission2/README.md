# (VnV) 경량 엣지 분석기반 추론 지연시간 개선율

## 문서의 개요
- 본 문서는 개발한 cloud-edge-framework 를 기반으로 VnV(Verification and Validation)를 수행하기 위한 절차 및 관련 코드를 설명합니다.

## 요약
- 이기종의 에지 디바이스 연동 플랫폼 성능을 검증하는 것을 목적으로 합니다.
- 연동 플랫폼의 성능은 추론 지연시간을 측정하여 정량적으로 평가합니다.


## 평가환경 구성

### HW 환경 구성

- 메인 서버 : {MacbookPro14}
- 에지 디바이스 : {RTX3080ti, RPI, TX2, NANO}

### SW 환경 구성

#### (1) 메인 서버와 에지 디바이스에 Ansible 설치

- 향후 이를 자동화 할 것이지만, 본 시험에서는 각각의 기기에 대해서 직접 설치합니다.

```bash
  # pip로 설치하는 방법입니다.
  $ pip install ansible
  
  # or 설치 할 앤서블 버전 설정
  $ pip install ansible==2.10.7

  # or conda로 설치 할 수 있습니다.
  $ conda install ansible

  # or ubuntu에서는 apt-get으로 설치할 수 있습니다.
  $ sudo apt install ansible

  # MacOS에는 brew로 설치할 수 있습니다.
  $ brew install ansible
```

#### (2) 메인 서버에서 에지 서버에 접속하기 위한 공개키를 생성하고 등록

- 메인 서버에서 에지 서버를 제어 및 모니터링 하려면 ssh 기술을 사용합니다.
- 그러나 매번 암호를 묻는 과정이 번거롭습니다.
- 암호 입력과정을 생략하기 위해 메인 서버에서는 RSA 방식으로 공개키(대칭암호화)를 생성합니다.
- 이를 각각의 에지 디바이스에 전송하여, ~/.ssh/authorized_keys 파일에 등록합니다.
- [주의] RSA 방식으로 키를 생성하면, 비밀키(개인키)와 공개키가 생성됩니다. 공개키는 말 그대로 공개가 가능하지만, 비밀키(개인키)는 절대 유출되지 않아야 합니다. 

##### 아래와 같은 절차에 따라 상기 과정을 수행할 수 있습니다.

- 단계 1. ssh-keygen으로 키를 생성하고,
- 단계 2. ssh-copy-id로 키를 추가합니다.

##### 예시

- 네트워크에 2대의 컴퓨터 {A, B}가 있다고 가정합니다.
- A 는 "192.168.1.5" IP를 갖는다고 하고,
- B 는 "192.168.1.3" IP를 갖는다고 가정합니다.
- B 의 사용자 id는 "user"이라고 가정합니다.
- A에서 ssh-keygen으로 먼저 키를 만듭니다.

```bash
$ ssh-keygen -t rsa
```

- private key(비밀키)와 public key(공개키)가 짝으로 만들어집니다.
- A에서 만든 공개키를 B로 전송합니다.
- A의 공개키 ~/.ssh/id_rsa.pub 의 내용이 B에 전달되어 B의 ~/.ssh/authorized_keys 파일에 추가됩니다.

```bash
$ ssh-copy-id user@192.168.1.3
```

- 이제 A는 B로 암호 입력 없이 접속 가능합니다.

```bash
$ ssh user@192.168.1.3
```



## 평가항목

### (1/1) 이기종 에지 디바이스 연동 플랫폼의 추론지연시간 절감율을 측정한다.

- todo




## 평가 절차

- step1 : todo

- step2 : todo

- step3 : todo



## 예상 평가 결과

### (1/1) 이기종 에지 디바이스 연동 플랫폼의 추론지연시간 절감율은 20%으로써, 목표치 20%를 상회한다.

- todo



### 주요 참고문헌

```bibtex
@article{mathur2021device,
  title={On-device federated learning with flower},
  author={Mathur, Akhil and Beutel, Daniel J and de Gusmao, Pedro Porto Buarque and Fernandez-Marques, Javier and Topal, Taner and Qiu, Xinchi and Parcollet, Titouan and Gao, Yan and Lane, Nicholas D},
  journal={arXiv preprint arXiv:2104.03042},
  year={2021}
}
```