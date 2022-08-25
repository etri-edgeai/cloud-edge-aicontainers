from clip_client import Client

c = Client('grpc://0.0.0.0:51000')
r = c.encode(['First do it', 'then do it right', 'then do it better'])

print(r.shape)  # [3, 512]
