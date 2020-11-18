import os
import os.path
from ..const import CONTEXT_FILE_NAME
from ..config import Config


def new_context(
    config: Config,
    name: str,
    image: str,
    base: str,
):
    path = os.getcwd()

    # create directory
    current_dir = os.path.basename(path)
    if current_dir != name and name is not None:
        path = os.path.join(path, name.lower())
        os.mkdir(path)
        print('Created context folder', path)

    context = Config(path=name, config=config)

    # image name
    if image is not None:
        print('Image:', image)
        context['image'] = image

    # base image name
    if base is not None:
        print('Base image:', base)
        context['base'] = base

    context_file = os.path.join(path, CONTEXT_FILE_NAME)
    if os.path.isfile(context_file):
        print('Error: Context file', context_file, 'already exists')
        return

    context.write(context_file)
    print('Created new context definition', context_file)
