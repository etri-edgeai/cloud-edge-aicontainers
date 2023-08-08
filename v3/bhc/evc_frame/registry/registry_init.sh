# docker run -d -p 5000:5000 --restart=always --name edge-registry \
# -v ./certs:/certs \
# -e REGISTRY_HTTP_ADDR=0.0.0.0:5000 \
# -e REGISTRY_HTTP_TLS_CERTIFICATE=./certs/registry.crt \
# -e REGISTRY_HTTP_TLS_KEY=./certs/registry.key \
# -e REGISTRY_STORAGE_DELETE_ENABLED=TRUE \
# registry:latest



## without CA
docker run -d -p 5000:5000 --restart=always --name evc-registry \
evc-registry:1.0