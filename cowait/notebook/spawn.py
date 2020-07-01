from cowait.tasks.pickled import PickledTask, pickle_task


def task(task_func):
    def spawn_task(*args, **inputs):
        if len(args) > 0:
            raise TypeError('Use keyword arguments for task inputs')
        return PickledTask(func=pickle_task(task_func), **inputs)
    return spawn_task
