
from cowait.tasks.notebook.code_builder import CodeBuilder


def test_is_empty_by_default():
    code = CodeBuilder()

    assert str(code) == ''

def test_ignores_trailing_new_line():
    codeWith = CodeBuilder().append(0, 'a\n')
    codeWithout = CodeBuilder().append(0, 'a')

    assert str(codeWith) == str(codeWithout)

def test_appends_lines_on_separate_lines():
    code = CodeBuilder()
    code.append(0, 'abc = 5')
    code.append(0, 'def = 7')

    assert str(code) == (
        'abc = 5\n'
        'def = 7\n')

def test_appends_line_with_indentation():
    code = CodeBuilder()
    code.append(3, 'some code')

    assert str(code) == '   some code\n'

def test_appends_code_block():
    block = CodeBuilder()
    block.append(0, 'line 2')
    block.append(3, 'line 3')
    
    code = CodeBuilder()
    code.append(3, 'line 1')
    code.appendBlock(2, block)

    assert str(code) == (
        '   line 1\n'
        '  line 2\n'
        '     line 3\n')

