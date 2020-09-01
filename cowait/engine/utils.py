import json
import gzip
from base64 import b64encode, b64decode


def env_pack(value):
    value = json.dumps(value).encode('utf-8')
    value = gzip.compress(value)
    return b64encode(value).decode('utf-8')


def env_unpack(value):
    value = b64decode(value)
    value = gzip.decompress(value)
    return json.loads(value)
