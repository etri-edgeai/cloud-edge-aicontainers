# 모델 업로드 및 다운로드 

- FastAPI를 사용하여 간단한 웹서버를 구현합니다.
- 이 서버를 통해 사용자는 모델을 업로드, 다운로드, 삭제할 수 있으며, 업로드된 파일 리스트도 확인할 수 있습니다.

## API 목록
- 5개의 API를 구현하고 있습니다.

- 모델 업로드: /upload
- 모델 다운로드: /download/{model_name}
- 모델 삭제: /delete/{model_name}
- 모델 업데이트: /update/{model_name}
- 업로드된 파일 리스트 확인: /list

## 사전 설치 패키지

!pip install fastapi
!pip install uvicorn
!pip install aiofiles

