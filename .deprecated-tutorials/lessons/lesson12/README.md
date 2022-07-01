# Lesson 12 Python代码规范

参考 [PEP 8](https://www.python.org/dev/peps/pep-0008/)

## 缩进

- 使用4个空格缩进，避免使用`Tab`.（如果使用`Tab`，则使用4个空格替换`Tab`的方式）

- 括号中使用悬挂缩进，2个缩进

```python
a = long_function_name(
        var_one, var_two,
        var_three, var_four)
```

- `if`语句跨行使用悬挂缩进，2个缩进

```python
if this_is_one_condition
        and this_is_another_condition:
    do_something()
```

## 行宽

- 限制最大行宽为100字符，文档字符串或注释为79

> Python 标准库比较保守，限制行宽为79字符

## 空行和空格

- 两行空行分割顶层函数和类的定义

- 单个空行分割类的方法定义

- 额外的空行可以分割逻辑块，但尽量节约使用

- 在操作符两边、逗号后使用空格。例如：`a = f(a, b)`

## 编码

- 所有文本文件（包括代码）一律使用**UTF-8**编码

## 注释

- 尽可能将注释放在单独一行

- 更新代码前，优先更新注释

- 使用docstring注释模块、类、方法、函数

## 命名

- 类的命名方式为`CamelCase`，方法及函数为`lower_case_with_underscores`

- 避免使用下划线开始的方式命名变量、函数或类

> 一般而言，使用`_xxx`开始的变量名为“私有的”变量或者方法。

> 以`__xxx__`命名的方法或变量，是Python内部变量。

## 变量

- 避免重复计算，使用变量保存计算结果

- 避免"Magic"数字。例如：`a[0]`或者`if a == 1`

## 模块导入

- 模块导入`import`始终在文件顶部，在模块注释和文档字符串之后，在模块全局变量和常量之前

- 模块导入在单独一行

```python
import sys
import os

# 不是
import sys, os
```

> 模块导入顺序:
>
>      - 标准库模块
>      - 第三方模块
>      - 自定义模块
>
> 每个模块类型都以一个空行分隔

- 禁止使用通配符导入 ( `from module import *` ).

## 编程建议

### 布尔值判断

```python
if a
if a == True      # Bad!!!
if a is True      # Worse!!!
```
### 判断是否是None

```python
if a is None
if a is not None
if not a is None  # Bad!!!
```

### 判断空序列

```python
if seq             # OK

if len(seq)        # Bad!!!
if len(seq) != 0   # Worse!!!
if not len(seq)    # Worse!!!
```

自定义异常类继承自`Exception`，而不是`BaseException`, Exception设计参考[PEP 3151](https://www.python.org/dev/peps/pep-3151/)
