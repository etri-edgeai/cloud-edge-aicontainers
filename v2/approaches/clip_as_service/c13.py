from clip_client import Client
from docarray import Document

c = Client('grpc://0.0.0.0:51000')

da = [
    Document(text='she smiled, with pain'),
    Document(uri='apple.png'),
    Document(uri='apple.png').load_uri_to_image_tensor(),
    Document(blob=open('apple.png', 'rb').read()),
    Document(uri='https://clip-as-service.jina.ai/_static/favicon.png'),
    Document(
        uri='data:image/gif;base64,R0lGODlhEAAQAMQAAORHHOVSKudfOulrSOp3WOyDZu6QdvCchPGolfO0o/XBs/fNwfjZ0frl3/zy7////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAkAABAALAAAAAAQABAAAAVVICSOZGlCQAosJ6mu7fiyZeKqNKToQGDsM8hBADgUXoGAiqhSvp5QAnQKGIgUhwFUYLCVDFCrKUE1lBavAViFIDlTImbKC5Gm2hB0SlBCBMQiB0UjIQA7'
    ),
]

r = c.encode(da)
print(r)
