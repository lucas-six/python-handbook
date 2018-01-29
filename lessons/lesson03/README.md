# Lesson 2 Python字符串

```python
a = 'abc 123  @! 你好'
```

## 字符集编码(Charset Encoding)

- `ASCII`
- Unicode
- `UTF-8`

### Python中的编码

**`ord()`/ `chr()`**

```python
assert ord('A') == 65
assert ord('你') == 20320

assert chr(65) == 'A'
assert chr(20320) == '你'
```

## 字符串 `str`

### 索引(index)

```python
assert a[0] == 'a'
assert a[-1] == '好'
```

### 分片(slice)

```python
s = 'abcdef'
assert s[0] == 'a'
assert s[-1] == 'f'
assert s[1:3] == 'bc'
assert s[1:] == 'bcdef'
assert s[:3] == 'abc'
assert s[::2] == 'ace'
assert s[:] == 'abcdef'  # 复制
```

Refer to `str_slice.py`

### 常见方法

- `startswith()`/`endswith()`
- `lower()`/`upper()`
- `format()`
- `join()` 尽量使用.join()方法连接字符串, +在JPython版本中运行效率很低!!!
- `split()`
- `strip()`/`rstrip()`/`lstrip()`
- `replace()`
- `find()` 没有则返回-1
