import inspect
from cowait.tasks.components import TaskManager


def html_repr(target):
    if not inspect.isclass(target):
        raise AttributeError(f'Target must be a class')

    if hasattr(target, '_repr_html_'):
        raise AttributeError(f'{target.__name__} already has a _repr_html_ method')

    def decorate(fn):
        setattr(target, '_repr_html_', fn)
        return fn

    return decorate


@html_repr(TaskManager)
def task_manager_html(self):
    rows = ''.join([task_row_html(t) for t in self.values()])
    if len(rows) == 0:
        rows = f'<tr><td colspan="3">no tasks</td></tr>'

    return (f'<table>'
            f'<tr>'
            f'<th>id</th>'
            f'<th>status</th>'
            f'<th>inputs</th>'
            f'</tr>'
            f'{rows}'
            f'</table>')


def task_row_html(task):
    return (f'<tr>'
            f'<td>{task.id}</td>'
            f'<td>{task.status}</td>'
            f'<td>{task.inputs}</td>'
            f'</tr>')
