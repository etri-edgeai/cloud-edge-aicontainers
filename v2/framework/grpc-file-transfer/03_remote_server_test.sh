
# KETI에서 생성한 원격지 컴퓨터에 서버 프로세스를 동작시켰습니다.

# 0번째 폴더의 파일 목록을 확인합니다.
python3 -m client.main -i keticmr.iptime.org -p 22808 --from_id 0 list

# 0번째 폴더에서 resnet50.onnx 파일을 현재폴더에 다운로드 합니다.
python3 -m client.main -i keticmr.iptime.org -p 22808 --from_id 0 download -d ./ -f resnet50.onnx


# 10번째 폴더의 파일 목록을 확인합니다.
python3 -m client.main -i keticmr.iptime.org -p 22808 --from_id 10 list

# 현재폴더의 resnet50.onnx 파일을 10번째 원격지 폴더에 업로드 합니다.
python3 -m client.main -i keticmr.iptime.org -p 22808 --from_id 1 --to_id 10 upload -f ./resnet50.onnx

# 10번째 폴더의 파일 목록을 다시 확인합니다.
python3 -m client.main -i keticmr.iptime.org -p 22808 --from_id 10 list

