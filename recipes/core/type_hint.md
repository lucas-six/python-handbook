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

## Advanced

```python
from typing import NoReturn

itertools.chain(...) -> itertools.chain[int]: ...

# `typing.NoReturn`
def func(arg: int, arg2: str = 'a') -> NoReturn:
    raise ValueError
```

## Examples (Recipes)

- [Type Hint for Basic Types](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_basic_type)
- [Type Hint for Literal: `typing.Literal`](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_literal)
- [Type Hint for Union Types: `|`, `typing.Union`, `typing.Optional`](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_union)
- [Type Hint for Any: `typing.Any` and `object`](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_any)
- [Type Hint for type objects](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_type)
- [Type Hint for callable objects](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_callable)
- [Type Hint for Regex](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_regex)
- [Type Hint for socket](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_socket)
- [Type Hint for Constants and Class Attributes: `typing.Final`](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_constant)
- [Type Hint for Class Variables: `typing.ClassVar`](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_class_var)
- [Type Hint for Restricting Inheritance and Overriding: `@typing.final`](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_inheritance)

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
