import os
from .run import run as run_cmd
from .build import build as build_cmd
from ..context import Context
from ..docker_file import Dockerfile
from ..task_image import TaskImage


def notebook(config, build: bool, image: str = None, cluster_name: str = None) -> None:
    if image is None:
        context = Context.open(config)

        # rebuild task image first
        if build:
            build_cmd(config, quiet=False)

        df = Dockerfile(context.image)
        df.run('pip install jupyterlab dill --no-cache-dir')

        buildctx = '/tmp/cowait-notebook-ctx'
        os.makedirs(buildctx, exist_ok=True)
        try:
            nbimage = TaskImage.build_image(path=buildctx, dockerfile=str(df), quiet=False)
            image = nbimage.short_id[7:]
        finally:
            os.removedirs(buildctx)

    return run_cmd(
        config=config,
        task='cowait.notebook',
        build=False,
        image=image,
        routes={
            '/': '8888',
        },
        cluster_name=cluster_name,
        volumes={
            '/var/task': {
                'bind': {
                    'src': os.getcwd(),
                    'mode': 'rw',
                    'inherit': 'same-image',
                },
            },
        },
    )
