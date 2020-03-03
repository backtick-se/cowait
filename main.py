"""
Task worker entry point.

Environment:
    TASK_CLUSTER (json): JSON-serialized ClusterProvider
    TASK_DEFINITION (json): JSON-serialized TaskDefinition
"""
import os
import asyncio
import traceback
from pipeline.worker import execute, \
    env_get_cluster_provider, \
    env_get_task_definition


async def main():
    # unpack cluster provider
    cluster = env_get_cluster_provider()

    # unpack task definition
    taskdef = env_get_task_definition()

    # execute task
    try:
        await execute(cluster, taskdef)

    except Exception:
        print(f'!! {taskdef.id} failed with error:')
        traceback.print_exc()
        os._exit(1)

    # clean exit
    # print(f'~~ {taskdef.id} completed')
    os._exit(0)

if __name__ == '__main__':
    asyncio.run(main())
