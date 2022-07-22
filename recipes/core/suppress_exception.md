# Suppress Exception

## Signature

```python
contextlib.suppress(*exceptions)
```

New in Python *3.4*.

Return a context manager that **suppresses** any of the specified exceptions
if they occur in the body of a `with` statement
and then resumes execution with the first statement following the end of the `with` statement.

## Usage

**NOTE**: This context manager is **reentrant**.

```python
from contextlib import suppress


with suppress(FileNotFoundError):
    os.remove('somefile.tmp')

with suppress(FileNotFoundError):
    os.remove('someotherfile.tmp')
```

This code is equivalent to:

```python
try:
    os.remove('somefile.tmp')
except FileNotFoundError:
    pass

try:
    os.remove('someotherfile.tmp')
except FileNotFoundError:
    pass
```
