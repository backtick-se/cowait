---
title: Spark
---

Automatically deploy Spark clusters for your projects with a single line of code.

**WARNING**: This is very experimental and currently just a proof of concept. Proceed at your own risk.

## Defining and running a Spark Cluster

This requires you to manually first install `pyspark`. Add it to your `requirements.txt` (or install it in your Dockerfile).

Spark clusters can be created using the `SparkCluster` task.

```python:title=spark_cluster.py
from cowait.tasks import Task
from cowait.tasks.spark import SparkCluster
from pyspark.sql import SparkSession

class YourSparkJob(Task):
    async def run(self, inputs**):
        cluster = SparkCluster(workers=5)
        conf = await cluster.get_config()

        # create spark session
        session = SparkSession.builder \
            .config(conf=conf) \
            .getOrCreate()

        # use your Spark SQL session!

        # you can also scale the cluster at will:
        await cluster.scale(workers=2)

        return "Spark job exited"
```

Run it:

```shell
cowait run Spark_cluster
```

## SparkCluster RPC Methods

The SparkCluster task will automatically set up a Spark scheduler and a set of workers. It provides a number of RPC methods for controlling your cluster, summarized below:

### `cowait.tasks.Spark.SparkCluster`

| RPC Method            |                                  Description |
| --------------------- | -------------------------------------------: |
| `get_workers()`       |     Get informations about all Spark workers |
| `scale(workers: int)` | Can be used to scale up or down your cluster |
| `get_config()`        |              Returns the Spark configuration |
| `teardown()`          |    Stop your Spark cluster task from running |

See [github](https://github.com/backtick-se/cowait/blob/master/cowait/tasks/spark/cluster.py) for full reference.

**WARNING**: This is very experimental and currently just a proof of concept.
