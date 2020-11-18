import yaml


class SettingsDict(object):
    def __init__(self, *, path: str = None, data: dict = None, parent: 'SettingsDict' = None):
        if path is not None:
            if data is not None:
                raise ValueError('Pass either path or a data dict')
            self.read(path)
        else:
            self.data = {} if data is None else data

        self.parent = parent

    def __getitem__(self, key: str) -> any:
        return self.get(key, required=True)

    def __setitem__(self, key: str, value: any):
        self.set(key, value)

    def __delattr__(self, key: str):
        self.delete(key)

    def set(self, key: str, value: any) -> any:
        path = split_key(key)
        container = self.data
        for part in path[:-1]:
            if part not in container:
                container[part] = {}
            if not isinstance(container, dict):
                raise TypeError(f'{part} is not a dict')
            container = container[part]

        container[path[-1]] = value
        return value

    def override(self, key: str, value: any) -> any:
        if value is None:
            return self.get(key, None, False)
        return self.set(key, value)

    def has(self, key: str) -> bool:
        path = split_key(key)
        container = self.data
        for part in path[:-1]:
            if part not in container:
                if self.parent:
                    return self.parent.has(key)
                return False
            if not isinstance(container, dict):
                return False
            container = container[part]
        return path[-1] in container

    def get(self, key: str, default: any = None, required: bool = True) -> any:
        path = split_key(key)
        value = self.data
        for part in path:
            if not isinstance(value, dict) or part not in value:
                value = None
                break
            value = value.get(part, default)
        if value is None:
            if self.parent:
                return self.parent.get(key, default, required)
            if default is None and required:
                raise KeyError(f'{key} not set')
            return default
        return value

    def delete(self, key: str) -> None:
        # TODO: propagate delete to parents
        path = split_key(key)
        container = self.data
        for part in path[:-1]:
            if part not in container:
                container[part] = {}
            if not isinstance(container, dict):
                raise TypeError(f'{part} is not a dict')
            container = container[part]
        del container[path[-1]]

    def coalesce(self, key: str, value: any, default: any) -> any:
        if value is not None:
            return value
        return self.get(key, default, required=False)

    def write(self, path):
        with open(path, 'w') as f:
            yaml.dump(
                self.pack_data(self.data),
                stream=f,
                sort_keys=False,
                default_flow_style=False,
            )

    def read(self, path):
        with open(path, 'r') as f:
            self.data = self.unpack_data(yaml.load(f, Loader=yaml.FullLoader))

    def pack_data(self, data):
        return data

    def unpack_data(self, data):
        return data


def split_key(key):
    path = None
    if isinstance(key, str):
        path = key.split('.')
    elif isinstance(key, list):
        path = key
    else:
        raise TypeError("Expected key to be str or list")

    if len(path) < 1:
        raise ValueError(f'Invalid key {key}')

    return path
