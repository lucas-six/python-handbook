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

## Event Signal

```python
import logging
import threading

logging.basicConfig(
    level=logging.DEBUG,
    style='{',
    format='[{threadName}] {message}'
)

def worker_1(event: threading.Event):
    logging.debug('wait for event')
    event.wait()
    logging.debug(f'event set: {event.is_set()}')

def worker_2(event: threading.Event, timeout: float):
    while not event.is_set():
        logging.debug('wait for event')
        event.wait(timeout)
        if event.is_set():
            logging.debug('process the event')
        else:
            logging.debug('timeout')

e = threading.Event()
t1 = threading.Thread(worker_1, name='worker_1', args=(e,))
t1.start()
t2 = threading.Thread(worker_2, name='worker_2', args=(e, 2))
t2.start()

time.sleep(0.2)
e.set()
```

## Lock

```python
import logging
import threading
import time

class MutexResource:

    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def inc(self):
        # is equivalent to:
        #
        # self.lock.acquire()
        # try:
        #     self.value += 1
        # finally:
        #     self.lock.release()
        with self.lock:
            self.value += 1

def worker(r):
    for i in range(3):
        time.sleep(0.5)
        r.inc()

logging.basicConfig(
    level=logging.DEBUG,
    style='{',
    format='[{threadName}] {message}'
)

r = MutexResource()
for i in range(3):
    t = threading.Thread(target=worker, args=(r,))
    t.start()

main_thread = threading.main_thread()
for t in threading.enumerate():
    if t is not main_thread:
        t.join()
```

## RLock vs Lock

RLock = **reentrant lock** = **recursion lock**

- *RLock* may be acquired multiple times by the same thread (owns the lock,
lock the lock or recursion lock),
but only once for *Lock*
- *RLock* can only be released by the owning thread, but *Lock* can be released by any other threads.

## Condition Variable

typical use case: producer-consumer situation with unlimited buffer capacity:

```python
import queue
import threading

def consumer(cond: threading.Condition, q: queue.SimpleQueue):
    with cond:
        # is equivalent to:
        #
        # def an_item_is_available(): return not q.empty()
        # if cond.wait_for(an_item_is_available):
        while q.empty():
            cond.wait()
            item = q.get()

def producer(cond: threading.Condition, q: queue.SimpleQueue):
    with cond:
        q.put('an item')  # produce_an_item
        cond.notify(2)  # default 1, notify_all() for all

cond = threading.Condition()
q = queue.SimpleQueue()
c1 = threading.Thread(target=consumer, name='c1', args=(cond, q))
c2 = threading.Thread(target=consumer, name='c2', args=(cond, q))
p = threading.Thread(target=producer, name='producer', args=(cond, q))
c1.start()
c2.start()
p.start()
```

## `Semaphore` vs `BoundedSemaphore`

A *`Semaphore`* can be released more times than it's acquired,
and that will raise its counter above the starting value.
A *`BoundedSemaphore`* **can't** be raised above the starting value.

This is one of the oldest synchronization primitives in the history of computer science,
invented by the early Dutch computer scientist *Edsger W. Dijkstra* (he used the names `P()` and `V()`).

## Semaphore

typical use case: producer-consumer situation with limited buffer capacity:

```python
import queue
import threading

MAX_SIZE = 5

def consumer(s: threading.BoundedSemaphore, q: queue.Queue):
    with s:
        while True:
            item = q.get()
            # ... to process the item
            q.task_done()

def producer(s: threading.BoundedSemaphore, q: queue.Queue):
    with s:
        # ... to produce_an_item
        q.put('an item')

s = threading.BoundedSemaphore(MAX_SIZE)
q = queue.Queue(MAX_SIZE)
c1 = threading.Thread(target=consumer, name='c1', args=(s, q))
c2 = threading.Thread(target=consumer, name='c2', args=(s, q))
p = threading.Thread(target=producer, name='producer', args=(s, q))
c1.start()
c2.start()
p.start()
q.join()
```

## Barrier

This class provides a simple synchronization primitive for use by a fixed number of threads
that need to wait for each other.

```python
import threading

THRESHOLD = 2

def worker(b: threading.Barrier):
    try:
        b.wait()
    except threading.BrokenBarrierError:
        # to handle

b = threading.Barrier(THRESHOLD)
t1 = threading.Thread(target=worker, name='t1', args=(b,))
t2 = threading.Thread(target=worker, name='t2', args=(b,))
t1.start()
t2.start()

b.abort()

t1.join()
t2.join()
```

## References

- [Python Documentation - `threading`](/docs/python/lastest/en/library/threading.html)
- [Python Documentation - `queue`](/docs/python/lastest/en/library/queue.html)
- [Python Documentation - `_thread`](/docs/python/lastest/en/library/_thread.html)
