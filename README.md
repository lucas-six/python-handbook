# Python Handbook

<section align="center">
  <img src="https://raw.githubusercontent.com/leven-cn/python-handbook/main/.python-logo.png"
    alt="Python Logo" width="200" height="200" title="Python Logo">
  <br><br>
  <p>
    <a href="https://github.com/leven-cn/python-handbook/actions/workflows/lint.yml">
      <img src="https://github.com/leven-cn/python-handbook/actions/workflows/lint.yml/badge.svg"
      alt="GitHub Actions - lint" style="max-width:100%;">
    </a>
    <a href="https://github.com/pre-commit/pre-commit">
      <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white"
      alt="pre-commit" style="max-width:100%;">
    </a>
  </p>
  <p>A missing manual, hands-on guide for <code>Python 3</code></p>
  <p><a href="https://leven-cn.github.io/python-handbook/">https://leven-cn.github.io/python-handbook/</a></p>
</section>

## Topics

<!-- markdownlint-disable line-length -->

### Core

- [String format specification](recipes/core/str_fmt_spec)
- [Function (Method) Decorator](recipes/core/function_decorator)
- [Class Decorator](recipes/core/class_decorator)
- [Context Manager](recipes/core/context_manager)
- Time
  - [Time](recipes/core/time)
  - [Time Zone](recipes/core/timezone)
- Representation of Dates and Times
  - [ISO 8601 Format](recipes/core/iso_8601_fmt)
  - [RFC 3339 Format](recipes/core/rfc_3339_fmt)
  - [Format Dates and Times](recipes/core/time_str_fmt)
- [Type Hint](recipes/core/type_hint)
- Text Processing
  - [Universal Newline](recipes/core/universal_newline)
  - [Regex (Regular Expression)](recipes/core/regex)
  - [FlashText Algorithm - `flashtext`](recipes/core/flashtext)
- I/O (File-Like Object)
  - [Inheritance of File Descriptor](recipes/core/fd_inheritable)
  - [File-Like Object (I/O)](recipes/core/file_object)
  - [`open()` Reference Implementation](recipes/core/open)
- [Logging](recipes/core/logging)
- Parallelism & Concurrent
  - [`threading` - Multi-Threads Parallelism for **I/O-bound** tasks](recipes/core/multi_threads)
  - [`multiprocessing` - Multi-Processes Parallelism for **CPU-bound** tasks](recipes/core/multi_processes)
  - [Process Pool](recipes/core/process_pool)
  - [`concurrent.futures` - High-Level Concurrent](recipes/core/concurrent)
  - [Synchronization Primitives - `Event`](recipes/core/synchronization_event)
  - [Synchronization Primitives - Mutex Lock `Lock`](recipes/core/synchronization_lock)
  - [Synchronization Primitives - Reentrant Lock `RLock`](recipes/core/synchronization_rlock)
  - [Synchronization Primitives](recipes/core/synchronization)
    - `Condition`
    - `Semaphore`/`BoundedSemaphore`
    - `Barrier`
- Package Management
  - [`pip` - Standard Package Manager](recipes/core/pip)
  - [`pipx` - Install and Run Python Applications](recipes/core/pipx)
  - [`pipenv` - Virtual Environment Manager](recipes/core/pipenv)
- Test
  - [`unittest` - Standard Unit Testing Framework](recipes/core/unittest)
  - [`pytest` - Testing Framework](recipes/core/pytest)
- Project Management
  - [Packaging Python Projects, Publishing to PyPI](recipes/package)
- [Performance Measurement](recipes/perf)

<!-- markdownlint-enable line-length -->

## License

[Apache 2.0 License](https://github.com/leven-cn/python-handbook/blob/main/LICENSE)
