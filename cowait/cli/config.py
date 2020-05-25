import yaml
import os.path
from cowait.engine import get_cluster_provider
from .const import CONTEXT_FILE_NAME


class CowaitConfig(object):
    def __init__(self, default_cluster: str = 'docker', clusters: dict = {}):
        self.default_cluster = default_cluster
        self.clusters = {
            'docker': {'type': 'docker'},
            'kubernetes': {'type': 'kubernetes'},
            **clusters,
        }

    def get_cluster(self, cluster_name: str = None):
        if cluster_name not in self.clusters:
            raise RuntimeError(
                f'No configuration found for cluster {cluster_name}')
        return get_cluster_provider(**self.clusters[cluster_name])

    @staticmethod
    def load():
        home = os.path.expanduser('~')
        cfgpath = f'{home}/.{CONTEXT_FILE_NAME}'
        if not os.path.exists(cfgpath):
            return CowaitConfig()
        with open(cfgpath) as cfg:
            return CowaitConfig(**yaml.load(cfg, Loader=yaml.FullLoader))
