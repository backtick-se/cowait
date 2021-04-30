---
title: Remote Procedure Calls (RPC)
---

Advanced task communication

## Introduction

Cowait provides a simple RPC system for advanced communication between tasks. RPC-callable methods are defined directly on the task classes and marked with the `@rpc` decorator. RPC calls can accept any JSON serializable arguments and return any JSON serializable value.

RPC communication can be used to send commands or updates to and from tasks, after they've been created. Defining RPC methods on tasks is a good place to introduce side effects to your tasks.

## Parent to Child RPC

The parent task can call RPC methods on child tasks by invoking methods on the remote task reference object.

1. Define an RPC method on your child task

```python:title=rpc_child.py
from cowait.tasks Task, rpc, sleep

class RpcChild(Task):
    async def run(self):
        # wait forever
        while True:
            await sleep(1)

    @rpc
    async def some_rpc_call(self):
        return 1337
```

2. Call it from the parent, after saving a reference to the child task.

```python:title=rpc_parent.py
from cowait.tasks Task
from rpc_child import RpcChild # your child task

class RpcParent(Task):
    async def run(self):
        child = RpcChild()
        result = await child.some_rpc_call()
        print('RPC result:', result)
        return result
```

## Child to parent RPC

Similarly, child tasks can call RPC methods on their parent task by invoking methods on `self.parent`

1. Have your parent task create the child task.

```python:title=rpc_parent.py
from cowait.tasks import Task, rpc, sleep
from rpc_child import RpcChild

class RpcParent(Task):
    async def run(self):
        self.called = False

        # spawn child and wait for it to make an RPC call:
        child = RpcChild()
        while not self.called:
            await sleep(1)

    @rpc
    async def set_called(self):
        self.called = True
```

2. Call the parent's RPC method through `self.parent`:

```python:title=rpc_child.py
from cowait.tasks import Task

class RpcChild(Task):
    async def run(self):
        # rpc call to parent:
        await self.parent.set_called()
```
