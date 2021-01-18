import click
import cowait.cli.commands
from .utils import parse_input_list


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
@click.option('-a', '--arg',
              type=str,
              multiple=True,
              help='docker build argument')
@click.option('-p', '--push',
              type=bool, is_flag=True,
              help='push image after building',
              default=False)
@click.pass_context
def build(ctx, quiet: bool, workdir: str, image: str, arg: dict, push: bool):
    cowait.cli.build(
        ctx.obj,
        quiet=quiet,
        workdir=workdir,
        image_name=image,
        buildargs=parse_input_list(arg),
        push=push,
    )


@click.command(help='push a task to the registry')
@click.pass_context
def push(ctx):
    cowait.cli.push(ctx.obj)
