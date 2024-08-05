# 이미지 빌드
docker build -t helloworld_single-python-app .

# 이미지 확인
docker images | grep helloworld_single-python-app

# 컨테이너 실행
docker run --rm helloworld_single-python-app
