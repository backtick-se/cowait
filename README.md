# Pipeline Bro

## Getting Started

**Requirements:**
- docker
- pipenv


**Installation:**
1. Clone repository
1. `$ pipenv install`
1. `$ pipenv install -e .`
1. `$ pipenv shell`

## Task Development

### First Task

1. **Write a task class.**

```python
# hello.py
from pipeline.tasks import Task

class Hello(Task):
    async def run(self):
        print('Hello World')
```

2. **Build the task image**

In the same folder as `hello.py`, run:

```bash
$ pipeline build
```

3. **Run it locally in Docker.** Make sure you're in a pipenv shell.

In the same folder as `hello.py`, run:

```bash
$ pipeline run hello
```

**Notes**
- `hello` supplied to `pipeline run` is the module name. This module should contain exactly *one* task class. Modules can be single python files or subdirectories with `__init__.py` files.
- Class name does not matter, except for importing to other tasks.

### Task Inputs

*Todo*

### Task Contexts

Tasks live in a *Task Context*. If you have not explicitly defined one, the enclosing folder will be used along with sensible defaults. A task context can be used to package multiple tasks into a single image, customize dockerfiles, and to add extra pip requirements.

*Todo*

### Pushing Tasks

Before you can run tasks on a remote cluster, they must be pushed to a docker registry accessible from the cluster. To do this, you must define a proper image name in the context configuration file.

```yaml
version: 1
pipeline:
    image: backtickse/task-test
```

Once the image url has been configured, you can push the image:

```bash
$ pipeline push
```

## Task Deployment

**Requiurements:**
- Configured kubernetes cluster.
- Docker registry accessible from the cluster.

First, ensure that the image has been pushed to your docker registry.

```
$ pipeline push
```

Run the task with the kubernetes provider:

```bash
$ pipeline run hello --provider kubernetes
```

## Pipeline Development

Changes to the `pipeline/` directory require a rebuild of the base image. You can do this with the provided helper script in the root of the repository:

```bash
$ ./build.sh
```

If you have access to `backtickse` on Docker Hub you can also push it automatically:

```bash
$ ./build.sh --push
```

**Note:** Tasks will have to rebuilt with `pipeline build` for the changes to take effect.
