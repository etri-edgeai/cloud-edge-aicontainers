# gRPC


- https://www.velotio.com/engineering-blog/grpc-implementation-using-python


```bash

mkdir grpc_example
cd grpc_example
pip istall virtualenv
virtualenv -p python3 env
source env/bin/activate
pip install grpcio grpcio-tools


python -m grpc_tools.protoc --proto_path=. ./unary.proto --python_out=. --grpc_python_out=.

python3 -m grpc_tools.protoc --proto_path=.  ./bidirectional.proto --python_out=. --grpc_python_out=. 


```