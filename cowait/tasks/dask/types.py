from dask.distributed import Client
from cowait.types import Type, TypeAlias

SCHEDULER_URI = 'scheduler_uri'


@TypeAlias(Client)
class DaskClientType(Type):
    name: str = 'DaskClient'

    def validate(self, client: Client, name: str) -> None:
        if not isinstance(client, dict):
            raise ValueError(f'{name} is not a DaskClient')
        if SCHEDULER_URI not in client:
            raise ValueError(f'{name} is not a valid DaskClient: Missing {SCHEDULER_URI}')

    def serialize(self, client: Client):
        return {
            SCHEDULER_URI: client.scheduler.address,
        }

    def deserialize(self, value: dict):
        return Client(
            address=value[SCHEDULER_URI]
        )
