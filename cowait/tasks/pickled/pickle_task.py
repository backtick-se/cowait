import dill
from base64 import b64encode, b64decode


def pickle_task(task):
    serialized = dill.dumps(task)
    return str(b64encode(serialized), encoding='utf-8')


def unpickle_task(task):
    funcbytes = b64decode(task)
    return dill.loads(funcbytes)
