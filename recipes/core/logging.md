# Logging

## Components

- `Logger`
- `LogRecord`
- `Handler`
- `Filter`
- `Formatter`

## Basic Usage

```python
import logging

logging.debug('xxx')
logging.info('xxx')
logging.warning('xxx')
logging.error('xxx')
logging.critical('xxx')
```

### Logger

```python
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.debug('xxx')
logger.info('xxx')
logger.warning('xxx')
logger.error('xxx')
logger.critical('xxx')
```

## Config

### Basic

```python
import logging

# The call to `basicConfig()` should come before any calls to `debug()`, `info()`, etc.
# As it’s intended as a one-off simple configuration facility,
# only the first call will actually do anything: subsequent calls are effectively no-ops.
logging.basicConfig(
    level=logging.DEBUG,
    style='{',  # f-string
    format='[{levelname}] [{asctime}] {name} {processName}({process}) {message}',
    # datefmt='%Y-%m-%d %H:%M:%S'

    # logging to file
    filename='example.log',
    encoding='utf-8'
)
```

### Dictionay

```python
import logging
import logging.config
import time

# UTC (GMT) Time
class UTCFormatter(logging.Formatter):
    converter = time.gmtime

LOGGING = {
    'version': 1,
    # 'disable_existing_loggers': True,
    'formatters': {
        'debug': {
            'class': 'logging.Formatter',
            'style': '{',
            'format': '[{levelname}] [{asctime}] {name} {process}({processName}) {thread}({threadName}) {message}',
        },
        'verbose': {
            '()': UTCFormatter,
            'style': '{',
            'format': '[{levelname}] [{asctime}] {name} {process} {thread} {message}',
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
            'formatter': 'debug',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'debug',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'example.log',
            'mode': 'a',
            'encoding': 'utf-8',
            'errors': 'strict',  # since Python 3.9
            'formatter': 'verbose',
        },
        'rfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'r.log',
            'mode': 'a',
            'encoding': 'utf-8',
            'errors': 'strict',  # since Python 3.9
            'maxBytes': 204800,  # 200kB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'tfile': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 't.log',
            'encoding': 'utf-8',
            'errors': 'strict',  # since Python 3.9
            'when': 'midnight',  # for Day; 's'(second), 'm'(minute), 'h'(hour), 'd'(day)
            'atTime': None,  # datetime.time instance
            'interval': 1,
            'utc': True,
            'formatter': 'verbose',
        },
        'errors': {
            'level': 'WARNING',
            'class': 'logging.RotatingFileHandler',
            'filename': 'errors.log',
            'mode': 'a',
            'encoding': 'utf-8',
            'errors': 'strict',  # since Python 3.9
            'maxBytes': 204800,  # 200kB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'app': {
            'level': 'INFO',
            'handlers': ['tfile', 'errors']
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'rfile', 'errors']
    },
}
logging.config.dictConfig(LOGGING)
```

## Commond-Line Option

```bash
python --log=INFO x.py
```

```python
import logging

# assuming loglevel is bound to the string value obtained from the
# command line argument. Convert to upper case to allow the user to
# specify --log=DEBUG or --log=debug
numeric_level = getattr(logging, loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError(f'Invalid log level: {loglevel}')

logging.basicConfig(level=numeric_level, ...)
```

## Logging Flow

![Logging Flow](https://leven-cn.github.io/python-handbook/imgs/logging_flow.png)

## References

- [Python - `logging` module](https://docs.python.org/3/library/logging.html)
- [Python - `logging.config` module](https://docs.python.org/3/library/logging.config.html)
- [Python - `logging.handlers` module](https://docs.python.org/3/library/logging.handlers.html)
- [Python - Logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [PEP 391 – Dictionary-Based Configuration For Logging](https://peps.python.org/pep-0391/)
