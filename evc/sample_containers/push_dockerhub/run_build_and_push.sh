# Docker Buildx 플러그인을 활성화합니다.
docker buildx create --use

# 사용할 수 있는 빌더 목록을 확인합니다.
docker buildx ls

# 다음 명령어를 사용하여 멀티 아키텍처 이미지를 빌드하고 
# Docker Hub와 같은 레지스트리에 푸시합니다. 
# 여기서는 myusername/myapp 이미지의 예시이며, 각자 환경에 맞게 수정해야 합니다.
# 또한 Docker Hub에 로그인한 상태여야 합니다.
docker buildx build --platform linux/amd64,linux/arm64 -t myrepo/myapp:latest --push .
