# Synchronization Primitives

## Event

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

## (Mutex) Lock

```python
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

r = MutexResource()
for i in range(3):
    t = threading.Thread(target=worker, args=(r,))
    t.start()

main_thread = threading.main_thread()
for t in threading.enumerate():
    if t is not main_thread:
        t.join()
```

## RLock

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

- [Python - `threading` module](https://docs.python.org/3/library/threading.html)
- [Python - `queue` module](https://docs.python.org/3/library/queue.html)
- [Python - `_thread` module](https://docs.python.org/3/library/_thread.html)
