# Time

## Timestamp (Unix time)

```python
import time

# seconds
>>> t = time.time()
>>> isinstance(t, float)
True

# nanoseconds
>>> t = time.time_ns()
>>>isinstance(t, int)
True
```

## epoch

The point where the time starts.
For Unix, the epoch is *January 1, 1970, 00:00:00 (UTC)*.

To find out what the epoch is on a given platform:

```python
import time

time.gmtime(0)
```

## UTC Time

```python
>>> utc_time = time.gmtime()
>>> isinstance(utc_time, time.struct_time)
```

## Local Time

```python
import time

>>> local_time = time.localtime()
>>> isinstance(local_time, time.struct_time)
```

## Local Time To Timestamp

```python
import time

>>> local_time = time.localtime()
>>> isinstance(local_time, time.struct_time)
>>> t = time.mktime(local_time)
>>> isinstance(t, float)
```

## Sleep

```python
import time

time.sleep(1.2)  # in seconds
```

## Monotonic Clock

**`time.monotonic()`**: the clock is not affected by system clock updates.

```python
import time

t0 = time.monotonic()
# do something ...
t1 = time.monotonic()
```

**`time.monotonic_ns()`** returns the value in nanoseconds.

## References

- [Python - `time` module](https://docs.python.org/3/library/time.html)
