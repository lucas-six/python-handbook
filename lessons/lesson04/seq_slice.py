#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

a = [1, 2, 3, ' ', 'a', 'b', 'c', '好']
b = (1, 2, 3, ' ', 'a', 'b', 'c', '好')

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
