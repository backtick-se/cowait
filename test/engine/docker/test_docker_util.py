import pytest
from cowait.engine.const import MAX_ENV_LENGTH
from cowait.engine.cluster import ClusterProvider
from cowait.engine.errors import ProviderError
from cowait.tasks import TaskDefinition
from cowait.utils import uuid
from cowait.engine.docker.utils import create_env


def test_max_env_length():
    """ Passing too large inputs should raise a ProviderError """
    random_data = uuid(2 * MAX_ENV_LENGTH, lower=False)

    with pytest.raises(ProviderError):
        cp = ClusterProvider('test')
        create_env(cp, TaskDefinition(
            'test-task',
            image='imaginary-image',
            inputs={
                'ohshit': random_data,
            },
        ))

