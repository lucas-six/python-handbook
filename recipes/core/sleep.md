# Sleep and Monotonic Clock

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
