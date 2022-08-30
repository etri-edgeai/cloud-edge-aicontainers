# 서버에 존재하는 <from_id 폴더>의 파일을 보여줍니다.
# 연합학습을 고려하여 from_id = 0은  Global 모델 관리를 위한 Master Node로 사용 가능하고,
# 나머지 from_id = {1, 2, 3, ...} 은 에지 디바이스로 정할 수 있습니다.

python3 -m client.main -i localhost -p 8081 --from_id 0 list

python3 -m client.main -i localhost -p 8081 --from_id 1 list

python3 -m client.main -i localhost -p 8081 --from_id 2 list

python3 -m client.main -i localhost -p 8081 --from_id 3 list
