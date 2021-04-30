---
title: Installation
---

Installing Cowait on your local machine.

## Requirements

Cowait is a python library that packages and runs tasks in Docker containers, both locally and on [Kubernetes](https://kubernetes.io/). The base requirements are:

- Python 3.6+
- [Docker](https://docs.docker.com/get-docker/)

## Installation

Cowait is available on [Pypi](https://pypi.org/project/cowait/), you can install it with `pip`:

```shell
python -m pip install cowait
```

We recommend installing in a virtual environment ([virtualenv](https://github.com/pypa/virtualenv)/[venv](https://docs.python.org/3/library/venv.html)) or using a python package manager such as [Poetry](https://python-poetry.org/) or [Pipenv](https://pipenv.pypa.io/en/latest/).

To quickly get started with Cowait, we provide a slim Docker image (~59 MB) that includes the Cowait library. It is based on this [Dockerfile](https://github.com/backtick-se/cowait/blob/master/Dockerfile). Pull the latest image.

```shell
docker pull cowait/task
```

You are now ready for your [first steps](/docs/get-started/first-steps/).

## Development

If you would like to contribute to Cowait, you may install Cowait from source:

1. Clone the repository

```shell
git clone git@github.com:backtick-se/cowait.git
cd cowait
```

2. It is recommended to first setup a virtual env of your choice. A `pyproject.toml` for Poetry is provided for your convenience in the root of the repository.

3. Install the library using pip's editable mode.

```shell
python -m pip install -e .
```

4. Make changes to the library. Note that changes to the `cowait/` directory require a rebuild of the base image. You can do this with the provided helper script in the root of the repository:

```shell
./build.sh
```

5. Note that tasks you use to test your new feature or bug-fix will have to be rebuilt with `cowait build` for the changes to take effect.
