import ast
import json
import cowait
from cowait import Task
from .code_builder import CodeBuilder


class NotebookRunner(Task):
    async def run(self, path: str, **inputs):
        if not path.endswith('.ipynb'):
            path += '.ipynb'
        cells = file_to_json(path)['cells']

        code = CodeBuilder()

        code.append(0, 'async def _notebook_runner():')

        code.appendBlock(4, cells_to_code(cells))

        global_scope = {'cowait': cowait, 'NotebookRunner': self.__class__}
        local_scope = {}
        exec(str(code), global_scope, local_scope)
        handle = local_scope['_notebook_runner']
        return await handle()


def cells_to_code(cells):
    code = CodeBuilder()
    for cell in cells:
        cell_type = cell['cell_type']

        if cell_type == 'code':
            source_rows = [row[:-1] if row[-1] == '\n' else row for row in cell['source']]

            if len(source_rows) > 0:
                code.appendBlock(0, code_from_source(source_rows))
                code.append(0, '')

    return code


def code_from_source(source_rows):
    code = CodeBuilder()

    _, first_line = strip_indentation(source_rows[0])
    if first_line.startswith('%%'):
        command, *args = first_line[2:].split(' ', 1)
        new_code = transform_cell_magic(source_rows[1:], command, args)
        if new_code:
            code.appendBlock(0, new_code)
    else:
        for row in source_rows:
            indentation, line = strip_indentation(row)
            if line.startswith('global '):
                new_line = 'nonlocal ' + line[7:]
                code.append(indentation, new_line)
                print(f"Warning: Replaced '{line}' with '{new_line}'")
            elif line.startswith('%'):  # Not supported: a = %ls
                command, *args = line[1:].split(' ', 1)
                new_code = transform_line_magic(command, args)
                if new_code:
                    code.appendBlock(indentation, new_code)
            else:
                code.append(indentation, line)

    # If there is a syntax error it will be found here
    try:
        ast.parse(str(code), filename='<notebook cell>')
    except SyntaxError as e:
        syntax_error = SyntaxError(f"{e.msg}\nThe error is located somewhere in this cell:\n\n{str(code)}", e.args[1])
        raise syntax_error from None

    return code


def strip_indentation(row):
    line = row.lstrip(' ')
    return len(row) - len(line), line


def transform_line_magic(command: str, args: str):
    ignorables = ['lsmagic', 'matplotlib']

    if command in ignorables:
        return None

    raise ValueError(f"Magic command %{command} is not supported")


def transform_cell_magic(rows: list, command: str, args: str):
    ignorables = ['html', 'HTML', 'markdown', 'latex']

    if command in ignorables:
        return None

    raise ValueError(f"Magic command %%{command} is not supported")


def file_to_json(path):
    with open(path, 'r') as f:
        return json.load(f)
