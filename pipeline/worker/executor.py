import os
import json
import importlib
import traceback
from typing import Dict, TypeVar
from contextlib import nullcontext
from pipeline.engine import ClusterProvider
from pipeline.tasks import TaskContext, TaskDefinition, TaskError
from pipeline.utils.stream_capture import StreamCapturing
from .connector import WorkerConnector


def get_task_class(taskdef: TaskDefinition) -> TypeVar:
    module = importlib.import_module(taskdef.name)

    try:
        task_class = getattr(module, 'Task')
        return task_class
    except AttributeError:
        raise RuntimeError('No task class exported from module')


def execute(cluster: ClusterProvider, upstream: WorkerConnector, taskdef: TaskDefinition) -> None:
    # create task context
    context = TaskContext(
        cluster  = cluster,
        upstream = upstream,
        taskdef  = taskdef,
    )

    # instantiate & run task
    upstream.run()

    try:
        # set up output capturing
        root_task = context.parent == 'root'
        capturing = StreamCapturing(
            on_stdout = lambda x: upstream.log('stdout', x),
            on_stderr = lambda x: upstream.log('stderr', x),
        ) if not root_task else nullcontext()

        # run task within capture context
        with capturing:
            TaskClass = get_task_class(taskdef)
            task = TaskClass(context)
            result = task.run(**taskdef.inputs)

        # submit result
        upstream.done(result)

    except TaskError as e:
        # pass subtask errors upstream
        upstream.fail(e.error)
        exit(1)

    except:
        # capture local errors
        error = traceback.format_exc()
        upstream.fail(error)
        exit(1)

    exit(0)