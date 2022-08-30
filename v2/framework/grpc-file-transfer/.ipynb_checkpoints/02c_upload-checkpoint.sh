# 1번이 자신의 폴더 1번으로
FROM_ID=1
TO_ID=1
PORT=8081
ADDR=localhost


# 나는 1번, 0번에 있는 모델을 먼저 다운로드 함
python3 -m client.main -i ${ADDR} -p ${PORT} --from_id 0 download -d client/dataset -f vgg16.onnx

# 업로드
python3 -m client.main -i ${ADDR} -p ${PORT} --from_id ${FROM_ID} --to_id ${TO_ID} upload -f client/dataset/vgg16.onnx

# 파일을 새로 생성
cal 1 2022 > client/dataset/cal2022jan.txt 

# 업로드
python3 -m client.main -i ${ADDR} -p ${PORT} --from_id ${FROM_ID} --to_id ${TO_ID} upload -f client/dataset/cal2022jan.txt


# 1번이 마스터 폴더 0번으로 업로드
FROM_ID=1
TO_ID=0
PORT=8081
ADDR=localhost

cal 1 2022 > client/dataset/cal2022jan.txt 
python3 -m client.main -i ${ADDR} -p ${PORT} --from_id ${FROM_ID} --to_id ${TO_ID} upload -f client/dataset/cal2022jan.txt


# 1번이 2번으로 업로드
FROM_ID=1
TO_ID=2
PORT=8081
ADDR=localhost

cal 1 2022 > client/dataset/cal2022jan.txt 
python3 -m client.main -i ${ADDR} -p ${PORT} --from_id ${FROM_ID} --to_id ${TO_ID} upload -f client/dataset/cal2022jan.txt


