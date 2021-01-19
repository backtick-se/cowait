

def pod_is_unschedulable(pod):
    for cond in pod.status.conditions:
        if cond.type == 'PodScheduled' and cond.status == 'False':
            return True
    return False


def pod_is_terminated(pod):
    statuses = pod.status.container_statuses
    if statuses is None:
        return False
    for status in statuses:
        if status.state.terminated is not None:
            return True
    return False


def pod_is_creating(pod):
    statuses = pod.status.container_statuses
    if statuses is None:
        return False
    for status in statuses:
        if status.state.waiting is not None:
            if status.state.waiting.reason == 'ContainerCreating':
                return True
    return False


def pod_is_running(pod):
    statuses = pod.status.container_statuses
    if statuses is None:
        return False
    for status in statuses:
        if status.state.running is not None:
            return True
    return False


def pod_image_pull_failed(pod):
    statuses = pod.status.container_statuses
    if statuses is None:
        return False
    for status in statuses:
        if status.state.waiting is not None:
            # abort if the image is not available
            if status.state.waiting.reason == 'ErrImagePull':
                return True
            if status.state.waiting.reason == 'ImagePullBackoff':
                return True
    return False
