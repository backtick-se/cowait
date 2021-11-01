import os
from cowait.tasks import TaskDefinition
from cowait.engine.const import ENV_TASK_DEFINITION, MAX_ENV_LENGTH
from cowait.engine.utils import env_unpack, base_environment
from cowait.engine.errors import ProviderError


def create_ports(taskdef):
    return taskdef.ports


def create_env(cluster, taskdef):
    env = base_environment(cluster, taskdef)

    # check total length of environment data
    length = 0
    for key, value in env.items():
        if isinstance(value, dict):
            # complex env settings are not supported by DockerProvider
            # try to inherit the setting from the host
            if key in os.environ:
                value = os.environ[key]
            elif 'fallback' in value:
                value = value['fallback']
            else:
                source = value.get('source', '<unset>')
                print(f'Warning: unset environment variable {key} with source "{source}"')
                value = ''

        length += len(str(key)) + len(str(value))
        env[key] = str(value)

    if length > MAX_ENV_LENGTH:
        raise ProviderError(f'Task environment too long. Was {length}, max: {MAX_ENV_LENGTH}')

    return env


def extract_container_taskdef(container) -> TaskDefinition:
    for env in container.attrs['Config']['Env']:
        if ENV_TASK_DEFINITION == env[0:len(ENV_TASK_DEFINITION)]:
            data = env[len(ENV_TASK_DEFINITION)+1:]
            return TaskDefinition(**env_unpack(data))
    raise Exception('Unable to unpack container task definition')
