from .const import DEFAULT_REPO, DEFAULT_BASE_IMAGE


def parse_task_image_name(
    full_name: str,
    default_image: str = DEFAULT_BASE_IMAGE
) -> (str, str):
    image = default_image
    name = full_name
    if '/' in full_name:
        s = full_name.rfind('/')
        image = full_name[:s]
        name = full_name[s+1:]
        if '/' not in image:
            # prepend default repo
            image = f'{DEFAULT_REPO}/{image}'

    return image, name
