---
title: Tests
---

## Overview

Cowait supports testing of tasks, asynchronous code and library code. Cowait uses [pytest](https://docs.pytest.org/en/6.2.x/).

Writing tests for your asynchronous tasks is simple. The cowait test runner will spawn a task(!) that allows you to perform assertions on your code and other tasks.

Good to know:

- For tests to be picked up by the test runner, make sure to prefix your test files with `test_`.
- Cowait will run **one** task that will execute all your tests, even if they're in different files.
- Cowait will create real instances of your tasks if you create them from your test code.
- Of course, you're free to import library code in the Cowait test runner to unit test smaller building blocks and functions.

## Black box task testing

In this example, we have added a `test_sleep.py` file to our project:

```
my-project/
  ├── cowait.yml
  ├── hello.py
  ├── parallel.py
  ├── requirements.txt
  ├── sleep.py
  └── test_sleep.py
```

```python:title=test_sleep.py
from sleep import Sleep

async def test_sleep():
    result = await Sleep(duration=1)

    assert result == {
        'duration': 1,
    }
```

To run the test, use the Cowait CLI:

```shell
cowait test
```

## Testing functions and library code

Of course, you can import your functions and library modules in the test task and write tests like you normally would (as long as the code is packaged into the same Docker image). Let's say you have a simple function that doesn't run any async code that you would like to test as well.

```python:title=sleep.py
import asyncio
from cowait import task

def add(a: int, b: int):
  return a + b

@task
async def Sleep(duration: int = 5):
    for i in range(duration):
      await asyncio.sleep(1) # blocking
      print("slept", i + 1)

    return {
        "duration": duration,
    }
```

You could simply import it in your test file and perform assertions like you normally would.

```python:title=test_sleep.py
from sleep import Sleep, add

def test_add():
    assert add(1, 2) == 3

async def test_sleep():
    result = await Sleep(duration=1)
    assert result == {
        'duration': 1,
    }
```

```bash
============================= test session starts ==============================
platform linux -- Python 3.7.10, pytest-6.2.3, py-1.10.0, pluggy-0.13.1
rootdir: /var/task, configfile: ../cowait/pytest.ini
plugins: cov-2.11.1, alt-pytest-asyncio-0.5.4, sugar-0.9.4
collected 2 items

test_sleep.py ..                                                         [100%]

============================== 2 passed in 4.19s ===============================
```

Moreover, you are free to create multiple files (`test_sleep.py`, `test_sleep2.py`). Cowait will pick up and run all defined tests. Tests will run in one Cowait task.

## Testing reads and write of datasets

In this example we assume you are doing some transformations on a dataset on `s3`. Let's assume your task takes a fair amount of time, and it would be sad to see it fail after running for 4 hours. You have decided to solve this problem by writing a test for your task.

Let's say your preprocessing task looks something like this:

```python:title=preprocess.py
from cowait import task

@task
async def Preprocess(dataset_url='s3://big-data-set'):
    #
    # data reading and data transformation code
    # ...

    return {
      # New output location. We use self.task.id to
      # generate a unique identifier for this dataset.
      new_location: f's3://preprocessed/{self.task.id}'
    }
```

Before investing time to run the big job, let's make sure everything works (inputs, reading data code, outputs, writing data) with a smaller dataset:

```python:title=test_preprocess.py
from preprocess import Preprocess

async def test_preprocess():
    # define the task so we can grab the task id.
    # The task will start executing in the background
    task = Preprocess(dataset_url='s3://small-data-set')

    # Wait for the task to finish
    result = await task

    assert result == {
      new_location: f's3://preprocesssed/{task.id}'
    }
    # ...
    # further assertions like data written, rows, size, columns or whatever
    # ...
```

```shell
cowait test
```

Of course, the above example would read data to your local machine. For very small datasets, this is probably fine, but you probably want to test on medium or large datasets as well, in a production cluster environment. For this use case, Cowait provides the CLI argument `--cluster` to `cowait test` that allows you to run your [tests on Kubernetes](/docs/kubernetes/testing/).
