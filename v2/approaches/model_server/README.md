# 모델 업로드 및 다운로드 

## 서버 코드

```python
from fastapi import FastAPI, File, UploadFile
from starlette.responses import StreamingResponse

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

@app.get("/download/{file_path:path}")
async def download_file(file_path: str):
    def iter_file():
        with open(file_path, mode="rb") as file:
            yield from file
    return StreamingResponse(iter_file(), media_type='application/octet-stream')

```

- 위 코드에서 create_upload_file 함수는 파일을 업로드하는 엔드포인트입니다. 클라이언트는 POST 요청으로 파일을 전송할 수 있으며, 서버는 파일 객체(UploadFile)를 인자로 받아서 처리합니다.

- download_file 함수는 파일을 다운로드하는 엔드포인트입니다. GET 요청으로 파일 경로를 전달하면, 해당 파일을 바이트 스트림으로 반환합니다. 이를 StreamingResponse로 감싸서 전송하게 됩니다.

- 위 코드를 실행하면, FastAPI 서버가 localhost:8000에서 실행됩니다. 파일을 업로드할 때는 /uploadfile/ 엔드포인트로 POST 요청을 보내면 되고, 다운로드할 때는 /download/<file_path> 엔드포인트로 GET 요청을 보내면 됩니다. 


## 클라이언트 코드

- 예를 들어, sample.pt 파일을 업로드하고 다운로드하려면 다음과 같이 실행하면 됩니다.

```python
import requests

# 파일 업로드
response = requests.post("http://localhost:8000/uploadfile/", files={"file": open("sample.pt", "rb")})
print(response.json())  # {"filename": "sample.pt"}

# 파일 다운로드
response = requests.get("http://localhost:8000/download/sample.pt")
with open("sample_downloaded.pt", "wb") as file:
    file.write(response.content)

```



## 서버 실행

- fastapi로 만든 서버 코드인 server.py를 실행하는 콘솔 명령어는 다음과 같습니다.

```bash
uvicorn server:app --reload
```

- 위 명령어에서 server는 server.py 파일 이름입니다. --reload 옵션은 코드 변경이 감지되면 자동으로 서버를 재시작합니다. app은 fastapi 애플리케이션 객체의 이름을 나타내며, server.py 파일 내부에서 app 객체를 생성했다고 가정합니다.

- Uvicorn은 Python ASGI 웹 서버의 구현체 중 하나입니다. ASGI(Asynchronous Server Gateway Interface)는 비동기 웹 프레임워크의 기본 인터페이스로, 비동기적인 웹 어플리케이션 개발을 지원합니다. Uvicorn은 Python 3.6 이상에서 동작하며, 웹 애플리케이션 개발에 사용되는 프레임워크인 FastAPI와 함께 자주 사용됩니다.

- FastAPI는 비동기 I/O를 기반으로 하는 고성능 웹 프레임워크로, Flask보다 빠른 속도와 대용량 처리 능력을 가지고 있습니다. 또한, 자동으로 API 문서를 생성해주는 기능도 있어 개발 효율성을 높일 수 있습니다.
