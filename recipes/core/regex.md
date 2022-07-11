# Regex: Regular Expression

## Basic Usage

```python
import re

p: re.Pattern[str] = re.compile(r'pattern-string')
m: re.Match[str] = p.search('string')
# m: re.Match[str] = p.match('string')  # from beginning
if m:
    assert m.start(), m.end() == m.span()
    s: str = m.group()
else:
    print('no match')
```

## Compile Flags

```python
import re

m = p.search('string', re.IGNORECASE)
```

- **`re.I`**/**`re.IGNORECASE`**: case-insensitive
- **`re.M`**/**`re.MULTILINE`**: multi-lines
- **`re.S`**/**`re.DOTALL`**: *`.`* includs a newline
- **`re.A`**/**`re.ASCII`**: ASCII-only
- **`re.X`**/**`re.VERBOSE`**: separate logical sections of the pattern and add comments

## Named Group

```python
import re

m = p.search(r'(?P<first>\w+) (?P<last>\w+)')
if m:
    s = m.groupdict('first')
```

## References

- [Python - `re`](https://docs.python.org/3/library/re.html)
