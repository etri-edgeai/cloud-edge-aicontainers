## pull image and run model container
## 2021. 11. 02 Ethicsense

echo "automatic inference-model activation start"
echo.
echo.

## pulling image
echo "getting model from server,,,"
echo.
echo.
docker image pull localhost:5000/edge-model:1.1

## build new model container
echo "building model,,,"
echo.
echo.
docker run -d --name edge-model -it localhost:5000/edge-model:1.1

## get prediction
echo "starting prediction,,,"
echo.
echo.
docker exec edge-model python home/classifier.py
echo.