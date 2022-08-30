# grpc-file-transfer

- by JPark @ KETI
- 원시 코드 : https://github.com/r-sitko/grpc-file-transfer
- 라이센스 : MIT
- 다운로드만 지원하는 것을 업로드도 지원하도록 수정했습니다.
- 보안 접속만 지원하는 것을 비보안 접속을 지원하도록 수정했습니다.
- 쉘 스크립트를 일부 추가했습니다.

## 준비

* Python3
* pip3
* OpenSSL


## 사용법

### 1. 준비사항

    - 프로젝트 파일을 클론합니다.
    
```bash
    git clone https://github.com/etri-edgeai/cloud-edge-aicontainers.git
    
    or
    
    보안 문제로 클론이 안되면 github에서 zip파일로 다운로드 합니다.
```

    - 작업할 폴더로 이동합니다.
    
```bash
    $ cd cloud-edge-aicontainers/v2/framework/grpc-file-transfer/
```


    - 작업 폴더에서 가상 환경을 만들고 의존성 패키지를 설치합니다.

```bash
    $ virtualenv env
    $ source env/bin/activate
    $ pip3 install -r requirements.txt
```

    -  *cert/generate.sh* 파일의 실행 권한을 설정 합니다
    
```bash
    $ chmod u+x cert/generate.sh
```

    - certificate 를 설정합니다.
        **Warning:** Don't use such created certificates for production environment.
        CN (Common Name) must match server name that you connect to with the client. In this example we will use *localhost*.
        
```bash
    $ cert/generate.sh /CN=localhost
    cert/generate.sh /CN=192.168.0.174
```


### 2. Quick Test

- KETI에서 생성한 원격지 컴퓨터에 서버 프로세스를 미리 동작시켰습니다.

- 상기, 작업폴더로 이동하고, 의존성 패키지를 설치해둔 가상환경을 수행합니다.
```bash
    $ cd cloud-edge-aicontainers/v2/framework/grpc-file-transfer/
    $ source env/bin/activate
```

- 0번째 폴더의 파일 목록을 확인합니다.
python3 -m client.main -i keticmr.iptime.org -p 22808 --from_id 0 list

- 0번째 폴더에서 resnet50.onnx 파일을 현재폴더에 다운로드 합니다.
python3 -m client.main -i keticmr.iptime.org -p 22808 --from_id 0 download -d ./ -f resnet50.onnx


- 10번째 폴더의 파일 목록을 확인합니다.
python3 -m client.main -i keticmr.iptime.org -p 22808 --from_id 10 list

- 현재폴더의 resnet50.onnx 파일을 10번째 원격지 폴더에 업로드 합니다.
python3 -m client.main -i keticmr.iptime.org -p 22808 --from_id 1 --to_id 10 upload -f ./resnet50.onnx

- 10번째 폴더의 파일 목록을 다시 확인합니다.
python3 -m client.main -i keticmr.iptime.org -p 22808 --from_id 10 list






### 3. 사용방법 (쉘 스크립트 실행, 비보안 접속)

    - 00_make_model.sh 을 실행하여 서버측에 기계학습 모델 파일을 생성합니다.
    
```bash
    $ 00_make_model.sh
```

    - 01_run_server.sh 을 실행하여 gRPC 서버를 구동합니다 (기계학습 파일을 클라이언트에게 보내고, 받습니다.) 
    
```bash
    $ 01_run_server.sh
```

    - 새로운 터미널 창을 띄우고 02a_show_filelist.sh 을 실행하여 gRPC 클라이언트에서 서버에 존재하는 파일 목록을 확인합니다.
    
```bash
    $ 02a_show_filelist.sh
```

    - 새로운 터미널 창에서 02b_download.sh 을 실행하여 서버에 존재하는 파일들을 다운로드 받습니다. 
      파라미터를 바꾸어 원하는 파일을 내려받을 수 있습니다.
    
```bash
    $ 02b_download.sh
```

    - 새로운 터미널 창에서 02c_upload.sh 을 실행하여 클라이언트에 존재하는 파일을 서버로 보냅니다.
    
```bash
    $ 02c_upload.sh
```




### 4. 사용방법 (파이썬 실행, 비보안 접속)

1. 첫번째 콘솔창을 띄우고 서버를 실행합니다.

```bash
    $ python3 -m server.main -i localhost -p 5000 -w 2 -d server/dataset -priv cert/server.key -cert cert/server.crt

```

2. 두번째 콘솔창을 띄우고 클라이언트를 여러 옵션을 주어 실행합니다.

    - list available files to download from server
        ```bash
        python3 -m client.main -i localhost -p 5000 -c cert/server.crt list
        ```
        
    - download *test_file.txt* file from server to *client/dataset* directory:
        ```bash
        python3 -m client.main -i localhost -p 5000 -c cert/server.crt download -d client/dataset -f test_file.txt
        ```

    - upload *test_file.txt* file from server to *client/dataset* directory:
        ```bash
        python3 -m client.main -i localhost -p 5000 -c cert/server.crt upload -f client/dataset/test_file.txt
        ```
        
        
        

### 5. 사용방법 (쉘 스크립트 사용, 보안접속)

    - 00_make_model.sh 을 실행하여 서버측에 기계학습 모델 파일을 생성합니다.
    
```bash
    $ 10_make_model.sh
```

    - 01_run_server.sh 을 실행하여 gRPC 서버를 구동합니다 (기계학습 파일을 클라이언트에게 보내고, 받습니다.) 
    
```bash
    $ 11_run_server.sh
```

    - 새로운 터미널 창을 띄우고 02a_show_filelist.sh 을 실행하여 gRPC 클라이언트에서 서버에 존재하는 파일 목록을 확인합니다.
    
```bash
    $ 12a_show_filelist.sh
```

    - 새로운 터미널 창에서 02b_download.sh 을 실행하여 서버에 존재하는 파일들을 다운로드 받습니다. 
      파라미터를 바꾸어 원하는 파일을 내려받을 수 있습니다.
    
```bash
    $ 12b_download.sh
```

    - 새로운 터미널 창에서 02c_upload.sh 을 실행하여 클라이언트에 존재하는 파일을 서버로 보냅니다.
    
```bash
    $ 12c_upload.sh
```


### 6. 사용방법 (파이썬 실행, 보안접속)

1. 첫번째 콘솔창을 띄우고 서버를 실행합니다.

```bash
    $ python3 -m server.main -i localhost -p 5000 -w 2 -d server/dataset -priv cert/server.key -cert cert/server.crt

```

2. 두번째 콘솔창을 띄우고 클라이언트를 여러 옵션을 주어 실행합니다.

    - list available files to download from server
        ```bash
        python3 -m client.main -i localhost -p 5000 -c cert/server.crt list
        ```
        
    - download *test_file.txt* file from server to *client/dataset* directory:
        ```bash
        python3 -m client.main -i localhost -p 5000 -c cert/server.crt download -d client/dataset -f test_file.txt
        ```

    - upload *test_file.txt* file from server to *client/dataset* directory:
        ```bash
        python3 -m client.main -i localhost -p 5000 -c cert/server.crt upload -f client/dataset/test_file.txt
        ```
        
        
        
        
        
        

## Description of client and server arguments

* server
```
usage: main.py [-h] -i IP_ADRESS -p PORT -w MAX_WORKERS -d FILES_DIRECTORY
               -priv PRIVATE_KEY_FILE -cert CERT_FILE

gRPC file transfer server

optional arguments:
  -h, --help            show this help message and exit
  -i IP_ADRESS, --ip_adress IP_ADRESS
                        IP address for server
  -p PORT, --port PORT  port address for server
  -w MAX_WORKERS, --max_workers MAX_WORKERS
                        maximum worker threads for server
  -d FILES_DIRECTORY, --files_directory FILES_DIRECTORY
                        directory containing files
  -priv PRIVATE_KEY_FILE, --private_key_file PRIVATE_KEY_FILE
                        private key file path
  -cert CERT_FILE, --cert_file CERT_FILE
                        certificate file path
```
* client
```
usage: main.py [-h] -i IP_ADRESS -p PORT -c CERT_FILE {download,list} ...

gRPC file transfer client

positional arguments:
  {download,upload,list}       client possible actions
    download            download file from server
    upload            upload file from server
    list                list files on server

optional arguments:
  -h, --help            show this help message and exit
  -i IP_ADRESS, --ip_adress IP_ADRESS
                        IP address of server
  -p PORT, --port PORT  port address of server
  -c CERT_FILE, --cert_file CERT_FILE
                        certificate file path

If you use download action you must provide below paramaters:
optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        where to save files
  -f FILE, --file FILE  file name to download
  
If you use upload action you must provide below paramaters:
optional arguments:
  -f FILE, --file FILE  file name to upload
```
