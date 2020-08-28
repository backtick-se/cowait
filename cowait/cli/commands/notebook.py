from .run import run as run_cmd


def notebook(config, build, image = None):
    task = 'cowait.notebook'
    if image is not None:
        task = f'{image}/{task}'
    return run_cmd(
        config=config,
        task=task,
        build=build,
        routes={
            '/': '8888',
        },
    )
