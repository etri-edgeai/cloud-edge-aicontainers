
# ref : https://novemberde.github.io/post/2017/04/09/Docker_Registry_0/


# push to private registry
docker tag nginx:evc-nginx localhost:5000/evc-nginx
docker push localhost:5000/evc-nginx

# check
curl -X GET http://localhost:5000/v2/_catalog
curl -X GET http://localhost:5000/v2/evc-nginx/tags/list
