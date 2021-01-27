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

