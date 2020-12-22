![cowait](/assets/cowait_bg.png)
# cowait

[![Actions Status](https://github.com/backtick-se/cowait/workflows/Tests/badge.svg)](https://github.com/backtick-se/cowait/actions)
[![PyPI version](https://img.shields.io/pypi/v/cowait.svg)](https://pypi.org/project/cowait/)
[![](https://img.shields.io/static/v1?label=docs&message=gitbook&color=blue)](http://docs.cowait.io/)
[![Website shields.io](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](http://cowait.io/)
[![](https://img.shields.io/badge/chat-slack-blueviolet)](https://slack.cowait.io)

Cowait is a framework for creating containerized distributed applications with asynchronous Python. Containerized functions, called *Tasks*, can run locally in Docker or on remote Kubernetes clusters. The intention is to build a novel type of workflow engine that offers maximum flexibility while also requiring minimal setup and configuration. Because of the loose definition of what a Task could be, and the integration with Docker & Kubernetes, Cowait can be used to easily build many types of distributed applications.

Check out the documentation at https://docs.cowait.io/

## Notice

Cowait is still in fairly early development. We invite you to try it out and gladly accept your feedback and contributions, but please be aware that breaking API changes may be introduced.

## Community

Join the Cowait development Slack channel! 

Get your invite at https://slack.cowait.io

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

1. **Write a task.**

Tasks can be written as decorated functions or subclasses of `cowait.Task`. The easiest way is to write a decorated function:

```python
# hello.py
from cowait import task

@task
async def Hello():
    print('Hello World')
```

2. **Build a task image**

All files within the current directory is bundled into a docker image.

In the same folder as `hello.py`, run:

```bash
$ cowait build
```

3. **Run it locally**

To run a task, pass the name of the module import name to `cowait run`. Since our task code lives in `hello.py`, the module name will be `hello`. In the same folder as `hello.py`, run:

```bash
$ cowait run hello
```

**Notes**
- `hello` supplied to `cowait run` is the python module name. This module should contain exactly *one* task class. Modules can be single python files or subdirectories with `__init__.py` files.
- The actual function/class name of the task does not matter when running from the CLI, only when importing and executing tasks from python.

### Subtasks, Arguments & Return Values

Tasks can execute subtasks by importing and calling asynchronously using the `await` keyword. Subtasks accept named arguments and return results, much like regular functions.

Suppose we have a `Square` task that squares an integer.

```python
# square.py
from cowait import task

@task
async def Square(number: int) -> int:
    return number ** 2
```

We can import it to another task and execute it:

```python
# main.py
from cowait import task
from square import Square

@task
async def MainTask():
    value = 22
    squared = await Square(number=22)
    print(f'{value} squared is {squared}!')
```

### Task Contexts

A task context is a directory containing a `cowait.yml` configuration file. This directory will act as the root of a project, and everything within this folder is copied into the resulting docker image during the build step. If you have not created a `cowait.yml` file, the current working directory (when executing `cowait build`) will be used.

** Example Task Context **
```
 /var/stuff/my_cowait_project
   src/
     library.py
   cowait.yml
   requirements.txt
   task1.py
   task2.py
```

In this case, `/var/stuff/my_cowait_project` will be the context directory.

### Pushing Task Images

Before you can run tasks on a Kubernetes cluster, they must be pushed to a docker registry that is accessible from the cluster. To do this, you must define a proper image name in the context configuration file.

```yaml
version: 1
cowait:
    image: docker.io/username/cowait-task
```

Once the full image name has been configured, you can push the image using `cowait push`:

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

Before you can run tasks on a kubernetes cluster, you need a service account with permissions to create/list pods. A sample configuration is provided in `k8setup.yml`, which will allow any pods owned by the default service account to create, list and destroy other pods. 

For detailed information about running on Kubernetes, see the [documentation](https://docs.cowait.io/kubernetes/setup]).

**Running Tasks**

To run tasks on a remote cluster, pass the cluster name using the `--cluster` option to `cowait run`. 

Cowait comes with a predefined cluster called `kubernetes` which always refers to your default configured cluster (the one returned by `$ kubectl config current-context`).

```bash
$ cowait run docker.io/username/cowait-task --cluster kubernetes
```

## Development

**Requirements**
- docker
- python 3.6+
- poetry (recommended)

**Installation**

1. Clone repository
1. `$ python3 -m pip install -e .`

Changes to the `cowait/` directory require a rebuild of the base image. You can do this with the provided helper script in the root of the repository:

```bash
$ ./build.sh
```

**Note:** Tasks will have to rebuilt with `cowait build` for the changes to take effect.
