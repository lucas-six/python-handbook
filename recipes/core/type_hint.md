# Type Hint

An *annotation* that specifies the expected type for:

- variable or class attribute
(New in Python *3.6*,
See [PEP 526](https://peps.python.org/pep-0526/ "PEP 526 - Syntax for Variable Annotations"))
- function/method parameter and return type
(See [PEP 3107](https://peps.python.org/pep-3107/ "PEP 3107 - Function Annotations"))

## Use Case

- static type analysis tools
- aid IDEs with code completion and refactoring

## Basic Type

```python
x1: int = 1

x2: str  # no initial value!

x3: list[int] = []  # a list of integers

x4: dict[int, str] = {}  # a dictionary of {int: str}

x5_1: tuple[int, str] = (0, 'a') # a tuple of (int, str)
x5_2: tuple[int, ...]  # a tuple of integers with any size

x6: set[int] = set()  # a set of integers

x7: bool = True

x8: float = 1.5  # int or float

def f(arg: int) -> int: ...
```

**NOTE**: *`typing.List`*, *`typing.Dict`*, *`typing.Tuple`*, *`typing.Set`*, *`typing.FrozenSet`*
are deprecated since Python *3.9*, using standard types instead.
See [PEP 585](https://peps.python.org/pep-0585/ "PEP 585 - Type Hinting Generics In Standard Collections")

## `Any` vs `object`

```python
from typing import Any

x: Any = None
x = 1  # ok
x = 'a'  # ok
s: str = ''
s = a  # ok

x: object = None
x = 1  # ok
x = 'a'  # ok
s: str = ''
s = a  # type check fails

def f(arg: Any):
    arg.method()  # ok
def f(arg: object):
    arg.method()  # type check fails

def f1() -> Any: return 1  # ok
def f2() -> object: return 1  # ok
s: str = ''
s = f1()  # ok
s = f2()  # type check fails

def f1(arg: Any): pass
def f2(arg: object): pass
f1(1)  # ok
f1('s')  # ok
f2(1)  # ok
f1('s')  # ok
```

```python
from typing import Any

x1: list[Any] = []  # a list of any type
x2: dict[int, Any] = {}  # a dictionary of {int: any type}
x3: tuple[Any, ...]  # tuple of items with any type and any size
```

## Advanced

```python
# PEP 604, Allow writing union types as X | Y
from __future__ import annotations

from typing import Literal, ItemsView, Type, NoReturn

x1: int | str  # Union[int, str]: int or str

x2: int | None  # Optional[int] == Union[int, None]
# x2: Optional[int, str]  # fails: Only one argument(type) accepted.

# Introduced since Python 3.8, See PEP 586.
x3: Literal[1, 2, True, False]  # one of 1, 2, True, False

# dict.items()
x4: dict[int, str] = {1: '1'}
x4.items() -> ItemsView[int, str]: ...

itertools.chain(...) -> itertools.chain[int]: ...

# socket
# Removed usage of `socket.SocketType`
# `SocketType` is an alias for the private `_socket.socket` class, a superclass of `socket.socket`.
# It is better to just always use `socket.socket` in types.
# See https://bugs.python.org/issue44261 and python/typeshed#5545 for some context.
#   See https://github.com/python/typeshed/pull/5545
#   See https://github.com/agronholm/anyio/pull/302
import socket
x5: socket.socket = socket.socket(...)
x5: socket.SocketKind = socket.SOCK_STREAM  # or `socket.SOCK_DGRAM`
x5: socket.AddressFamily = socket.AF_INET  # or `socket.AF_INET6`

# callable object
# Since Python 3.9, `typing.Callable` is deprecated, using `collections.abc.Callable` instead.
# See PEP 585 - Type Hinting Generics In Standard Collections
#   https://peps.python.org/pep-0585/
from collections.abc import Callable
Callable[[Arg1Type, Arg2Type], ReturnType]
Callable[[...], ReturnType]  # variable arguements

# type object
class C: pass
c: Type[C] = C
o: Type[object]
e: Type[BaseException]

# regex pattern object
# Since Python 3.9, `typing.Pattern` is deprecated, using `re.Pattern` instead,
# and `typing.Match` is replaced with `re.Match`.
# See PEP 585 - Type Hinting Generics In Standard Collections
#   https://peps.python.org/pep-0585/
import re
p: re.Pattern[str] = re.compile(r'xxx')
p: re.Pattern[bytes] = re.compile(rb'xxx')
m: re.Match[str] = re.match(r'xxx', 'xxx')
m: re.Match[bytes] = re.match(rb'xxx', b'xxx')

# `typing.NoReturn`
def func(arg: int, arg2: str = 'a') -> NoReturn:
    raise ValueError
```

## `Final`

New in Python *3.8*,
see [PEP 591](https://peps.python.org/pep-0591/ "PEP 591 - Adding a final qualifier to typing").

```python
from typing import Final


# constant
MAX_SIZE: Final = 1024
MAX_SIZE: Final[int] = 1024

# class attribute
class Base:
    ATTR: Final[int] = 10

class Sub(Base):
    ATTR = 1  # Error reported by type checker

class ImmutablePoint:
    x: Final[int]
    y: Final[int]  # Error: final attribute without an initializer

    def __init__(self) -> None:
        self.x = 1  # Good
```

## `@final`

New in Python *3.8*,
see [PEP 591](https://peps.python.org/pep-0591/ "PEP 591 - Adding a final qualifier to typing").

The **`@typing.final`** decorator is used to restrict the use of *inheritance* and *overriding*.

```python
from typing import final

@final
class Base:
    pass

class Derived(Base):  # Error: Cannot inherit from final class "Base"
    pass
```

and

```python
from typing import final

class Base:
    @final
    def done(self) -> None:
        ...

class Sub(Base):
    def done(self) -> None:  # Error: Cannot override final attribute "done"
                             # (previously declared in base class "Base")
        ...
```

The method decorator version may be used with all of *instance methods*, *class methods*,
*static methods*, and *properties*.

## `ClassVar`

Special type construct to mark **class variables**.

```python
from typing import ClassVar

class C:
    cls_attr: ClassVar[dict[str, int]] = {}   # class variable
    ins_attr: int = 10                        # instance variable
```

## Typeshed Stub

See [typeshed](https://github.com/python/typeshed) and [mypy](https://github.com/python/mypy).

```bash
pip install mypy
pip install mypy-xxx
```

## Backward Compability

See [typing-extensions](https://pypi.org/project/typing-extensions/ "PyPI - typing-extensions").

```bash
pip install typing-extensions
```

## `typing.get_type_hints()`

Type hints of global variables, class attributes, and functions, but not local variables,
can be accessed using **`typing.get_type_hints()`**.

```python
typing.get_type_hints(obj, globalns=None, localns=None, include_extras=False) -> dict
```

Return a dictionary containing type hints for a function, method, module or class object.

This is often the same as *`obj.__annotations__`*.
In addition, forward references encoded as string literals
are handled by evaluating them in `globalns` and `localns` namespaces.

## References

- [Python - `typing` module](https://docs.python.org/3/library/typing.html)
- [PEP 526 - Syntax for Variable Annotations](https://peps.python.org/pep-0526/)
- [PEP 3107 – Function Annotations](https://peps.python.org/pep-3107/)
- [PEP 484 – Type Hints](https://peps.python.org/pep-0484/)
- [PEP 483 – The Theory of Type Hints](https://peps.python.org/pep-0483/)
- [PEP 591 – Adding a final qualifier to typing](https://peps.python.org/pep-0591/)
- [PEP 585 – Type Hinting Generics In Standard Collections](https://peps.python.org/pep-0585/)
- [PEP 586 – Literal Types](https://peps.python.org/pep-0586/)
- [PEP 563 – Postponed Evaluation of Annotations](https://peps.python.org/pep-0563/)
- [PEP 604 – Allow writing union types as `X | Y`](https://peps.python.org/pep-0604/)
- [GitHub - `typeshed`](https://github.com/python/typeshed)
- [GitHub - `mypy`](https://github.com/python/mypy).
- [PyPI - `typing-extensions` package](https://pypi.org/project/typing-extensions/)
