#!/bin/bash

docker tag joxit/docker-registry-ui:static localhost:3002/joxit/docker-registry-ui:static
docker tag joxit/docker-registry-ui:static localhost:3002/joxit/docker-registry-ui:0.3
docker tag joxit/docker-registry-ui:static localhost:3002/joxit/docker-registry-ui:0.3.0
docker tag joxit/docker-registry-ui:static localhost:3002/joxit/docker-registry-ui:0.3.0-static
docker tag joxit/docker-registry-ui:static localhost:3002/joxit/docker-registry-ui:0.3-static

docker push localhost:3001/joxit/docker-registry-ui

docker tag registry:2.7 localhost:3001/registry:latest
docker tag registry:2.6.2 localhost:3001/registry:2.6.2
docker tag registry:2.6.2 localhost:3001/registry:2.6
docker tag registry:2.6.2 localhost:3001/registry:2.6.0
docker tag registry:2.6.2 localhost:3001/registry:2

docker push localhost:3001/registry