# Decorator

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

def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper function."""
        print(f'run wrapper: {args}, {kwargs}')
        return func(*args, **kwargs)

    print('run decorator')
    return wrapper

@decorator
def func(*args, **kwargs):
    """original function."""
    print('run func')


# Without Arguments
>>> func()
run decorator
run wrapper: (), {}
run func

# With Arguments
>>> func('arg1', 'arg2')
run decorator
run wrapper: ('arg1', 'arg2'), {}
run func
```

```python
>>> func.**module**
'**main**'
>>> func.**name**
'func'
>>> func.**doc**
'original function.'
>>> func.**annotations**
{}
>>> func.**qualname**
'func'
```

Without **`@functools.wraps`**, some attributeshave not been passed:

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

### With Arguments

```python
from functools import wraps, partial

def decorator(func=None, arg1=None, arg2=None):
    if func is None:
        return partial(decorator, arg1=arg1, arg2=arg2)

    @wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper function."""
        print(f'run wrapper: {args}, {kwargs}')
        return func(*args, **kwargs)

    print('run decorator')
    return wrapper

@decorator(1, 2)
def func(*args, **kwargs):
    """original function."""
    print('run func')
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

## Function (Method) Decorators Examples

1. Add attributes to a function/method.

    ```python
    def attrs(**kwds):
        def wrapper(func):
            for k in kwds:
                setattr(func, k, kwds[k])
            return func
        return wrapper

    @attrs(versionadded="2.2",
           author="Guido van Rossum")
    def method(f):
        pass
    ```

2. Enforce function argument and return types.

    ```python
    def accepts(*types):
        def wrapper(func):
            assert len(types) == func.func_code.co_argcount

            def new_func(*args, **kwds):
                for (a, t) in zip(args, types):
                    assert isinstance(a, t), f'arg {a} does not match {t}'
                return func(*args, **kwds)

            new_func.func_name = func.func_name
            return new_func
        return wrapper

    def returns(rtype):
        def wrapper(func):
            def new_func(*args, **kwds):
                result = func(*args, **kwds)
                assert isinstance(result, rtype), f'return value {result} does not match {rtype}'
                return result
            new_func.func_name = func.func_name
            return new_func
        return wrapper

    @accepts(int, (int,float))
    @returns((int,float))
    def func(arg1, arg2):
        return arg1 * arg2
    ```

## Class Decorators

```python
class A:
  pass
A = decorator_a(decorator_b(A))


@decorator_a
@decorator_b
class A:
  pass
```

A class decorator is defined as follows:

```python
from functools import wraps

class Decorator:
    def __init__(self, func):
        print('create instance')
        self.func = func

    @wraps(func)
    def __call__(self, *args, **kwargs):
        print('working here')
        return self.func(*args, **kwargs)

@Decorator
def func(arg1, arg2):
    return f'{arg1=}, {arg2=}'


>>> func('A', 'B')
create instance
working here
"arg1='A', arg2='B'"
```

A decorator for classes is defined as follows:

```python
def decorator(cls):
    cls.num_of_animals = 10
    return cls

@decorater
class A:
    pass


>>> a_obj = A()
>>> A.num_of_animals
10
```

## Class Decorators Examples

1. Define a class with a singleton instance.

    ```python
    def singleton(cls):
        instances = {}
        def getinstance():
            if cls not in instances:
                instances[cls] = cls()
            return instances[cls]
        return getinstance

    @singleton
    class MyClass:
        pass
    ```

2. Declare that a class implements a particular (set of) interface(s).

    ```python
    def provides(*interfaces):
        """
        An actual, working, implementation of provides for
        the current implementation of PyProtocols.
        Not particularly important for the PEP text.
        """
        def provides(typ):
            declareImplementation(typ, instancesProvide=interfaces)
            return typ
        return provides

    class IBar(Interface):
        """Declare something about IBar here"""
        pass

    @provides(IBar)
    class Foo(object):
        """Implement something here..."""
        pass
    ```

## References

- [PEP 318 - Decorators for Functions and Methods](https://peps.python.org/pep-0318/)
- [PEP 3129 – Class Decorators](https://peps.python.org/pep-3129/)
- [PEP 614 – Relaxing Grammar Restrictions On Decorators](https://peps.python.org/pep-0614/)
