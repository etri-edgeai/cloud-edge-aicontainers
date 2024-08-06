docker buildx create --use
docker buildx ls
docker buildx build --platform linux/arm64 -f Dockerfile4Arm -t ketirepo/beacon4arm:latest --push .

