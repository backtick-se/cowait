import sys
from ..task_image import TaskImage
from ..const import CONTEXT_FILE_NAME
from ..config import Config
from ..context import Context
from ..utils import ProgressBars


def push(config: Config, **kwargs) -> TaskImage:
    context = Context.open(config)
    image = TaskImage.open(context)

    if image is None:
        print('Error: Failed to resolve task image')
        sys.exit(1)

    if '/' not in image.name:
        print(f'Error: You must specify a full image name in '
              f'{CONTEXT_FILE_NAME} before you can push')
        sys.exit(1)

    print('Pushing image')

    progress = ProgressBars()
    logs = image.push()
    for update in logs:
        if 'id' in update and 'progressDetail' in update:
            id = update['id']
            detail = update['progressDetail']
            if not progress.has(id):
                progress.add(id, id, 0, 0)
            if 'total' in detail:
                progress.set(id, detail['current'], detail['total'])
            progress.refresh()

        if 'errorDetail' in update:
            print('Error:', update['error'])
            sys.exit(1)

    return image
