import yaml
import click
import cowait.cli.commands
from cowait.cli import CliError
from .utils import parse_input_list


@click.command(help='run a task')
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
              type=str,
              multiple=True,
              help='specify task input')
@click.option('-e', '--env',
              type=str,
              multiple=True,
              help='define enviornment variable')
@click.option('-p', '--port', type=int, multiple=True, help='open a port')
@click.option('-r', '--route',
              type=str,
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
@click.option('-a', '--affinity',
              help='task affinity (stack/spread)',
              type=str,
              default=None)
@click.pass_context
def run(
    ctx, task: str, cluster: str, name: str,
    input, env, port, route,
    upstream: str, build: bool, detach: bool,
    cpu: str, cpu_limit: str, memory: str, memory_limit: str,
    file: str, raw: bool, quiet: bool, affinity: str
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
            **parse_input_list(input),
        },
        env=parse_input_list(env),
        ports={p: p for p in port},
        routes=parse_input_list(route),
        upstream=upstream,
        build=build,
        detach=detach,
        raw=raw,
        quiet=quiet,
        cpu=cpu,
        cpu_limit=cpu_limit,
        memory=memory,
        memory_limit=memory_limit,
        affinity=affinity,
        cluster_name=cluster,
    )


@click.command(help='run task tests')
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


@click.command(help='destroy tasks')
@click.option('-c', '--cluster',
              default=None,
              type=str,
              help='cluster name')
@click.pass_context
def rm(ctx, cluster: str):
    cowait.cli.destroy(ctx.obj, cluster_name=cluster)


@click.command(help='list tasks')
@click.option('-c', '--cluster',
              default=None,
              type=str,
              help='cluster name')
@click.pass_context
def ps(ctx, cluster: str):
    cowait.cli.list_tasks(ctx.obj, cluster_name=cluster)


@click.command(help='kill tasks by id')
@click.option('-c', '--cluster',
              default=None,
              type=str,
              help='cluster name')
@click.argument('task', type=str)
@click.pass_context
def kill(ctx, cluster: str, task: str):
    cowait.cli.kill(ctx.obj, task, cluster_name=cluster)


@click.command(help='deploy cowait agent')
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


@click.command(help='start notebook')
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
