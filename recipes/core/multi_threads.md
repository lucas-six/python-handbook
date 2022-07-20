# Multi-Threads - `threading`

## Basic Usage

```python
import logging
import threading


logging.basicConfig(
    level=logging.DEBUG,
    style='{',
    # thread: thread id
    format='[{levelName}] {threadName}({thread}) {message}'
)


def worker():
    """thread worker function."""

    logger = logging.getLogger()

    current_thread: threading.Thread = threading.current_thread()

    # thread ID
    # `threading.get_native_id()` and `Thread.native_id` are new in Python 3.8,
    # available in Linux, macOS, Windows, FreeBSD, OpenBSD, NetBSD, AIX.
    tid: int = current_thread.native_id
    assert tid == threading.get_native_id()

    # thread name
    # `Thread.getName()` and `Thread.setName()` are deprecated,
    # using `Thread.name` instead.
    thread_name: str = current_thread.name
    assert thread_name == 'worker_name'

    logger.debug('finished')


def worker_args(num: int):
    """thread worker function with parameters."""
    logging.debug(f'worker {num}')


for i in range(5):
    t1 = threading.Thread(target=worker, name='worker_name')

    # passing arguments
    t2 = threading.Thread(target=worker_args, args=(i,))  # default thread name: "Thread-N"

    t1.start()
    t2.start()


# Wait until the threads terminate.
main_thread = threading.main_thread()
for t in threading.enumerate():  # enumerate active threads
    if t is not main_thread:
        logging.debug(f'join {t.name}({t.native_id})')
        t.join()
```

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

## Timeout

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

# Wait until the thread terminates or 0.2 seconds.
d.join(0.2)
if d.isAlive():
    logging.debug(f'{d.name} isAlive')
t.join()
```

logging output:

```plaintext
[daemon] start
[non_daemon] start
[non_daemon] end
[mainThread] daemon isAlive
```

## Subclass Threads

```python
import logging
import threading

class MyThread(threading.Thread):

    def run(self):
        logging.debug('start')
        logging.debug('end')

logging.basicConfig(
    level=logging.DEBUG,
    style='{',
    format='[{threadName}] {message}'
)

for i in range(3):
    t = MyThread()
    t.start()
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
