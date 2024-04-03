## hyper/registry-web creation
# docker run -it -p 8080:8080 --name registry-web --link edge-registry \
#            -e REGISTRY_URL=http://edge-registry:30000/v2 \
#            -e REGISTRY_TRUST_ANY_SSL=true \
#            -e REGISTRY_BASIC_AUTH="YWRtaW46Y2hhbmdlbWU=" \
#            -e REGISTRY_NAME=localhost:30000 hyper/docker-registry-web



## joxit/registry-ui config-file based creation
# docker run -v $(pwd)/conf/registry-web.yml:/conf/config.yml:ro \
#            -v $(pwd)/conf/auth.key:/conf/auth.key \
#            -v $(pwd)/db:/data \
#            -it -p 8080:8080 --link edge-registry --name registry-web \
#            hyper/docker-registry-web



## joxit/regsitry-ui easy creation
docker run -d -p 8879:80 --name registry-ui \
-e REGISTRY_URL=http://deepcase.mynetgear.com:20093 \
-e DELETE_IMAGES=true \
joxit/docker-registry-ui