Module cowait.cli.task_image
============================

Classes
-------

`BuildError(*args, **kwargs)`
:   Unspecified run-time error.

    ### Ancestors (in MRO)

    * builtins.RuntimeError
    * builtins.Exception
    * builtins.BaseException

`TaskImage(context)`
:   

    ### Static methods

    `build_image(quiet: bool, **kwargs)`
    :

    `get(name_or_id)`
    :

    `open(context: cowait.cli.context.Context = None)`
    :

    `pull(name: str, tag: str = 'latest') ‑> NoneType`
    :

    ### Instance variables

    `name`
    :

    ### Methods

    `build(self, base: str, requirements: str = None, buildargs: dict = {}, quiet: bool = False) ‑> NoneType`
    :   Build task image

    `push(self)`
    :   Push context image to a remote registry.