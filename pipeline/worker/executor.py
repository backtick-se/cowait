import traceback
from contextlib import nullcontext
from pipeline.engine import ClusterProvider
from pipeline.tasks import TaskContext, TaskDefinition, TaskError, StopException
from pipeline.utils.stream_capture import StreamCapturing
from .connector import UpstreamConnector
from .loader import instantiate_task_class


def execute(cluster: ClusterProvider, upstream: UpstreamConnector, taskdef: TaskDefinition) -> None:
    try:
        # create task context
        context = TaskContext(
            cluster  = cluster,
            upstream = upstream,
            taskdef  = taskdef,
        )

        # instantiate & run task
        upstream.run()

        # set up output capturing
        capturing = StreamCapturing(
            on_stdout = lambda x: upstream.log('stdout', x),
            on_stderr = lambda x: upstream.log('stderr', x),
        ) if context.parent else nullcontext()

        # run task within capture context
        with capturing:
            task = instantiate_task_class(taskdef, context)
            result = task.run(**taskdef.inputs)

        # submit result
        upstream.done(result)

    except StopException:
        upstream.stop()

    except TaskError as e:
        # pass subtask errors upstream
        upstream.fail(e.error)
        exit(1)

    except:
        # capture local errors
        error = traceback.format_exc()
        upstream.fail(error)
        exit(1)

    finally:
        # clean exit
        exit(0)