---
title: First steps
---

Your first steps into the world of Cowait.

## Overview

Cowait organizes code into Tasks. A Task is essentially nothing more than a function, and just like your typical function, it can accept input arguments and return values. Similarly they may also invoke other tasks, with one key difference: a call to another task will be intercepted by the Cowait runtime and executed in a separate container — potentially on a different machine.

## Tasks

The basic unit of execution in Cowait is the Task. Tasks can be implemented either as simple functions, or classes deriving from `cowait.Task`.

### Creating a task

Create a new folder called `my-project` and a python file called `hello.py`. We assume you've managed to [install Cowait](/docs/get-started/installation/).

```
my-project/
  └── hello.py
```

```python:title=hello.py
from cowait import task

# function style
@task
async def Hello():
    print('Hello World')
```

```python
from cowait import Task

# class style
class Hello(Task):
    async def run(self):
        print('Hello World')
```

### Running the task

You can now run your task. Unlike Python code that you execute directly, this will run inside a Docker Container. You can run your task like so:

```shell
cd my-project
cowait run hello
```

You should see something like this:

```
-- TASK ---------------------------------------------
   task:       "hello-plapdnoy"
   cluster:    "docker" {  }
   image:      "cowait/task"
   volumes:    { /var/task: { bind: { src: "/Users/cowait-demo/my-project/demo", mode: "rw" } } }
-- TASK OUTPUT --------------------------------------
15:53:28 hello * started with {  }
15:53:28 hello = returned null
15:53:28 hello   Hello World
-----------------------------------------------------
```

### Volume Mounts

Behind the scenes, Cowait uses Docker Volume Mounts to speed up local development. Notice that you did not have to build anything. This is because you pulled the base Cowait image in the installation process.

If you would like to build your Docker image with your added code, simply run:

```shell
cowait build
```

## Inputs & Outputs

Cowait tasks can accept inputs and return outputs.

```python:title=hello.py
import asyncio
from cowait import task

@task
async def Hello(name: str, **inputs):
    print("Hello", name)

    return {
        "hello": name,
    }
```

- Inputs that you do not define explicitly in the function signature are passed in `**inputs`.
- You can return whatever you would like, as long as it can be serialized. This work out of the box with python types (`str`, `int`, `float`, `boolean`, `list`, `dict`). You can also [create your own types](/docs/tasks/type-system/)
- The Cowait CLI allows you to pass inputs when running your task:

```shell
cowait run hello --input name=world
```

## Notes

- `hello` supplied to `cowait run` is the python module name. This module should contain exactly one task class. Modules can be single python files or subdirectories with **init**.py files.
- The actual function/class name of the task does not matter when running from the CLI, only when importing and executing tasks from python.
