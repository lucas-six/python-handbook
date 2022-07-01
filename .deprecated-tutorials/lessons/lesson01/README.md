# Lesson 1 Python基础类型

```python
a = 1
```

## 基础类型

- `type()` / `isinstance()`
- `bool`, `int`, `float`, `str`, `bytes`, `None`

### 布尔类型(`bool`)

- `True` / `False`
- `not`, `and`, `or`
- 断言(**assertion**): `assert`, `AssertionError`

### 整数型(`int`)

- `0b`/`0o`/`0x`
- `bin()`, `oct()`, `hex()`
- `abs()`

### 浮点数(`float`)

- `float('inf')`, `float('-inf')`, `float('nan')`
- `abs()`
- `round()`

## 操作符或运算符(operator)

- `+`, `-`, `*`, `/`, `**`, `//`, `%`
- `()`
- `==`, `!=`, `<`, `>`, `>=`, `<=`
- `is`

```python
0 * 0 = 1
```

### 类型转换

- `int()`
- `float()`
- `str()`

`int` -> `float`:

```python
1 + 1.0
```

`bool` -> `int`:

```python
1 + True
```

`int` -> `bool`:

```python
assert 1
assert 0
```

`float` -> `bool`:

```python
assert 1.0
assert 0.0
```

`None` -> `bool`:

```python
assert None
```

## 编程概念

- 表达式(expression)，语句(statement)，语法错误(`SyntaxError`)
- 变量，常量，类型(type)和值(value)，赋值语句(assignment)，`del`，`NameError`，`TypeError`
- bug，调试(debug)
- 交互模式，脚本(script)模式
- 注释(comment): `#`

### 语法错误(`SyntaxError`)

`IndentationError`

```python
a =
```

### `NameError`

```python
del b
```

### `TypeError`

```python
1 + None
```

## 脚本模式

```python
#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

print('hello world')
```
