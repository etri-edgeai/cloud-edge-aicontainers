from clip_client import Client

c = Client('grpc://0.0.0.0:51000')

c.encode(
    [
        'she smiled, with pain',
        'hismiled, with pain',
    ]
)
print(c)
