Module cowait.tasks.ops
=======================

Functions
---------

    
`join(tasks: list) ‑> list`
:   Waits for a list of tasks to complete, returning a list containing their results.

    
`wait(tasks: list, ignore_errors: bool = False) ‑> NoneType`
:   Waits for a list of tasks to complete. Returns nothing.