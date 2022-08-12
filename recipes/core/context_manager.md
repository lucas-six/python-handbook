# Context Manager

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
