# Lesson 7 Python函数

```python
def func_name():
	pass

def func_name2(a):
	return a + 1
```

**NOTE**: 引入函数（function）的两个目的：减少代码冗余和便于调试

```bash
>>> type(func_name)
<class 'function'>
```

## 默认参数

```python
# 函数参数的默认值只计算一次
def f(a, L=[]):
    L.append(a)
    return L
assert f(1) == [1]
assert f(2) == [1 , 2]
assert f(3) == [1, 2, 3]

# 由于函数参数的默认值只计算一次,如果有默认值的参数是可改变对象，应该按照此函数定义。
def func_params_default_value(arg, L=None):
    if L is None:
        L = []
    L.append(arg)
    return L
assert func_params_default_value(1) == [1]
assert func_params_default_value(2) == [2]
assert func_params_default_value(3) == [3]
```

## 从字典、元组或列表中获取函数参数

```python
def func_unpack_args(arg1, arg2):
    pass

# 字典
mydict = {'arg1': 1, 'arg2': 2}
func_unpack_args(**mydict)

# 元组或列表
mytuple = ("a", "b")
func_unpack_args(*mytuple)
```

## 可变长参数

```python
# 1. *vargs参数位置必须在**args之前.
# 2. 任何在*vargs参数A之后的均为关键字参数（不可按参数顺序）
def func_vargs(arg, other='o', *vargs, **args):

    # 所有vargs参数都映射为元组(tuple)
    for param in vargs:
        # handle `*vargs`
        pass

    # 所有args参数都映射为有序字典(OrderedDict)
    for key, value in args.items():
        # handle `**args`
        pass
```
