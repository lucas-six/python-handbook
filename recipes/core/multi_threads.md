# Multi-Threads - `threading`

## Basic Usage

```python
import threading

def worker():
    """thread worker function."""
    print('worker')

for i in range(5):
    t = threading.Thread(target=worker)
    t.start()
```

## Passing Arguments

```python
import threading

def worker(num: int):
    """thread worker function with parameters."""
    print(f'worker {num}')

for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    t.start()
```

## Determine Current Thread

*`Thread.getName()`* and *`Thread.setName()`* are deprecated, using **`Thread.name`** instead.

**`threading.get_native_id()`** and **`Thread.native_id`** are new in Python *3.8*,
available in *Linux*, *macOS*, *Windows*, *FreeBSD*, *OpenBSD*, *NetBSD*, *AIX*.

```python
import threading
import time

def worker_1():
    """thread worker 1."""
    tid: int = threading.get_native_id()
    thread_name: str = threading.current_thread().name
    print(f'{thread_name}({tid}) starting')
    time.sleep(0.2)
    print(f'{thread_name}({tid}) exiting')

def worker_2():
    """thread worker 2."""
    tid: int = threading.get_native_id()
    thread_name: str = threading.current_thread().name
    print(f'{thread_name}({tid}) starting')
    time.sleep(0.3)
    print(f'{thread_name}({tid}) exiting')

t1 = threading.Thread(target=worker_1, name='worker_1')
t2 = threading.Thread(target=worker_2, name='worker_2')
t0 = threading.Thread(target=worker_1)  # default thread name: "Thread-N"

>>> t1.start()
>>> t2.start()
>>> t0.start()
worker_1(1) starting
worker_2(2) starting
Thread-1(3) starting
worker_1(1) exiting
worker_2(2) exiting
Thread-1(3) exiting
```

## Logging

**`threadName`**: thread name

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    style='{',
    format='[{levelName}] {threadName} {message}'
)
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

## Enumerate Active Threads

```python
import logging
import random
import threading
import time

def daemon():
    logging.debug('start')
    time.sleep(random.randint(1 ,5) / 10)
    logging.debug('end')

logging.basicConfig(
    level=logging.DEBUG,
    style='{',
    format='[{threadName}] {message}'
)

for i in range(3):
    d = threading.Thread(target=daemon, name=f'daemon_{i}', daemon=True)
    d.start()

main_thread = threading.main_thread()
for t in threading.enumerate():
    if t is not main_threading:
        t.join()
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
