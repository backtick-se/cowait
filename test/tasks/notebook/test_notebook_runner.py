import pytest
import cowait.tasks.notebook.notebook_runner as nb


def test_file_to_json():
    json = nb.file_to_json('test/tasks/notebook/sample_json_file.json')

    assert json == {
        "four": 4,
        "array": [5, 6],
        "obj": {
            "f": "a string"
        }
    }

def test_normal_code_cell():
    code = nb.cells_to_code([{
        'cell_type': 'code',
        'source': [
            'a = 5\n',
            'if a > 4:\n'
            '    print(a - 4)'
        ]
    }])
    assert str(code) == (
        'a = 5\n'
        'if a > 4:\n'
        '    print(a - 4)\n\n')

def test_markdown_cell():
    code = nb.cells_to_code([{
        'cell_type': 'markdown',
        'source': [
            '## Some text'
        ]
    }])

    assert str(code) == ''

def test_global_to_nonlocal():
    code = nb.code_from_source([
        'def a():',
        '    global v',
        '    v = 3'
    ])

    assert str(code) == (
        'def a():\n'
        '    nonlocal v\n'
        '    v = 3\n')

def test_ignorable_line_magics():
    code = nb.code_from_source([
        '%matplotlib inline',
        'plt.plot(a)'
    ])

    assert str(code) == 'plt.plot(a)\n'

def test_ignorable_cell_magics():
    code = nb.code_from_source([
        '%%latex',
        '\\int_0^4{x^2 dx}'
    ])

    assert str(code) == ''

def test_unsupported_line_magic():
    with pytest.raises(ValueError) as error_info:
        nb.code_from_source([
            '%%scala',
            'val a = 4',
            'val m = 2'
        ])
    
    error = error_info.value

    assert '%%scala' in error.args[0]

def test_unsupported_cell_magic():
    with pytest.raises(ValueError) as error_info:
        nb.code_from_source([
            'a = 4',
            '%cat file.py',
            'm = 2'
        ])
    
    error = error_info.value

    assert '%cat' in error.args[0]

def test_syntax_error():
    with pytest.raises(SyntaxError) as error_info:
        nb.code_from_source([
            'a = 5',
            'b =',
            'c = 7'
        ])

    error = error_info.value

    assert 'invalid syntax' in error.msg

    # The error should contain the source code from the problematic cell
    assert 'a = 5' in error.msg
    assert 'b =' in error.msg
    assert 'c = 7' in error.msg
