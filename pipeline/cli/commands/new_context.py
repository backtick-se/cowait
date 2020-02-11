import os
import os.path
import yaml
from ..const import CONTEXT_FILE_NAME


def new_context(name: str, image: str, provider: str):
    name = name.lower()
    path = os.getcwd()

    # create directory
    current_dir = os.path.basename(path).lower()
    if current_dir != name:
        path = os.path.join(path, name)
        os.mkdir(path)
        print('Created context folder', path)

    context = {}
    if image is not None:
        context['image'] = image

    context_file = os.path.join(path, CONTEXT_FILE_NAME)
    if os.path.isfile(context_file):
        print('Error: Context file', context_file, 'already exists')
        return

    with open(context_file, 'w') as cf:
        yaml.dump(
            {
                'version': 1,
                'pipeline': context,
            },
            stream=cf,
            sort_keys=False,
        )
