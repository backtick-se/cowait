import click
import cowait.cli


@click.command(help='create a new context')
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
