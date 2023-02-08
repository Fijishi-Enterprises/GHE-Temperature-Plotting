from functools import partial
from typing import Callable

class Example:

    def __init__(self, a: int):
        self.a = a

    def calc(self, b: int) -> int:
        return self.a + b

    def add(self, c: int):
        self.a += c


exa = Example(1)
func = partial(exa.calc, 2)

exa2 = Example(1)
func2 = partial(exa2.calc, 2)
assert func.func.__func__.__name__ == func2.func.__func__.__name__
assert func.args == func2.args
assert func.keywords == func2.keywords

print(func())

func = partial(exa.add, 5)
func()
print(exa.a)