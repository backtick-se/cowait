

class CodeBuilder:
    def __init__(self):
        self.lines = []
    
    def append(self, indentation: int, line: str):
        if len(line) > 0 and line[-1] != '\n':
            self.lines.append(' ' * indentation + line)
        else:
            self.lines.append(' ' * indentation + line[:-1])
        return self

    def appendBlock(self, indentation: int, block):
        for line in block.lines:
            self.append(indentation, line)
        return self
    
    def __str__(self):
        s = ''
        for line in self.lines:
            s += line
            s += '\n'
        return s
