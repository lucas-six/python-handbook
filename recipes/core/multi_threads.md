# Multi-Threads - `threading`

## Examples (Recipes)

- [Multi-Threads Parallelism for **I/O-bound** tasks](https://leven-cn.github.io/python-cookbook/recipes/core/multi_threads)

## Daemon

*`Thread.isDaemon()`* and *`Thread.setDaemon()`* are deprecated, using **`Thread.daemon`** instead.

```python
import logging
import threading
import time

def daemon():
    logging.debug('start')
    time.sleep(0.2)
    logging.debug('end')

def non_daemon():
    logging.debug('start')
    logging.debug('end')

logging.basicConfig(
    level=logging.DEBUG,
    style='{',
    format='[{threadName}] {message}'
)

d = threading.Thread(target=daemon, name='daemon', daemon=True)
t = threading.Thread(target=non_daemon, name='non_daemon')

d.start()
t.start()

# Wait until the thread terminates.
d.join()
t.join()
```

Logging output:

```plaintext
[daemon] start
[non_daemon] start
[non_daemon] end
[daemon] end
```

## Timer

```python
import logging
import threading

logging.basicConfig(
    level=logging.DEBUG,
    style='{',
    format='[{threadName}] {message}'
)

def worker():
    logging.debug('run')

t = threading.Timer(0.3, worker)
t.name = 'worker'
t.start()  # run after 0.3 seconds
time.sleep(0.2)
t.cancel()  # stop the timer, and cancel the execution of the timer’s action.
```

## References

- [Python - `threading` module](https://docs.python.org/3/library/threading.html)
- [Python - `queue` module](https://docs.python.org/3/library/queue.html)
- [Python - `_thread` module](https://docs.python.org/3/library/_thread.html)
