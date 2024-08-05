docker buildx create --use
docker buildx ls
docker buildx build --platform linux/amd64,linux/arm64 -t myusername/myapp:latest --push .
