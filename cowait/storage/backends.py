import fsspec


class StorageBackends(object):
    cache = {}

    def __init__(self, backends: dict = {}):
        self.backends = {}
        if not isinstance(backends, dict):
            raise TypeError('backends must be a dict')
        for name, store in backends.items():
            self.add(name, **store)

    def add(self, name: str, protocol: str, **storage) -> None:
        fs = fsspec.filesystem(protocol, **storage)
        self.backends[name] = fs

    def get(self, attr) -> fsspec.AbstractFileSystem:
        return self.backends.get(attr)

    def __getattr__(self, attr) -> fsspec.AbstractFileSystem:
        return self.backends.get(attr)

    def __getitem__(self, attr) -> fsspec.AbstractFileSystem:
        return self.backends.get(attr)

    def open(self, path: str, **kwargs):
        if len(self.backends) > 1:
            raise RuntimeError('Cant use open() shorthand with multiple backends')
        if len(self.backends) == 0:
            raise RuntimeError('No storage backend defined')
        fs = next(iter(self.backends.values()))
        return fs.open(path, **kwargs)

    @staticmethod
    def from_json(json):
        if json in StorageBackends.cache:
            return StorageBackends.cache[json]

        fs = fsspec.AbstractFileSystem.from_json(json)
        StorageBackends.cache[json] = fs
        return fs
