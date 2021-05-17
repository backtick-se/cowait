---
title: Type system
---

Customizable type checking & input/output serialization

## Built in types

Cowait provides a simple system for defining data types. By annotating task functions and [RPC methods](/docs/tasks/remote-procedure-calls/) with these types, Cowait can perform automatic type checking and serialization/deserialization of complex objects.

```python:title=example.py
from cowait import task
from cowait.types import Dict

TypecheckedDict = Dict({
    'text': str,
    'number': int,
})

@task
def test_task(input_dict: TypecheckedDict) -> int:
    print(input_dict['text'])
    return input_dict['number']
```

### Input Values

If you need to pass any value that is not a simple type (str, int, float, boolean, list, dict), you must annotate the argument. This tells the runtime how to deserialize the object before passing it to the task function. Because the incoming object is serialized, its type can not be automatically inferred.

### Return Values

Type information for result serialization can usually be automatically inferred from the returned object. However, to benefit from type checking, the return type should be annotated on the task function.

## Custom Types

Custom types can be implemented by creating a subclass of `cowait.types.Type` and implementing its `validate()`, `serialize()` and `deserialize()` methods. To register it with the type system, decorate it with the `@TypeAlias()` decorator.

```python:title=datetime_type.py
from cowait.types import Type, TypeAlias

@TypeAlias(datetime)
class DateTime(Type):
    """ Python datetime object serialized as an ISO8601 string """

    def validate(self, value: str, name: str) -> None:
        if isinstance(value, datetime):
            return

        if not isinstance(value, str):
            raise ValueError('Expected ISO8601 datetime')

        datetime.fromisoformat(value)

    def serialize(self, value: datetime) -> str:
        return value.isoformat()

    def deserialize(self, value: str) -> datetime:
        return datetime.fromisoformat(value)
```
