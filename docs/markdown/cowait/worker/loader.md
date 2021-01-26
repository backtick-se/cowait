Module cowait.worker.loader
===========================

Functions
---------

    
`load_task_class(task_name: str) ‑> <class 'TypeVar'>`
:   Loads a task class from the given module.
    
    Arguments:
        task_name (str): Import path of the module containing the task.
    
    Raises:
        TaskNotFoundError
    
    Returns:
        Class (type)