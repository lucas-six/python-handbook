# Lesson 4 Python列表和元组

```python
a = [1, 2, 3, ' ', 'a', 'b', 'c', '好']

b = (1, 2, 3, ' ', 'a', 'b', 'c', '好')
```

**NOTE**: 列表(list)可修改(mutable), 元组(tuple)不可修改(immutable)

序列(sequence): `str`, `list`, `tuple`

## 长度(length)

长度适用于序列(sequence): `str`, `list`, `tuple`

```python
assert len(a) == 8

assert len(b) == 8
```

## 索引(index)

索引适用于序列(sequence): `str`, `list`, `tuple`

```python
assert a[0] == 1
assert a[-1] == '好'

assert b[0] == 1
assert b[-1] == '好'
```

索引越界: `IndexError: list index out of range`

## 遍历

```python
for a0 in a:
    print(a0)

for b0 in b:
    print(b0)
```

## 分片(slice)

分片适用于序列(sequence): `str`, `list`, `tuple`

```python
assert a[0] == 1
assert a[-1] == '好'
assert a[1:3] == [2, 3]
assert a[1:] == [2, 3, ' ', 'a', 'b', 'c', '好']
assert a[:3] == [1, 2, 3]
assert a[::2] == [1, 3, 'a', 'c']
assert a[:] == [1, 2, 3, ' ', 'a', 'b', 'c', '好']  # 复制

assert b[0] == 1
assert b[-1] == '好'
assert b[1:3] == (2, 3)
assert b[1:] == (2, 3, ' ', 'a', 'b', 'c', '好')
assert b[:3] == (1, 2, 3)
assert b[::2] == (1, 3, 'a', 'c')
assert b[:] == (1, 2, 3, ' ', 'a', 'b', 'c', '好')  # 复制
```

Refer to `seq_slice.py`

## 操作符

`in`

```python
assert 1 in a
```

## 常见方法

- `max()` / `min()`

### 列表常用方法

- `append()`/`extend()`
- `del`
- `count()`
- `index()`
- `remove()`
- `sort()`/`reverse()` in place
- 列表推导式(list comprehension): `[x for x in 'abracadabra' if x not in 'abc']`
- 遍历且更新列表，需复制: `for b in a[:]`
