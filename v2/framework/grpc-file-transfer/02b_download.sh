# 서버에 존재하는 <from_id 폴더>에 있는 특정 파일을 다운로드 합니다.

ID=0
PORT=8081
ADDR=localhost

python3 -m client.main -i ${ADDR} -p ${PORT} --from_id ${ID} download -d client/dataset -f vgg16.onnx

python3 -m client.main -i ${ADDR} -p ${PORT} --from_id ${ID} download -d client/dataset -f resnet50.onnx

python3 -m client.main -i ${ADDR} -p ${PORT} --from_id ${ID} download -d client/dataset -f na.txt

python3 -m client.main -i ${ADDR} -p ${PORT} --from_id ${ID} download -d client/dataset -f cal2022.txt


# 없는 폴더

ID=100
PORT=8081
ADDR=localhost

python3 -m client.main -i ${ADDR} -p ${PORT} --from_id ${ID} download -d client/dataset -f vgg16.onnx

python3 -m client.main -i ${ADDR} -p ${PORT} --from_id ${ID} download -d client/dataset -f resnet50.onnx

