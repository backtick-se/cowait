import click
import cowait.cli.commands
from .utils import parse_input_list


@click.group(help='cluster management')
@click.pass_context
def cluster(ctx):
    pass


@cluster.command(help='describe cluster')
@click.argument('name', type=str)
@click.pass_context
def get(ctx, name: str):
    cowait.cli.cluster_get(ctx.obj, name)


@cluster.command(help='list all clusters')
@click.pass_context
def ls(ctx):
    cowait.cli.cluster_ls(ctx.obj)


@cluster.command(help='default cluster name')
@click.pass_context
def default(ctx):
    cowait.cli.cluster_default(ctx.obj)


@cluster.command(help='set default cluster')
@click.argument('name', type=str)
@click.pass_context
def set_default(ctx, name: str):
    cowait.cli.cluster_set_default(ctx.obj, name)


@cluster.command(help='add new cluster')
@click.argument('name', type=str)
@click.option('--type', type=str, help='cluster provider type')
@click.option('-o', '--option',
              type=str,
              multiple=True,
              help='specify cluster provider option')
@click.pass_context
def add(ctx, name: str, type: str, option: dict = {}):
    cowait.cli.cluster_add(ctx.obj, name, type.lower(), **parse_input_list(option))


@cluster.command(help='remove cluster')
@click.argument('name', type=str)
@click.pass_context
def rm(ctx, name: str):
    cowait.cli.cluster_rm(ctx.obj, name)
