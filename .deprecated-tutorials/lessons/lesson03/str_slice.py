#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

s = 'abcdef'
assert s[0] == 'a'
assert s[-1] == 'f'
assert s[1:3] == 'bc'
assert s[1:] == 'bcdef'
assert s[:3] == 'abc'
assert s[::2] == 'ace'
assert s[:] == 'abcdef'  # 复制
