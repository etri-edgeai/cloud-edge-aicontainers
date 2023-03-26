import requests

# 파일 업로드
response = requests.post("http://localhost:8000/uploadfile/", files={"file": open("sample.pt", "rb")})
print(response.json())  # {"filename": "sample.pt"}

# 파일 다운로드
response = requests.get("http://localhost:8000/download/sample.pt")
with open("sample_downloaded.pt", "wb") as file:
    file.write(response.content)