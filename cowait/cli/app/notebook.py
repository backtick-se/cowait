import yaml
import click
import cowait.cli.commands
from cowait.cli import CliError
from .utils import parse_input_list


@click.group(help='start notebook', invoke_without_command=True)
@click.option('-c', '--cluster',
              default=None,
              type=str,
              help='cluster name')
@click.option('-i', '--image',
              type=str,
              default=None,
              help='remote image')
@click.pass_context
def notebook(ctx, cluster, image):
    if ctx.invoked_subcommand is None:
        cowait.cli.notebook(ctx.obj, image, cluster_name=cluster)


@notebook.command(help='run notebook as a task')
@click.argument('path', type=str)
@click.option('--image',
              default=None,
              type=str,
              help='image name')
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
@click.option('-b', '--build',
              type=bool, is_flag=True,
              help='build and push first',
              default=False)
@click.option('-d', '--detach',
              type=bool, is_flag=True,
              help='run in detached mode',
              default=False)
@click.option('-f', '--json', '--yml', '--yaml', 'file',
              help='yaml/json file with inputs',
              type=str,
              default=None)
@click.option('-q', '--quiet',
              type=bool, is_flag=True,
              help='no output except result',
              default=False)
@click.pass_context
def run(
    ctx, path: str, image: str, cluster: str, name: str,
    input, env, build: bool, detach: bool, file: str, quiet: bool
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

    cowait.cli.run_notebook(
        ctx.obj,
        path,
        image=image,
        cluster=cluster,
        name=name,
        inputs={
            **file_inputs,
            **parse_input_list(input),
        },
        env=parse_input_list(env),
        build=build,
        detach=detach,
        quiet=quiet)
