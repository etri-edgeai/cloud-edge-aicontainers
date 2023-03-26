import os
from fastapi import FastAPI, File, UploadFile, HTTPException

app = FastAPI()

# 저장소 경로
MODEL_REPO_PATH = "./models/"

# 저장소 경로가 없다면 생성
if not os.path.exists(MODEL_REPO_PATH):
    os.makedirs(MODEL_REPO_PATH)

@app.post("/models/upload/")
async def upload_model(file: UploadFile = File(...)):
    """
    모델 업로드 엔드포인트
    """
    # 파일 저장
    file_path = os.path.join(MODEL_REPO_PATH, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    return {"filename": file.filename}

@app.get("/models/list/")
async def list_models():
    """
    업로드된 모델 리스트 반환
    """
    models = []
    for filename in os.listdir(MODEL_REPO_PATH):
        models.append(filename)
    return {"models": models}

@app.get("/models/download/")
async def download_model(filename: str):
    """
    모델 다운로드 엔드포인트
    """
    file_path = os.path.join(MODEL_REPO_PATH, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/octet-stream', filename=filename)
    else:
        raise HTTPException(status_code=404, detail="File not found")

@app.delete("/models/delete/")
async def delete_model(filename: str):
    """
    모델 삭제 엔드포인트
    """
    file_path = os.path.join(MODEL_REPO_PATH, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": "Model deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="File not found")
