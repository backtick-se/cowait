import sys
from cowait.cli import CliError
from cowait.cli.config import Config
from cowait.cli.app import new_cli_app


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    config = Config.get_global()
    app = new_cli_app()
    try:
        app(obj=config)
    except CliError as e:
        print(f'Error: {e}')


if __name__ == "__main__":
    sys.exit(main())
