import json
from cowait.tasks import TaskDefinition
from cowait.engine.const import ENV_TASK_DEFINITION
from cowait.engine.utils import env_unpack
from .errors import PodTerminatedError, PodUnschedulableError, ImagePullError


def pod_is_ready(pod):
    if pod.status.conditions:
        for cond in pod.status.conditions:
            if cond.type == 'PodScheduled' and cond.status == 'False':
                raise PodUnschedulableError(cond.message)

    statuses = pod.status.container_statuses
    if statuses is None:
        return False

    for status in statuses:
        state = status.state

        if state.running is not None:
            return True

        if state.terminated is not None:
            raise PodTerminatedError()

        if state.waiting is not None:
            if state.waiting.reason == 'ContainerCreating':
                return False

            if state.waiting.reason == 'ErrImagePull':
                raise ImagePullError(state.waiting.message)

            if state.waiting.reason == 'ImagePullBackoff':
                raise ImagePullError(state.waiting.message)

    return False


def extract_pod_taskdef(pod) -> TaskDefinition:
    for container in pod.spec.containers:
        for env in container.env:
            if env.name == ENV_TASK_DEFINITION:
                taskdef = env_unpack(env.value)
                return TaskDefinition(**taskdef)
    raise Exception('Failed to extract pod task definition')

