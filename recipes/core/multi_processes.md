# Multi-Processes - `multiprocessing`

## Basic Usage

```python
import logging
import multiprocessing
import os


def worker(logger: logging.Logger):
    """worker function."""
    # current process
    p: multiprocessing.Process = multiprocessing.current_process()
    pid: int = p.pid
    p_name: str = p.name
    assert pid == os.getpid()
    assert p_name == 'worker_name'

    # parent process
    pp: multiprocessing.Process = multiprocessing.parent_process()
    assert pp.pid == os.getppid()

    logger.debug(f'run {p_name}({pid})')


def worker_args(logger: logging.Logger, num: int):
    """worker function with parameters."""
    logger.debug(f'worker {num}')


if __name__ == '__main__':

    # is equivalent to:
    #
    # logging.basicConfig(
    #      level=logging.DEBUG,
    #      format='[%(levelname)s/%(processName)s] %(message)s'
    # )
    logger = multiprocessing.log_to_stderr(logging.DEBUG)


    p1 = multiprocessing.Process(target=worker, name='worker_name', args=(logger,))
    p1.start()
    for i in range(5):

        # passing arguments
        # default name: "Process-N"
        p = multiprocessing.Process(target=worker_args, args=(logger, i))
        p.start()


    # enumerate active child processes
    for p in multiprocessing.active_children():
        logger.debug(f'join {p.name}({p.pid})')
        p.join()
```

## Daemon

```python
import logging
import multiprocessing
import time

def daemon(logger: logging.Logger):
    logger.debug('start')
    time.sleep(0.2)
    logger.debug('end')

def non_daemon(logger: logging.Logger):
    logger.debug('run')

if __name__ == '__main__':
    logger = multiprocessing.log_to_stderr(logging.DEBUG)
    d = multiprocessing.Process(target=daemon, name='daemon', args=(logger,), daemon=True)
    p = multiprocessing.Process(target=non_daemon, name='non_daemon')

    d.start()
    p.start()

    # Wait until the process terminates.
    d.join()
    p.join()
```

Logging output:

```plaintext
[DEBUG/daemon] start
[DEBUG/non_daemon] run
[DEBUG/daemon] end
```

## Timeout

```python
import logging
import multiprocessing
import time

def daemon(logger: logging.Logger):
    logger.debug('start')
    time.sleep(0.2)
    logger.debug('end')

def non_daemon(logger: logging.Logger):
    logger.debug('run')

if __name__ == '__main__':
    logger = multiprocessing.log_to_stderr(logging.DEBUG)
    d = multiprocessing.Process(target=daemon, name='daemon', args=(logger,), daemon=True)
    p = multiprocessing.Process(target=non_daemon, name='non_daemon')

    d.start()
    p.start()

    # Wait until the process terminates or 0.2 seconds.
    d.join(0.2)
    if d.is_alive():
        logger.debug(f'{d.name} is alive')
    p.join()
```

logging output:

```plaintext
[daemon] start
[non_daemon] run
[mainProcess] daemon is alive
```

## Terminate

```python
import logging
import multiprocessing
import sys
import time

def worker(logger: logging.Logger):
    logger.debug('run')
    time.sleep(5)


def worker_exit_error():
    sys.exit(1)


if __name__ == '__main__':
    logger = multiprocessing.log_to_stderr(logging.DEBUG)
    p = multiprocessing.Process(target=worker, name='worker', args=(logger,))
    p_error = multiprocessing.Process(target=worker, name='worker_exit_error')

    p.start()
    p_error.start()

    p.terminate()

    # Wait until the process terminates.
    p.join()
    p_error.join()
    logger.debug(p.exitcode, p_error.exitcode)  # 0, 1
```

## Subclass Process

```python
import multiprocessing

class MyProcess(multiprocessing.Process):

    def run(self):
        print('run')

if __name__ == '__main__':
    p = MyProcess()
    p.start()
    p.join()
```

## IPC

### Queue: Producer-Consumer

```python
import multiprocessing

def consumer(tasks: multiprocessing.JoinableQueue, results: multiprocessing.Queue):
    while True:
        task = tasks.get()
        if task is None:
            tasks.task_done()
            break

        # ... to process the task
        tasks.task_done()
        results.put('result')

def producer(tasks: multiprocessing.JoinableQueue, max_num_tasks):
    # ... to produce_an_item
    tasks.put('task')
    for i in range(max_num_tasks):
        tasks.put(None)

if __name__ == '__main__':
    max_num_tasks = multiprocessing.cpu_count() * 2
    tasks = multiprocessing.JoinableQueue(max_num_tasks)
    results = multiprocessing.Queue(max_num_tasks)

    # start consumers
    consumers = []
    for i in range(max_num_tasks):
        c = multiprocessing.Process(target=consumer, args=(tasks, results))
        consumers.append(c)
        c.start()

    # start producer
    p = multiprocessing.Process(target=producer, args=(tasks, max_num_tasks))
    p.start()

    # wait to finish
    tasks.join()
    p.join()
    for c in consumers:
        c.join()

    # output results
    while max_num_tasks:
        result = results.get()
        max_num_tasks -= 1
```

## References

- [Python - `multiprocessing` module](https://docs.python.org/3/library/multiprocessing.html)
