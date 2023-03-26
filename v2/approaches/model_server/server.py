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
