# Lesson 2 Python控制流

```python
if a == 1:
    print(a)
else:
    pass
```

## 控制流(Control Flow)

### 条件语句

- `if`
- `elif`
- `else`

### 循环语句

- `for`, `in`, `else`
- `while`, `else`
- `break`

```python
n = 5
while n > 0:
    print(n)
    n = n - 1
print('out of while: ')
print(n)
```
Refer to `while_statement.py`

```python
n = 5
while n > 0:
    print(n)
    n = n - 1
    if n == 1:
        break
print('out of while: ')
print(n)
```
Refer to `while_statement_with_break.py`

### 什么也不做

- `pass`

## 彩蛋

### `print()`不换行

```python
n = 5
while n > 0:
    print(n)
    n = n - 1
    if n == 1:
        break
print('out of while: ', n)
```
Refer to `while_statement_with_break_print.py`
