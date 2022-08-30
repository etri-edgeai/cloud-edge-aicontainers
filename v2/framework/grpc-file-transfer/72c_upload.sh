cal 1 2022 > client/dataset/cal2022jan.txt 
python3 -m client.main -i localhost -p 5000 -c cert/server.crt upload -f client/dataset/cal2022jan.txt
python3 -m client.main -i localhost -p 5000 -c cert/server.crt upload -f client/dataset/vgg16.onnx
