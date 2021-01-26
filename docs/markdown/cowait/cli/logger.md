Module cowait.cli.logger
========================

Classes
-------

`Logger(quiet: bool = False, time: bool = True)`
:   

    ### Descendants

    * cowait.cli.commands.run.RunLogger
    * cowait.cli.commands.test.TestLogger

    ### Instance variables

    `newline_indent`
    :

    ### Methods

    `header(self, title: str = None)`
    :

    `json(self, obj, indent: int = 0, lv=0)`
    :

    `print(self, *args)`
    :

    `print_exception(self, error)`
    :

    `print_time(self, ts: str = None)`
    :

    `println(self, *args, time=False)`
    :