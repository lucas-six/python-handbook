# Lesson 5 Python字典和集合

```python
d = {'a': 1, 'b': 'abc'}

s = {1, 2, 3}
```

**NOTE**: 字典(dict)和集合(set)均可修改(mutable)

## 字典(Dictionary)

### 长度(length)

```python
assert len(d) == 2
```

### 键(key)

```python
assert d['a'] == 1
assert d['b'] == 'abc'
```

字典是用**哈希表(`Hash Table`)**实现的**键值对(Key-Value pair)**映射(mapping)关系,
所以，键只能是可哈希(hashable)的值，否则会抛出TypeError异常: `TypeError: unhashable type`

找不到对应的键，抛出``KeyError`异常

### 遍历

```python
# 只遍历键
for k in d:
    print(k)

# 只遍历值
for v in d.values():
    print(v)

# 既遍历键，也遍历值
for k, v in d.items():  # Python 2: i.iteritems()
    print(k, v)
```

### `in`操作符

```python
assert k in d
```

### 常见方法

- `get()`/`pop()`
- `update()`
- `clear()`
- `copy()`/`copy.deepcopy()` 深浅复制

## 集合(set)

集合推导式(set comprehension): `{x for x in 'abracadabra' if x not in 'abc'}`

### 长度(length)

```python
assert len(s) == 3
```

### 操作符

`1 in s`

```python
a - b   # in a, but not in b
a | b   # in either a or b
a & b   # in both a and b
a ^ b   # in a or b but not both
```

### 常用方法

- 全局函数：`max()` / `min()`
- `add()`
- `remove()`
