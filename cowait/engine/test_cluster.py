import pytest
from .const import MAX_ENV_LENGTH
from .cluster import ClusterProvider
from .errors import ProviderError
from cowait.tasks import TaskDefinition
from cowait.utils import uuid


def test_max_env_length():
    """ Passing too large inputs should raise a ProviderError """
    random_data = uuid(2 * MAX_ENV_LENGTH, lower=False)

    with pytest.raises(ProviderError):
        cp = ClusterProvider('test')
        cp.create_env(TaskDefinition(
            'test-task',
            image='imaginary-image',
            inputs={
                'ohshit': random_data,
            },
        ))
