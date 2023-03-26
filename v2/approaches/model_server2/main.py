import os
import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import aiofiles  # 추가해야 함
from typing import List

app = FastAPI()

UPLOAD_FOLDER = "./upload_folder"
MODEL_FOLDER = "./model_folder"

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(await file.read())
    return {"file_path": file_path}

@app.get("/download/{model_name}")
async def download_file(model_name: str):
    file_path = os.path.join(MODEL_FOLDER, model_name)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return {"error": "File not found."}

@app.delete("/delete/{model_name}")
async def delete_file(model_name: str):
    file_path = os.path.join(MODEL_FOLDER, model_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": "File deleted successfully."}
    else:
        return {"error": "File not found."}

@app.put("/update/{model_name}")
async def update_file(model_name: str, file: UploadFile = File(...)):
    file_path = os.path.join(MODEL_FOLDER, model_name)
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(await file.read())
    return {"file_path": file_path}

@app.get("/list")
async def list_files():
    return {"models": os.listdir(MODEL_FOLDER)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)