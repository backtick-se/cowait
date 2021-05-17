---
title: Task Lifecycle Methods
---

Tasks have several methods that can be overridden to customize their behavior. Task lifecycle methods can be used to accomplish more control when implementing for example task inheritance. **However, this functionality is mostly intended for more advanced use cases, and should be avoided if possible.**

Task lifecycle methods are added as class methods on tasks.

## init

Tasks should never override the default python `__init__()` constructor, so the framework provides its own initialization function, ` init()`. It is called before `before()` and must be a synchronous python function.

```python
def init(self) -> None:
    pass
```

## before

The `before()` hook is called immediately before `run()`. All task inputs are passed as a dict, and `before()` can be used to modify the task inputs before the `run()` function is executed.

```python
# inputs can be modified before run() is executed:
async def before(self, inputs: dict) -> dict:
    inputs['new_input'] = 2
    return inputs
```

## after

The `after()` hook can be used to perform actions after the task has finished, such as cleaning up any running child tasks.

```python
async def after(self, inputs: dict) -> None:
    return
```
