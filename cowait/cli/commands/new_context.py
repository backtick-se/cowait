import os
import os.path
import yaml
from ..const import CONTEXT_FILE_NAME


def new_context(
    name: str,
    image: str,
    base: str,
    cluster_name: str = None,
):
    path = os.getcwd()

    # create directory
    current_dir = os.path.basename(path)
    if current_dir != name and name is not None:
        path = os.path.join(path, name.lower())
        os.mkdir(path)
        print('Created context folder', path)

    context = {}

    # image name
    if image is not None:
        print('Image:', image)
        context['image'] = image

    # base image name
    if base is not None:
        print('Base image:', base)
        context['base'] = base

    # override default cluster
    if cluster_name is not None:
        context['cluster'] = cluster_name

    context_file = os.path.join(path, CONTEXT_FILE_NAME)
    if os.path.isfile(context_file):
        print('Error: Context file', context_file, 'already exists')
        return

    with open(context_file, 'w') as cf:
        yaml.dump(
            {
                'version': 1,
                'cowait': context,
            },
            stream=cf,
            sort_keys=False,
        )

    print('Created new context definition', context_file)
