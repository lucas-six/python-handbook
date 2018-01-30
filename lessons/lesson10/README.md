# Lesson 8 Python文件及模块(module)

## 模块
	
- `import ... as ...`
- `from ... import ... as ...`
- `__init__.py`

## 文件处理

- 全局函数: `open()`
- `bytes`
- `OSError`
- `pathlib`(`os.path`/`glob`/`fnmatch`) *NEW in Python 3.4*
- `tempfile`

### 二逼青年写法

```python
# 打开（文本）文件
try:
    f = open('filename', 'rwxtb')
except OSError as err:
    # 错误处理

# 读取并关闭文件
try:
    for line in f:
        print(line)
except OSError as err:
    # 错误处理
finally:
    f.close()
```

### 文艺青年写法

Context Manager (`with`语句)
```python
try:
    with open('filename', 'rwxtb') as f:
        for line in f:
            print(line)
except OSError as err:
    # 错误处理
```

### 临时文件

```python
from tempfile import TemporaryFile

with TemporaryFile('w+') as tf:
    # ...
```

### 二进制文件

```python
# Read fixed-size data directly into buffer without intermediate copying.
#
# Unlike `read()` method, `readinto()` method doesn't need to allocate new
# objects and return them, avoiding making extra memory allocations.

import functools

size = 2
buf = bytearray(size)
try:
    with open(filename, 'rb') as f:
        for nbytes in iter(functools.partial(f.readinto, buf), 0):
            print(nbytes, buf)
except OSError as err:
    print(err)
```
