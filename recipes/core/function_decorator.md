# Function (Method) Decorator

## Syntactic Sugar

```python
@decorator
def func(arg1, arg2, ...):
    pass
```

semantically equivalent:

```python
def func(arg1, arg2, ...):
    pass
f = decorator(func)(arg1, arg2, ...)
```

## Multiple Decorators

```python
@dec2
@dec1
def func(arg1, arg2, ...):
    pass
```

equivalent to:

```python
def func(arg1, arg2, ...):
    pass
func = dec2(dec1(func))(arg1, arg2, ...)
```

## Examples (Recipes)

- [Create Function Decorator Without Argument](https://leven-cn.github.io/python-cookbook/recipes/core/function_decorator_no_args)
- [Create Function Decorator With Required Arguments](https://leven-cn.github.io/python-cookbook/recipes/core/function_decorator_args_required)
- [Create Function Decorator With Optional Arguments](https://leven-cn.github.io/python-cookbook/recipes/core/function_decorator_args_optional)

## Usage: Act on Function

```python
def decorator(*_args, **_kwargs):

    def wrapper(_func):
        """wrapper function."""
        print(f'run wrapper: {_args}, {_kwargs}')
        return _func

    print(f'run decorator: {_args}, {_kwargs}')
    return wrapper

@decorator(1)
def func(*args, **kwargs):
    """original function."""
    print(f'run func: {args}, {kwargs}')


run decorator: (1,), {}
run wrapper: (1,), {}
>>> func()
run func: (), {}
>>> func(2)
run func: (2,), {}
```

## `@functools.wraps` Implementation Detail

```python
from functools import partial, update_wrapper

WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__qualname__', '__doc__', '__annotations__')
WRAPPER_UPDATES = ('__dict__',)

def wraps(wrapped,
          assigned = WRAPPER_ASSIGNMENTS,
          updated = WRAPPER_UPDATES):
    return partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)
```

## References

- [PEP 318 - Decorators for Functions and Methods](https://peps.python.org/pep-0318/)
- [PEP 614 – Relaxing Grammar Restrictions On Decorators](https://peps.python.org/pep-0614/)
