# Lesson 8 Python面向对象(Object Oriented, OO)

## 核心概念

- 类(`class`)
- 属性(`attribute`)
- 方法(`method`)
- 实例(`instance`)
- 继承(`inheritance`)

## Python中的OO:

- `class`
- `object`
- `self`
- `__init__()` / `__str__()` / `__len__()`
- `super()`
- `issubclass()` / `isinstance()`
- `@staticmethod` / `@classmethod`

```python
class A(object):
    '''A class.

    # Built-in Class Attributes:
    - __name__   : string name of class
    - __doc__    : documentation string
    - __bases__  : tuple of class's base classes
    - __slots__  : list of attribute names (reduce memory)
    - __dict__   : mappingproxy(like dict) of class attributes

    # Built-in Instance Attributes:
    - __class__  : class for instance
    - __module__ : module where class is defined
    - __dict__   : dictionary of instance attributes' names and values

    # Built-in Methods:
    - __init__() : constructor
    - __str__()  : string representation, str(obj)
    - __len__()  : length, len(obj)
    '''

    # Python does not provide any internal mechanism track how many instances
    # of a class have been created or to keep tabs on what they are. The best
    # way is to keep track of the number of instances using a class attribute.
    num_of_instances = 0

    def __init__(self, a1=None, a2=None):
        A.num_of_instances += 1
        self.public_instance_attribute = a1
        self.private_instance_attribute = a2

    def public_instance_method(self):
        return (A.num_of_instances,
                self.publuc_instance_attribute,
                self.private_instance_attribute)

    def _private_instance_method(self):
        pass

    @staticmethod
    def static_method():
        return A.num_of_instances

    @classmethod
    def class_method(cls):
        return cls.__name__


assert isinstance(A(), A)
assert type(A).__name__ == 'type'
assert type(A()).__name__ == 'A'
```

## 继承

```python
class B(A):
    '''Subclass of A.
    '''

    def __init__(self, b, a1=None, a2=None):
        super(B, self).__init__(a1, a2)
        self.b = b

    def public_instance_method(self):
        print('Override method of {0}'.format(self.__class__.__bases__[0]))

    def new_method(self):
        print('New method without inheritance from {0}'
                .format(self.__class__.__bases__[0]))


assert issubclass(B, A)
```

示例代码见`oo.py`
