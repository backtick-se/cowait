# cowait

[![Actions Status](https://github.com/backtick-se/cowait/workflows/Tests/badge.svg)](https://github.com/backtick-se/cowait/actions)
[![PyPI version](https://img.shields.io/pypi/v/cowait.svg)](https://pypi.org/project/cowait/)
[![](https://img.shields.io/static/v1?label=docs&message=gitbook&color=blue)](http://docs.cowait.io/)
[![Website shields.io](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](http://cowait.io/)

Cowait is a framework for creating containerized distributed applications with asynchronous Python. Containerized functions, called *Tasks*, can run locally in Docker or on remote Kubernetes clusters. The intention is to build a novel type of workflow engine that offers maximum flexibility while also requiring minimal setup and configuration. However, Cowait can be used to easily build many types of distributed applications.

Check out the documentation at https://docs.cowait.io/

## Notice

Cowait is still in fairly early development. We invite you to try it out and gladly accept your feedback and contributions, but please be aware that breaking API changes may be introduced. Or things might straight up break occasionally.

## Getting Started

**Requirements**
- docker
- python 3.6+

**Installation**

```bash
$ pip install cowait
```

## Task Development

### First Task

1. **Write a task class.**

```python
# hello.py
from cowait import task

@task
async def Hello():
    print('Hello World')
```

2. **Build the task image**

All files within the current directory is bundled into a task image.

In the same folder as `hello.py`, run:

```bash
$ cowait build
```

3. **Run it locally**

To run a task, pass the name of the module containing the task to `cowait run`. In the same folder as `hello.py`, run:

```bash
$ cowait run hello
```

**Notes**
- `hello` supplied to `cowait run` is the module name. This module should contain exactly *one* task class. Modules can be single python files or subdirectories with `__init__.py` files.
- Function/class name of the task does not matter when running, only when importing and running from other tasks.

### Subtasks, Arguments & Return Values

Tasks can create subtasks, by importing and calling other tasks as if they were asynchronous python functions. Subtasks accept arguments and return results. Arguments and results must be JSON serializable.

```python
from cowait import task
from some_subtask import SomeSubtask

@task
async def MainTask(some_input: int = 5):
    subtask_result = await SomeSubtask(custom_argument = 'hello')
    print('Subtask finished with result', subtask_result)
    return 'ok'
```

### Task Contexts

Tasks belong to a *Task Context*. If you have not explicitly defined one by creating a `cowait.yml` file, the enclosing folder will be used along with sensible defaults. Everything in the task context directory will be bundled into the final task image. A task context can be used to package multiple tasks into a single image, customize dockerfiles, and to add extra pip requirements.

### Pushing Task Images

Before you can run tasks on a remote cluster, they must be pushed to a docker registry accessible from the cluster. To do this, you must define a proper image name in the context configuration file.

```yaml
version: 1
cowait:
    image: cowait/task-test
```

Once the image url has been configured, you can push the image:

```bash
$ cowait push
```

## Cluster Deployment

**Requiurements**
- Configured kubernetes cluster context.
- Docker registry accessible from the cluster.

First, ensure that the image has been pushed to your docker registry.

```
$ cowait push
```

**Kubernetes Configuration**

Before you can run tasks on a kubernetes cluster, you need to apply some RBAC rules to allow pods to interact with other pods. A sample configuration is provided in `k8setup.yml`, which will allow pods owned by the default service account to create, list and destroy other pods.

Tasks will run on your default configured cluster (the one returned by `$ kubectl config current-context`).

**Running Tasks**

Once the cluster has been configured, simply run a task with the kubernetes cluster provider:

```bash
$ cowait run hello --cluster kubernetes
```

## Development

**Requirements**
- docker
- python 3.6+
- pipenv/virtualenv (optional)

**Installation**

1. Clone repository
1. `$ python3 -m pip install -e .`

Changes to the `cowait/` directory require a rebuild of the base image. You can do this with the provided helper script in the root of the repository:

```bash
$ ./build.sh
```

If you have access to `cowait` on Docker Hub you can also push it automatically:

```bash
$ ./build.sh --push
```

**Note:** Tasks will have to rebuilt with `cowait build` for the changes to take effect.
