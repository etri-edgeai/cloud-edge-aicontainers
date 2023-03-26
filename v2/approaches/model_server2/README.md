# 모델 업로드 및 다운로드 

코드에서는 FastAPI를 사용하여 간단한 웹서버를 구현하였습니다. 이 서버를 통해 사용자는 모델을 업로드, 다운로드, 삭제할 수 있으며, 업로드된 파일 리스트도 확인할 수 있습니다.

서버에서는 models라는 폴더를 만들어서 업로드된 모델들을 저장하도록 했습니다. POST 요청을 받으면 request 객체에서 파일을 읽어서 models 폴더에 저장하며, GET 요청을 받으면 models 폴더에서 파일을 읽어서 클라이언트에게 보내주도록 했습니다. 삭제 요청은 os 모듈을 사용해서 파일을 삭제하도록 했습니다.

- API 목록은 다음과 같습니다.
- 5개의 API를 구현하고 있습니다.

- 모델 업로드: /upload
- 모델 다운로드: /download/{model_name}
- 모델 삭제: /delete/{model_name}
- 모델 업데이트: /update/{model_name}
- 업로드된 파일 리스트 확인: /list


!pip install fastapi
!pip install uvicorn
!pip install aiofiles


