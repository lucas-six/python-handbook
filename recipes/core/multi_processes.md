# Multi-Processes - `multiprocessing`

## Examples (Recipes)

- [Multi-Processes Parallelism for **CPU-bound** tasks](https://leven-cn.github.io/python-cookbook/recipes/core/multi_processes)
- [Multi-Processes - Queue](https://leven-cn.github.io/python-cookbook/recipes/core/multi_processes_queue)

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

## References

- [Python - `multiprocessing` module](https://docs.python.org/3/library/multiprocessing.html)
