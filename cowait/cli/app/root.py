import click
from cowait.version import version
from . import task, image, context
from .cluster import cluster


def new_cli_app():
    @click.group()
    @click.version_option(version)
    @click.pass_context
    def cli(ctx):
        pass

    # task commands
    cli.add_command(task.run)
    cli.add_command(task.kill)
    cli.add_command(task.ps)
    cli.add_command(task.rm)
    cli.add_command(task.agent)
    cli.add_command(task.notebook)
    cli.add_command(task.test)

    # image commands
    cli.add_command(image.build)
    cli.add_command(image.push)

    # context commands
    cli.add_command(context.new)

    # cluster commands
    cli.add_command(cluster)

    return cli
