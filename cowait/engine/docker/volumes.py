from docker.types import Mount


def create_volumes(volumes: dict) -> list:
    mounts = [
        # this is the secret sauce that allows us to create new
        # tasks as sibling containers
        create_bind_mount('/var/run/docker.sock', {
            'src': '/var/run/docker.sock',
            'mode': 'ro',
        })
    ]

    for target, volume in volumes.items():
        if 'bind' in volume:
            mounts.append(create_bind_mount(target, volume['bind']))
        elif 'tmpfs' in volume:
            mounts.append(create_tmpfs_mount(target, volume['tmpfs']))

    return mounts


def create_bind_mount(target: str, bind) -> Mount:
    mode = 'rw'
    src = None
    if isinstance(bind, str):
        src = bind
    elif isinstance(bind, dict):
        src = bind.get('src')
        mode = bind.get('mode', 'rw')
    else:
        raise TypeError(f'Invalid bind volume definition {target}')

    return Mount(
        type='bind',
        target=target,
        source=src,
        read_only=mode != 'rw',
    )


def create_tmpfs_mount(target: str, tmpfs) -> Mount:
    size = 0
    mode = 0
    if isinstance(tmpfs, dict):
        size = tmpfs.get('size')
        mode = tmpfs.get('mode', 1777)
    else:
        raise TypeError(f'Invalid tmpfs volume definition {target}')

    return Mount(
        type='tmpfs',
        target=target,
        tmpfs_size=size,
        tmpfs_mode=mode,
    )
