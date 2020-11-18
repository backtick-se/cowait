import sys
import yaml
import json
import click
import cowait.cli.commands
from cowait.cli import CliError
from cowait.cli.config import CowaitConfig
from cowait.utils import version_string


def option_val(val):
    try:
        return json.loads(val)
    except json.JSONDecodeError:
        return val


def option_dict(opts):
    options = {}
    for [key, val] in opts:
        options[key] = option_val(val)
    return options


@click.group()
@click.version_option(version_string())
@click.pass_context
def cli(ctx):
    pass


#
# context commands
#


@cli.command(help='create a new context')
@click.argument('name', type=str, required=False)
@click.option('--image', type=str, required=False, help='image name')
@click.option('--base', type=str, required=False, help='base image name')
@click.pass_context
def new(ctx, name: str, image: str, base: str):
    cowait.cli.new_context(
        ctx.obj,
        name=name,
        image=image,
        base=base,
    )


#
# task commands
#


@cli.command(help='run a task')
@click.argument('task', type=str)
@click.option('-c', '--cluster',
              default=None,
              type=str,
              help='cluster name')
@click.option('-n', '--name',
              type=str,
              default=None,
              help='specific task name')
@click.option('-i', '--input',
              type=(str, str),
              multiple=True,
              help='specify task input')
@click.option('-e', '--env',
              type=(str, str),
              multiple=True,
              help='define enviornment variable')
@click.option('-p', '--port', type=int, multiple=True, help='open a port')
@click.option('-r', '--route',
              type=(str, str),
              multiple=True,
              help='add an ingress route')
@click.option('-u', '--upstream',
              type=str,
              help='root task upstream uri')
@click.option('-b', '--build',
              type=bool, is_flag=True,
              help='build and push first',
              default=False)
@click.option('-d', '--detach',
              type=bool, is_flag=True,
              help='run in detached mode',
              default=False)
@click.option('--cpu',
              help='cpu request',
              type=str,
              default=None)
@click.option('--cpu-limit',
              help='cpu limit',
              type=str,
              default=None)
@click.option('--memory', '--mem',
              help='memory request',
              type=str,
              default=None)
@click.option('--memory-limit', '--mem-limit',
              help='memory limit',
              type=str,
              default=None)
@click.option('-f', '--json', '--yml', '--yaml', 'file', 
              help='yaml/json file with inputs', 
              type=str, 
              default=None)
@click.option('--raw',
              type=bool, is_flag=True,
              help='raw json output',
              default=False)
@click.option('-q', '--quiet',
              type=bool, is_flag=True,
              help='no output except result',
              default=False)
@click.pass_context
def run(
    ctx, task: str, cluster: str, name: str,
    input, env, port, route,
    upstream: str, build: bool, detach: bool,
    cpu: str, cpu_limit: str, memory: str, memory_limit: str,
    file: str, raw: bool, quiet: bool
):
    file_inputs = {}
    if file is not None:
        try:
            with open(file, 'r') as f:
                file_inputs = yaml.load(f, Loader=yaml.FullLoader)
        except yaml.parser.ParserError as e:
            raise CliError(f'Error in {file}: {e}')

    if not isinstance(file_inputs, dict):
        raise CliError('Error: Expected input file to contain a dictionary')

    cowait.cli.run(
        ctx.obj,
        task,
        name=name,
        inputs={
            **file_inputs,
            **option_dict(input),
        },
        env=option_dict(env),
        ports={p: p for p in port},
        routes=option_dict(route),
        upstream=upstream,
        build=build,
        detach=detach,
        raw=raw,
        quiet=quiet,
        cpu=cpu,
        cpu_limit=cpu_limit,
        memory=memory,
        memory_limit=memory_limit,
        cluster_name=cluster,
    )


@cli.command(help='run task tests')
@click.option('-c', '--cluster',
              default=None,
              type=str,
              help='cluster name')
@click.option('--push',
              type=bool, is_flag=True,
              help='build and push first',
              default=False)
@click.pass_context
def test(ctx, cluster: str, push: bool):
    cowait.cli.test(ctx.obj, push, cluster_name=cluster)


@cli.command(help='destroy tasks')
@click.option('-c', '--cluster',
              default=None,
              type=str,
              help='cluster name')
@click.pass_context
def rm(ctx, cluster: str):
    cowait.cli.destroy(ctx.obj, cluster_name=cluster)


@cli.command(help='list tasks')
@click.option('-c', '--cluster',
              default=None,
              type=str,
              help='cluster name')
@click.pass_context
def ps(ctx, cluster: str):
    cowait.cli.list_tasks(ctx.obj, cluster_name=cluster)


@cli.command(help='kill tasks by id')
@click.option('-c', '--cluster',
              default=None,
              type=str,
              help='cluster name')
@click.argument('task', type=str)
@click.pass_context
def kill(ctx, cluster: str, task: str):
    cowait.cli.kill(ctx.obj, task, cluster_name=cluster)


@cli.command(help='deploy cowait agent')
@click.option('-c', '--cluster',
              default=None,
              type=str,
              help='cluster name')
@click.option('-d', '--detach',
              type=bool, is_flag=True,
              help='run in detached mode',
              default=False)
@click.option('-u', '--upstream',
              type=str, default=None,
              help='custom upstream uri')
@click.pass_context
def agent(ctx, cluster: str, detach: bool, upstream: str):
    cowait.cli.agent(ctx.obj, detach, upstream, cluster_name=cluster)


@cli.command(help='start notebook')
@click.option('-c', '--cluster',
              default=None,
              type=str,
              help='cluster name')
@click.option('-b', '--build',
              type=bool, is_flag=True,
              help='build and push first',
              default=False)
@click.option('-i', '--image',
              type=str,
              default=None,
              help='default image')
@click.pass_context
def notebook(ctx, cluster, build, image):
    cowait.cli.notebook(ctx.obj, build, image, cluster_name=cluster)


#
# task image commands
#


@cli.command(help='build a task')
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


@cli.command(help='push a task to the registry')
def push():
    cowait.cli.push()


#
# cluster subcommand
#


@cli.group(help='cluster management')
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
              type=(str, str),
              multiple=True,
              help='specify cluster provider option')
@click.pass_context
def add(ctx, name: str, type: str, option: dict = {}):
    cowait.cli.cluster_add(ctx.obj, name, type.lower(), **option_dict(option))


@cluster.command(help='remove cluster')
@click.argument('name', type=str)
@click.pass_context
def rm(ctx, name: str):
    cowait.cli.cluster_rm(ctx.obj, name)


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    config = CowaitConfig.get_global()
    try:
        cli(obj=config)
    except CliError as e:
        print(f'Error: {e}')


if __name__ == "__main__":
    sys.exit(main())
