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
- `enumerate()`
- `zip()` / `itertools.zip_longest()`

### `enumerate()` 同时获取索引和值，参考实现：

```python
def enumerate(sequence, start=0):
    n = start
    for elem in sequence:
        yield n, elem
        n += 1
```

### `zip()`/`itertools.zip_longest()` 同时遍历多个序列

- `for value1, value2 in zip(seq1, seq2)`
- `for value1, value2 in itertools.zip_longest(seq1, seq2, fillvalue=None)`

### `itertools.chain()` 连接多个序列, 参考实现如下：

```python
def chain(iterators):
    for i in iterators:
        yield from i
```

`for item in itertools.chain(seq1, seq2)`

### 列表常用方法

- `append()`/`extend()`
- `del`
- `count()`
- `index()`
- `remove()`
- `sort()`/`reverse()` in place
- 列表推导式(list comprehension): `[x for x in 'abracadabra' if x not in 'abc']`
- 遍历且更新列表，需复制: `for b in a[:]`
