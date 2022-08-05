# Multi-Processes - `multiprocessing`

## Examples (Recipes)

- [Multi-Processes Parallelism for **CPU-bound** tasks](https://leven-cn.github.io/python-cookbook/recipes/core/multi_processes)

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
