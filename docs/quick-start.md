---
title: Quick Start
---

This quick start assumes you have intermediate programming skills and are familiar with python, asyncio and Docker.

## Cowait quick start

1. Install cowait

```shell
pip install cowait
```

2. Pull the base Cowait image. Don't worry - you can use your own Dockerfile if you want to.

```shell
docker pull cowait/task
```

3. Create a new Cowait task, `hello.py`:

```python:title=hello.py
import asyncio
from cowait import task

@task
async def Hello():
    print("Hello World")

```

4. Run your Cowait task, this spins up a new docker container.

```shell
cowait run hello
```

5. Start the Cowait UI

```shell
cowait agent
```

You can visit the UI at `http://localhost:1339`

6. If you run your task again, it should show up in the UI.

## Asyncio, Inputs & Outputs

1. Create a new file `sleep.py`.

Cowait tasks are defined with the `async` keyword. This allows us to wait for other tasks in an asynchronous fashion, or to use basic features from `asyncio`, like `sleep(n)`.

```python:title=sleep.py
import asyncio
from cowait import task

@task
async def Sleep():
    for i in range(5):
      await asyncio.sleep(1)
      print("slept", i + 1)

```

2. Modify the Sleep task to take duration as an input. Also return how long it slept.

   - Inputs that you do not define explicitly in the function signature are passed in `**inputs`.
   - Outputs can be consumed by other tasks or systems.

```python:title=sleep.py
import asyncio
from cowait import task

@task
async def Sleep(duration: int = 5, **inputs):
    for i in range(duration):
        await asyncio.sleep(1)
        print("slept", i + 1)

    return {
        "duration": duration,
    }
```

3. The Cowait CLI allows you to pass inputs when running your task:

```shell
cowait run sleep --input duration=7
```

## Parallel Tasks

One of the core features of Cowait is its simple interface to paralellize work on multiple containers. Let's add a new task that spawns multiple `Sleep` tasks in parallel:

```python:title=parallel.py
import asyncio
from cowait import task, join
from sleep import Sleep

@task
async def Parallel():
    tasks = [Sleep(duration=5), Sleep(duration=5)]

    result = await join(tasks)

    return result

```

```shell
cowait run parallel
```

Nice! Here's an illustration of what you just ran, in terms of containers:

![Parallel Docker Illustration](./images/parallel_tasks_docker.svg)

You will note that the program doesn't run for precisely 5 seconds, and that the `Sleep` containers may start / exit at different times (however `parallel` will block until both are done). This is because there is some overhead in the underlying docker engine to create and spawn new containers for the tasks.
