# docker run -d -p 5000:5000 --restart=always --name edge-registry \
# -v ./certs:/certs \
# -e REGISTRY_HTTP_ADDR=0.0.0.0:5000 \
# -e REGISTRY_HTTP_TLS_CERTIFICATE=./certs/registry.crt \
# -e REGISTRY_HTTP_TLS_KEY=./certs/registry.key \
# -e REGISTRY_STORAGE_DELETE_ENABLED=TRUE \
# registry:latest


docker run -v $(pwd)/conf/edge-registry.yml:/etc/docker/registry/config.yml:ro \
            -v $(pwd)/conf/auth.cert:/etc/docker/registry/auth.cert:ro \
            -p 30000:30000 --name edge-registry -d registry:latest