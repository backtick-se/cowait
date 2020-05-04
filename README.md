# cowait

Cowait is a framework for creating containerized workflows with asynchronous Python. Tasks can be run locally with Docker or on a kubernetes cluster. The goal is complete flexibility with minimal setup and configuration.

Docs: http://docs.cowait.io/

## Getting Started

**Requirements**
- docker
- python 3.6+

**Installation**

```bash
$ pip3 install cowait
```

## Task Development

### First Task

1. **Write a task class.**

```python
# hello.py
from cowait import Task

class Hello(Task):
    async def run(self):
        print('Hello World')
```

2. **Build the task image**

All files within a folder is bundled into a task image.

In the same folder as `hello.py`, run:

```bash
$ cowait build
```

3. **Run it locally in Docker.** Make sure you're in a pipenv shell.

In the same folder as `hello.py`, run:

```bash
$ cowait run hello
```

**Notes**
- `hello` supplied to `cowait run` is the module name. This module should contain exactly *one* task class. Modules can be single python files or subdirectories with `__init__.py` files.
- Class name does not matter, except for importing to other tasks.

### Subtasks, Arguments & Return Values

Tasks can create subtasks, by importing and calling other tasks as if they were asynchronous python functions. Subtasks accept arguments and return results. Arguments and results must be JSON serializable.

```python
from cowait import Task
from some_subtask import SomeSubtask

class MainTask(Task):
    async def run(self, **inputs):
        subtask_result = await SomeSubtask(custom_argument = 'hello')
        print('Subtask finished with result', subtask_result)
        return 'ok'
```

### Task Contexts

Tasks live in a *Task Context*. If you have not explicitly defined one, the enclosing folder will be used along with sensible defaults. A task context can be used to package multiple tasks into a single image, customize dockerfiles, and to add extra pip requirements.

*Todo*

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

**Running Tasks**

Once the cluster has been configured, simply run a task with the kubernetes provider:

```bash
$ cowait run hello --provider kubernetes
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
