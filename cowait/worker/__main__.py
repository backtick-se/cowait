"""
Task worker entry point.

Environment:
    COWAIT_CLUSTER (json): JSON-serialized ClusterProvider
    COWAIT_TASK (json): JSON-serialized TaskDefinition
"""
import os
import sys
import json
import asyncio
import traceback
import nest_asyncio
from datetime import datetime
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
        await asyncio.sleep(0.1)

    except Exception:
        print(json.dumps({
            'id': taskdef.id,
            'type': TASK_FAIL,
            'error': traceback.format_exc(),
            'ts': datetime.now().isoformat(),
        }))
        os._exit(1)

    os._exit(0)


if __name__ == "__main__":
    # apply a patch that allows nested asyncio loops
    nest_asyncio.apply()

    # run asyncio loop
    asyncio.run(main())

else:
    raise ImportError('Worker.__main__ is not meant to be imported')
