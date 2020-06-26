from .run import run as run_cmd


def notebook(config, build):
    return run_cmd(
        config=config,
        task='cowait.notebook',
        build=build,
        routes={
            '/': '8888',
        },
    )
