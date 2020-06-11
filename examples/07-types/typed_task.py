from cowait import Task
from cowait.types import Dict, String, Int

TypedResult = Dict({
    'text': String(),
    'number': Int(),
})


class TypedTask(Task):
    async def run(
        self,
        text: str = 'hi',
        number: int = 5,
        **inputs
    ) -> TypedResult:
        return {
            'text': text,
            'number': number
        }
