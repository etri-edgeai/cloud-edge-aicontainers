# grpc file transfer

- original code from https://github.com/gooooloo/grpc-file-transfer
- modified by J. Park @ KETI



## 사전 작업

mkdir grpc_example
cd grpc_example
pip istall virtualenv
virtualenv -p python3 env
source env/bin/activate
pip install grpcio grpcio-tools


python -m grpc_tools.protoc --proto_path=. ./unary.proto --python_out=. --grpc_python_out=.

python3 -m grpc_tools.protoc --proto_path=.  ./bidirectional.proto --python_out=. --grpc_python_out=. 





About
=====
Handy tool for large file transfering using gRPC.

Demo
=====

Server side:

```
python3 src/demo_server.py
```

Client side:

```
python3 src/demo_client.py
```
