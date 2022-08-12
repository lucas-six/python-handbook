# Context Manager

## Context Manager Protocol

```python
from types import TracebackType
from typing import Optional, Type


class ContextManager:
    """A example of context manager."""

    def __init__(self, propogate=False, exit_raise_exception=False):
        self.propogate = propogate
        self.exit_raise_exception = exit_raise_exception

    def __enter__(self):
        """Enter the runtime context and return either this object
        or another object related to the runtime context.

        The value returned by this method is bound to the identifier
        in the `as` clause of `with` statements using this context manager.

        - An example of a context manager that returns itself is a `file` object.
        File objects return themselves from `__enter__()`
        to allow `open()` to be used as the context expression in a `with` statement.

        - An example of a context manager that returns a related object
        is the one returned by `decimal.localcontext()`.
        These managers set the active `decimal` context to a copy of
        the original `decimal` context and then return the copy.
        This allows changes to be made to the current `decimal` context
        in the body of the `with` statement without affecting code
        outside the `with` statement.
        """
        print('enter into runtime context')
        return self

    def __exit__(self,
                 exc_type: Optional[Type[BaseException]],
                 exc_val: Optional[Exception],
                 exc_tb: TracebackType) -> bool:
        """Exit the runtime context and return a Boolean flag
        indicating if any exception that occurred should be suppressed.
        `True` for suppressed.

        If an exception occurred while executing the body of the `with` statement,
        the arguments contain the exception type, value and traceback information.
        Otherwise, all three arguments are `None`.
        """
        print('exit from runtime context')
        if self.exit_raise_exception:
            raise TypeError
        if exc_type is not None:
            print(exc_type)
        return self.propogate
```

Case 1: No exception occurred while executing the body of the `with` statement:

```python
>>> with ContextManager() as cm:
...     print('run')
...
enter into runtime context
run
exit from runtime context
```

Case 2: Exception(s) occurred while executing the body of the `with` statement,
exception occurred **NOT** be suppressed by default:

```python
>>> with ContextManager() as cm:
...     print('run')
...     raise KeyError
...
enter into runtime context
run
exit from runtime context
<class 'KeyError'>
KeyError
```

Case 3: Exception(s) occurred while executing the body of the `with` statement,
exception occurred is suppressed:

```python
>>> with ContextManager(propogate=True) as cm:
...     print('run')
...     raise KeyError
...
enter into runtime context
run
exit from runtime context
<class 'KeyError'>
```

Case 4 (not recommended): Exceptions that occur during execution of *`__exit__()`* method
will replace any exception that occurred in the body of the `with` statement:

**Warn**: The exception passed in should never be reraised explicitly - instead,
this method should return a false value to indicate that the method completed successfully
and does not want to suppress the raised exception.
This allows context management code to easily detect
whether or not an `__exit__()` method has actually failed.

```python
>>> with ContextManager(exit_raise_exception=True) as cm:
...     print('run')
...     raise KeyError
...
enter into runtime context
run
exit from runtime context
KeyError
During handling of the above exception, another exception occurred:
TypeError
```

## Examples (Recipes)

- [Create Context Manager](https://leven-cn.github.io/python-cookbook/recipes/core/context_manager)

## Single Use Context Manager

Most context managers are written in a way that means
they can only be used effectively in a `with` statement **once**.
These *single use context managers* must be created afresh each time they're used - attempting to
use them a second time will trigger an exception or otherwise not work correctly.

This common limitation means that it is generally advisable to create context managers directly
in the header of the `with` statement where they are used.

Context managers created using *`contextmanager()`* are also single use context managers,
and will complain about the underlying generator failing to `yield`
if an attempt is made to use them a second time:

```python
from contextlib import contextmanager

@contextmanager
def singleuse():
    print("Before")
    yield
    print("After")

>>> cm = singleuse()

# Run first time
>>> with cm:
...     pass
...
Before
After

# Run second time (failed)
>>> with cm:
...     pass
...
RuntimeError: generator didn't yield
```

## Reentrant Context Manager

**Reentrant** context managers can not only be used in multiple `with` statements,
but may also be used inside a `with` statement that is already using the same context manager.
Such as `threading.RLock`，`contextlib.suppres()`，`contextlib.redirect_stdout()`.

Here's a very simple example of reentrant use:

```python
>>> from contextlib import redirect_stdout
>>> from io import StringIO

>>> stream = StringIO()
>>> write_to_stream = redirect_stdout(stream)

>>> with write_to_stream:
...     print("This is written to the stream rather than stdout")
...     with write_to_stream:
...         print("This is also written to the stream")
...

>>> print("This is written directly to stdout")
This is written directly to stdout

>>> print(stream.getvalue())
This is written to the stream rather than stdout
This is also written to the stream
```

**Note**: Being *reentrant* is **not** the same thing as being *thread safe*.

## Reusable Context Manager

To be completely explicit, "reusable, but not reentrant" context managers,
since reentrant context managers are also reusable.
These context managers support being used multiple times,
but will fail (or otherwise not work correctly)
if the specific context manager instance has already been used in a containing `with` statement.
Such as `threading.Lock`，`contextlib.ExitStack`.

## References

- [Python - `with` Statement Context Managers](https://docs.python.org/3/reference/datamodel.html#context-managers)
- [Python - Context Manager Types](https://docs.python.org/3/library/stdtypes.html#typecontextmanager)
- [Python - `@contextlib.contextmanager`](https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager)
