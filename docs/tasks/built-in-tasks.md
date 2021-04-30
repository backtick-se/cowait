---
title: Built in tasks
---

Some useful library tasks that can simplify your life.

## ShellTask

ShellTask can be used to run any shell command. `stdout` and `stderr` is forwarded to the task log.

### `cowait.tasks.shell.ShellTask`

| Input   |  Type  |              Description |
| ------- | :----: | -----------------------: |
| command | string | Shell command to execute |
| env     |  dict  |              Environment |

**Returns**: shell command return code (integer)

```python:title=example-ls.py
from cowait.tasks.shell import ShellTask

@task
async def MyTask():
    await ShellTask(command='ls')
```

```shell
# Example using the CLI
cowait run cowait.tasks.shell --input command=ls
```

## ContainerTask

`ContainerTask` can be used to launch and monitor any Docker container. This can be useful for setting up side-car containers. Container logs are forwarded to the task log.

### `cowait.tasks.container.ContainerTask`

| Input  |    Type    |           Description |
| ------ | :--------: | --------------------: |
| name   |   string   |             Task Name |
| image  |   string   |     Docker image name |
| env    |    dict    | Environment variables |
| routes | Route Dict |                       |
| ports  | Port Dict  |                       |
| cpu    |   string   |        CPU allocation |
| memory |   string   |     Memory allocation |

```python:title=mongo.py
from cowait.tasks.container import ContainerTask

@task
async def MyTask():
    await ContainerTask(
      name="mongodb-task"
      image="mongo"
    )
```

```shell
# Example using the CLI
cowait run cowait.tasks.container --input name="mongodb-task" -i image=mongo
```
