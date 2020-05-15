import sys
import json
from ..task_image import TaskImage
from ..const import CONTEXT_FILE_NAME
from .build import build


def push() -> TaskImage:
    image = build()

    if image is None or '/' not in image.name:
        print(f'Error: You must specify a full image name in '
              f'{CONTEXT_FILE_NAME} before you can push')
        return

    sys.stdout.write('pushing...')
    logs = image.push()
    progress = {}
    for log in logs:
        rows = log.decode('utf-8').split('\r\n')
        for data in rows:
            if len(data) == 0:
                continue
            update = json.loads(data.strip())
            if 'id' in update and 'progressDetail' in update:
                id = update['id']
                progress[id] = update['progressDetail']

        current = 0
        total = 0
        for detail in progress.values():
            current += detail.get('current', 0)
            total += detail.get('total', 0)

        if total > 0:
            pct = 100 * min(current / total, 1.0)
            sys.stdout.write(f'\rpushing... {pct:0.2f}%  ')
            sys.stdout.flush()

    sys.stdout.write(f'\rpushing... done       \n')
    sys.stdout.flush()
    return image
