import os.path
from cowait.engine import get_cluster_provider
from .const import CONTEXT_FILE_NAME
from .settings_dict import SettingsDict


def get_config_path():
    home = os.path.expanduser('~')
    return f'{home}/.{CONTEXT_FILE_NAME}'


class CowaitConfig(SettingsDict):
    def __init__(
        self, *,
        path: str = None,
        data: dict = None
    ):
        super().__init__(path=path, data=data)
        self.set('clusters', {
            'docker': {'type': 'docker'},
            'kubernetes': {'type': 'kubernetes'},
            **self.get('clusters', {}),
        })

    @property
    def clusters(self) -> list:
        return self.get('clusters', {}, False)

    @property
    def default_cluster(self) -> str:
        return self.get('default_cluster', 'docker', False)
    
    @default_cluster.setter
    def default_cluster(self, value):
        self.set("default_cluster", value)

    def get_cluster(self, cluster_name: str = None):
        if cluster_name is None:
            cluster_name = self.default_cluster
        if cluster_name not in self.clusters:
            raise RuntimeError(
                f'No configuration found for cluster {cluster_name}')
        return get_cluster_provider(**self.get(f'clusters.{cluster_name}'))

    @staticmethod
    def load(path: str = None) -> None:
        if path is None:
            path = get_config_path()

        if not os.path.exists(path):
            return CowaitConfig(data={})

        return CowaitConfig(path=path)

    def write(self, path: str = None) -> None:
        if path is None:
            path = get_config_path()
        return super().write(path)
