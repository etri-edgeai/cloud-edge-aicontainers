from docarray import DocumentArray
from clip_client import Client

c = Client(server='grpc://0.0.0.0:51000')

da = DocumentArray.pull('ttl-original', show_progress=True, local_cache=True)
da = c.encode(da, show_progress=True)

vec = c.encode(["a happy potato"])
r = da.find(query=vec, limit=9)
r.plot_image_sprites()
