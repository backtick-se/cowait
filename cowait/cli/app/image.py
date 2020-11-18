import click
import cowait.cli.commands


@click.command(help='build a task')
@click.option('-q', '--quiet',
              type=bool, is_flag=True,
              help='no output except result',
              default=False)
@click.option('-w', '--workdir',
              default=None,
              type=str,
              help='task working directory')
@click.option('-i', '--image',
              default=None,
              type=str,
              help='image name')
def build(quiet: bool, workdir: str, image: str):
    cowait.cli.build(
        quiet=quiet,
        workdir=workdir,
        image_name=image,
    )


@click.command(help='push a task to the registry')
def push():
    cowait.cli.push()
