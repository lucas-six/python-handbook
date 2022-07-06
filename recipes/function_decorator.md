# Function Decorator

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

## Usage: Wrapper

### No Argument

```python
from functools import wraps

def decorator(_func):

    @wraps(_func)
    def wrapper(*args, **kwargs):
        """wrapper function."""
        print(f'run wrapper: {args}, {kwargs}')
        return _func(*args, **kwargs)

    return wrapper

@decorator
def func(*args, **kwargs):
    """original function."""
    print(f'run func: {args}, {kwargs}')


# Without Arguments
>>> func()
run wrapper: (), {}
run func: (), {}

# With Arguments
>>> func('arg1', 'arg2')
run wrapper: ('arg1', 'arg2'), {}
run func: ('arg1', 'arg2'), {}
```

```python
>>> func.__module__
'**main**'
>>> func.__name__
'func'
>>> func.__doc__
'original function.'
>>> func.__annotations__
{}
>>> func.__qualname__
'func'
```

Without **`@functools.wraps`**, some attributes have not been passed:

```python
>>> func.__module__
'__main__'
>>> func.__name__
'wrapper'
>>> func.__doc__
'wrapper function.'
>>> func.__annotations__
{}
>>> func.__qualname__
'decorator.<locals>.wrapper'
```

### Required Arguments

```python
from functools import wraps

def decorator(arg1=None, arg2=None, *_args, **_kwargs):

    def _decorator(_func):

        @wraps(_func)
        def wrapper(*args, **kwargs):
            """wrapper function."""
            print(f'run wrapper: {arg1}, {arg2}, {_args}, {_kwargs}')
            return _func(*args, **kwargs)

        return wrapper

    return _decorator

@decorator(1, 2)
def func(*args, **kwargs):
    """original function."""
    print(f'run func: {args}, {kwargs}')
```

### Optional Arguments

```python
from functools import wraps, partial

def decorator(func=None, *, arg1=None, arg2=None):
    if func is None:
        return partial(decorator, arg1=arg1, arg2=arg2)

    @wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper function."""
        print(f'run wrapper: {args}, {kwargs}')
        return func(*args, **kwargs)

    return wrapper

@decorator(1, 2)
def func(*args, **kwargs):
    """original function."""
    print('run func')
```

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
