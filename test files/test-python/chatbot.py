async def main(query: str) -> str:
    for i in range(4):
        print(i)
    return "main function imported and executed..."

def some_func1() -> str:
    return "some_func1 triggered, this should not execute!"