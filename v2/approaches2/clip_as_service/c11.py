from clip_client import Client

c = Client('grpc://0.0.0.0:51009')
print(c.profile())
