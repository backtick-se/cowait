---
title: Dask
---

Automatically deploy Dask clusters for your projects with a single line of code.

**WARNING**: This is very experimental and currently just a proof of concept. Proceed at your own risk.

## Defining and running a Dask Cluster

Dask clusters can be created using the `DaskCluster` task.

```python:title=dask_cluster.py
from cowait.tasks import Task
from cowait.tasks.dask import DaskCluster

class YourDaskJob(Task):
    async def run(self, dask, inputs**):
        cluster = DaskCluster(workers=5)
        client = await cluster.get_client()
        # dask client ready to use!

        def square(x):
            return x ** 2

        def neg(x):
            return -x

        A = client.map(square, range(10))
        B = client.map(neg, A)

        total = client.submit(sum, B)
        result = total.result()

        print(result)

        return result
```

Run it:

```shell
cowait run dask_cluster
```

## DaskCluster RPC Methods

The DaskCluster task will automatically set up a Dask scheduler and a set of workers. It provides a number of RPC methods for controlling your cluster, summarized below:

### `cowait.tasks.dask.DaskCluster`

| RPC Method            |                                  Description |
| --------------------- | -------------------------------------------: |
| `get_workers()`       |      Get informations about all Dask workers |
| `scale(workers: int)` | Can be used to scale up or down your cluster |
| `get_scheduler_uri()` |               Returns the Dask scheduler URI |
| `get_client()`        |                      Returns the dask client |
| `teardown()`          |     Stop your Dask cluster task from running |

See [github](https://github.com/backtick-se/cowait/blob/master/cowait/tasks/dask/cluster.py) for full reference.

**WARNING**: This is very experimental and currently just a proof of concept.
