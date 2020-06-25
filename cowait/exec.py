"""
Task worker entry point.

Environment:
    TASK_CLUSTER (json): JSON-serialized ClusterProvider
    TASK_DEFINITION (json): JSON-serialized TaskDefinition
"""
import os
import sys
import json
import asyncio
import traceback
from cowait.tasks.messages import TASK_FAIL
from cowait.worker import execute, \
    env_get_cluster_provider, \
    env_get_task_definition


async def main():
    # add working directory to pythonpath
    sys.path += [os.getcwd()]

    # unpack cluster provider
    cluster = env_get_cluster_provider()

    # unpack task definition
    taskdef = env_get_task_definition()

    # execute task
    try:
        await execute(cluster, taskdef)

    except Exception:
        print(json.dumps({
            'id': taskdef.id,
            'type': TASK_FAIL,
            'error': traceback.format_exc(),
        }))
        os._exit(1)

    os._exit(0)

# run asyncio loop
asyncio.run(main())
