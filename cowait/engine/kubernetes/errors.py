

class PodUnschedulableError(Exception):
    pass


class PodTerminatedError(Exception):
    pass


class ImagePullError(Exception):
    pass


class PodConfigError(Exception):
    pass
