# 실험 환경 네트워크 구성
시나리오 상 추론을 위한 각 노드와 제어용 서버 노드는 다른 네트워크에서 동작할 확률이 높습니다.<br>
시나리오에 맞게 환경을 구성하기 위한 방법, 요소들을 정리합니다.<br>

## 레지스트리 서버 외부 통신
구축된 도커 레지스트리 서버 컨테이너는 외부 네트워크를 통해 원격지의 노드에 모델 이미지를 배포할 수 있어야 합니다.<br>
도커 컨테이너의 원격지 통신을 활성화하는 방법은 두 가지가 있습니다.

### Insecure Registry
Client 내부에 insecure-registry config file을 저장할 경우 대상 네트워크에 접근할 수 있습니다.

#### daemon.json 작성
```plain text
{
  "insecure-registries" : ["123.214.186.252:39500"]
}
```
#### 파일 저장
``` /etc/docker/ ``` 내부에 저장합니다.

#### 도커엔진 재시작
```bash
sudo systemctl restart docker
```

> 단점 : curl 등 다른 기능을 사용할 수 없으며, http 프로토콜을 사용하기 때문에 보안성이 떨어집니다.

### HTTPS 프토로콜 사용
SSL 인증서를 사용하여 https 프로토콜로 통신할 경우 외부에서 접속할 수 있습니다.<br>
자체적으로 CA 인증서를 생성하고 대상 노드에만 인증서를 전송하여 보안성을 확립한 상태에서 통신을 확립합니다.

#### CA 키, 인증서 생성
```bash
mkdir certs && cd certs
openssl genrsa -out rootca.key 2048
openssl req -x509 -new -nodes -key rootca.key -days 365 -out rootca.crt

## 입력창은 작성하지 않습니다.
```

#### extfile 생성
```bash
echo subjectAltName = IP:123.214.186.252,IP:127.0.0.1 > extfile.cnf
```

#### registry 키, 사설 인증서 생성
```bash
openssl genrsa -out registry.key 2048
openssl req -new -key registry.key -out registry.csr

## 입력창이 여러 차례 팝업합니다. 작성하지 않습니다.
## Common Name 만 입력 : IP 주소 (123.214.186.252)

openssl x509 -req -in registry.csr -CA rootca.crt -CAkey rootca.key -CAcreateseiral -out registry.crt -days 365 -extfile extfile.cnf
```

#### registry 인증서 등록 및 docker 재실행
```bash
cp registry.crt /usr/local/share/ca-certifica tes/registry.crt
update-ca-certificates

systemctl restart docker
```
#### certs 디렉터리가 마운트된 레지스트리 컨테이너 생성
```bash
sh registry_init.sh
```

#### docker test
```bash
docekr push 123.214.186.252:39500/aarch64-model:imagenet

curl 123.214.186.252:39500/v2/_catalog
# 에러 출력 시 option -k 추가
```

#### Client set
client에 인증서를 전송하기 위한 playbook 작성
```yaml
- name: copy CA files & keys
  hosts: rpi6404
  
  tasks:
  
    - name: copy CA dir
      copy:
        src: "certs"
        dest: "/home/keti"
```

#### client에 인증서 적용
```bash
ansible-playbook copy.yaml -i {hostsfile_path}
cp registry.crt /usr/local/share/ca-certificates/registry.crt
update-ca-certificates
systemctl restart docker

# curl test
curl https://123.214.186.252:39500/v2/_catalog

# pull image
docker pull 123.214.186.252:39500/aarch64-model:imagenet
```
