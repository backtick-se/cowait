import json
from pathlib import Path

from .code_builder import CodeBuilder

def file_to_json(path):
    s = None
    with open(path, 'r') as f:
        s = f.read()
    return json.loads(s)

def snake_to_upper_camel_case(s: str) -> str:
    parts = s.split('_')
    return ''.join(p.title() for p in parts)

def file_name(path: str) -> str:
    return Path(path).stem

def change_extension(path: str, ext: str) -> str:
    left_dot_idx = path.rfind('.')
    left_slash_idx = path.rfind('/')

    if left_dot_idx > left_slash_idx:
        return path[:left_dot_idx] + '.' + ext
    else:
        return path + '.' + ext

def to_code_string(v) -> str:
    vStr = str(v)
    if isinstance(v, str):
        vStr = '\'' + v + '\''
    return vStr
