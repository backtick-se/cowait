from datetime import datetime
import json
from sty import fg, rs
from time import time as ctime
from .utils import printheader


class Logger(object):
    def __init__(self, quiet: bool = False, time: bool = True):
        self.quiet = quiet
        self.time = time
        self.start = ctime()

    def header(self, title: str = None):
        if self.quiet:
            return
        printheader(title)

    @property
    def newline_indent(self):
        return 0 if not self.time else 6

    def print(self, *args):
        if self.quiet:
            return
        text = ' '.join(map(lambda s: str(s), args))
        last_break = text[-1] == '\n'
        if last_break:
            text = text[:-1]
        if self.newline_indent > 0:
            text = text.replace('\n', '\n'.ljust(self.newline_indent))
        print(text, end='' if not last_break else '\n')

    def println(self, *args, time=False):
        text = ' '.join(map(lambda s: str(s), args))
        if len(text) == 0 or text[-1] != '\n':
            text += '\n'
        self.print(text)

    def print_time(self, ts: str = None):
        if not self.time:
            return
        if ts is None:
            elapsed = ctime() - self.start
            self.print(f'{elapsed:05.1f} ')
        else:
            dt = datetime.fromisoformat(ts)
            timestamp = dt.strftime('%H:%M:%S')
            self.print(f'{timestamp} ')

    def print_exception(self, error):
        self.header(f'error')
        self.println(error)

    def json(self, obj, indent: int = 0, lv=0):
        idt = indent * lv * ' '
        keyc = fg.blue
        strc = fg.green
        numc = fg.red
        dotc = rs.all

        if isinstance(obj, dict):
            if len(obj) > 2 and len(obj) < 20 and indent > 0:
                return f'{idt}{dotc}{{{rs.all}\n' + \
                    f'\n{idt}'.join([
                        f'{keyc}{k}{dotc}:{rs.all} '+self.json(v, lv=lv+1, indent=indent)
                        for k, v in obj.items()
                    ]) + \
                    f'\n{idt}{keyc}}}{rs.all}'
            return f'{idt}{dotc}{{{rs.all} ' + \
                ', '.join([
                    f'{keyc}{k}{dotc}:{rs.all} '+self.json(v, lv=lv+1, indent=indent)
                    for k, v in obj.items()
                ]) + f' {dotc}}}{rs.all}'
        elif isinstance(obj, list):
            if len(obj) > 2 and len(obj) < 20 and indent > 0:
                return f'{idt}{dotc}[{rs.all}\n' + \
                    f'{dotc},{rs.all}\n{idt}'.join([
                        self.json(v, lv=lv+1, indent=indent)
                        for v in obj
                    ]) + f'\n{idt}{dotc}]{rs.all}'
            return f'{dotc}[{rs.all} ' + \
                f'{dotc},{rs.all} '.join([
                    self.json(v, lv=lv+1, indent=indent)
                    for v in obj
                ]) + f' {dotc}]{rs.all}'
        elif isinstance(obj, int):
            return f'{numc}{obj}{rs.all}'
        elif isinstance(obj, str):
            return f'{strc}' + json.dumps(obj) + rs.all
        elif isinstance(obj, bool):
            return f'{numc}true{rs.all}' if obj else f'{numc}false{rs.all}'
        else:
            return json.dumps(obj)
