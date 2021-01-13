from .run import run as run_cmd


def notebook(config, build: bool, image: str = None, cluster_name: str = None) -> None:
    if image is None:
        image = 'cowait/notebook'

    task = f'{image}/cowait.notebook'
    return run_cmd(
        config=config,
        task=task,
        build=build,
        routes={
            '/': '8888',
        },
        cluster_name=cluster_name,
    )
