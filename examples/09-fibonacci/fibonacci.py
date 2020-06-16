from cowait import task


@task
async def Fibonacci(n: int) -> int:
    if n < 2:
        return 1

    a = Fibonacci(n=n-2)
    b = Fibonacci(n=n-1)
    return (await a) + (await b)
