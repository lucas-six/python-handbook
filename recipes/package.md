# Packaging Python Projects

## Project file/directory structure

```plaintext
<repo-name>/
├── LICENSE
├── CONTRIBUTION
├── pyproject.toml
├── .pre-commit-config.yaml
├── README.md
├── setup.cfg (optional)
└── src/
│   └── <project_name>/
│       ├── __init__.py
│       └── example.py
└── tests/
```

## Prepare environment

```bash
pipx install pipenv 'flit>=3.4'

pipenv --python 3.9
```

## `pyproject.toml`

```toml
[build-system]
requires = ["flit_core >=3.4,<4"]
build-backend = "flit_core.buildapi"

[project]
name = "<project_name>"
description = "<project description>"
authors = [
    {name = "<Author Name>", email = "<author@email>"},
    {name = "Lee", email = "leven.cn@gmail.com"},
]
readme = "README.md"
requires-python = "~=3.9"
license = {file = "LICENSE"}
maintainers = [
    {name = "<Maintainer Name>", email = "<maintainer@email>"},
]
keywords = ["xxx"]
classifiers = [
    "Development Status :: 1 - Planning",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    "License :: OSI Approved :: Apache Software License",
    "Typing :: Typed",
]
dependencies = [
    "requests >=2.6",
    "configparser; python_version == '2.7'",
]
dynamic = ["version"]

[project.optional-dependencies]
test = [
    "pre-commit",
    "black",
    "isort",
    "mymy",
    "flake8 >= 4.0",
    "pyupgrade",
    "pytest >= 7.1",
    "coverage >= 6.4",
    "pytest-cov >= 3.0",
]
doc = [
    "sphinx"
]

[project.urls]
Documentation = "<URL>"
Source = "<URL>"
Home = "<URL>"

[project.scripts]
<command_name> = "xxx:main"

[project.gui-scripts]
<command_name> = "xxx:main_gui"

[project.entry-points."<group.name>"]
dogelang = "<package>:<name>"

[tool.flit.module]
name = "<module_name>"

[tool.flit.sdist]
include = ["doc/"]
exclude = ["doc/*.html"]

[tool.isort]
profile = "hug"
src_paths = ["isort", "test"]
```

## `pre-commit`

```bash
pipx install pre-commit
```

or in virtual env by `pipenv`:

```bash
pipenv install --dev pre-commit
```

generate a very basic configuration:

```bash
pre-commit sample-config > .pre-commit-config.yaml
```

or in virtual env by `pipenv`:

```bash
pipenv run pre-commit sample-config > .pre-commit-config.yaml
```

Edit `.pre-commit-config.yaml`:

```yaml
# See https://pre-commit.com for more information
# See https://pre-commit.com/hooks.html for more hooks
repos:
    - repo: https://github.com/pre-commit/pre-commit-hooks
      rev: v4.3.0
      hooks:
          - id: trailing-whitespace
            args: [--markdown-linebreak-ext=md]
          - id: end-of-file-fixer
          - id: check-yaml
          - id: check-json
          - id: check-toml
          - id: check-added-large-files
            args: ['--maxkb=500']
          - id: mixed-line-ending
          - id: fix-byte-order-marker
          - id: detect-private-key
          - id: double-quote-string-fixer
          - id: name-tests-test
            args: [--django]

default_language_version:
    # force all unspecified python hooks to run python3
    python: python3
```

Install the Git hook scripts:

```bash
$ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

or in virtual env by `pipenv`:

```bash
$ pipenv run pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

Run as:

```bash
pre-commit run --all-files
```

or in virtual env by `pipenv`:

```bash
pipenv run pre-commit run --all-files
```

Badging your repository in your *`README`*:

Markdown:

```markdown
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
```

HTML:

```html
<a href="https://github.com/pre-commit/pre-commit"><img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white" alt="pre-commit" style="max-width:100%;"></a>
```

### `pyproject.toml`

```toml
[project.optional-dependencies]
test = [
    ...
    "pre-commit",
]
```

## `black`

```bash
pipenv install --dev black
```

### `pyproject.toml`

```toml
[project.optional-dependencies]
test = [
    ...
    "black",
]

[tool.black]
line-length = 88
target-version = ['py39']
skip-string-normalization = true
include = '\.pyi?$'
extend-exclude = '''
# A regex preceded with ^/ will apply only to files and directories
# in the root of the project.
^/foo.py  # exclude a file named foo.py in the root of the project (in addition to the defaults)
^/.github/workflows/*.yml
```

### `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
        args: ['--verbose']
        # It is recommended to specify the latest version of Python
        # supported by your project here, or alternatively use
        # pre-commit's default_language_version, see
        # https://pre-commit.com/#top_level-default_language_version
        language_version: python3.9
```

## `isort`

```bash
pipenv install --dev isort
```

### `pyproject.toml`

```toml
[project.optional-dependencies]
test = [
    ...
    "isort",
]

[tool.isort]
profile = "black"
```

### `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
        name: isort (python)
        language_version: python3.9
```

## `mypy`

```bash
pipenv install --dev mypy
```

### `pyproject.toml`

```toml
[project.optional-dependencies]
test = [
    ...
    "mypy",
]

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
exclude = [
    '^file1\.py$',  # TOML literal string (single-quotes, no escaping necessary)
    "^file2\\.py$",  # TOML basic string (double-quotes, backslash and other characters need escaping)
]
```

### `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.950
    hooks:
      - id: mypy
```

## `flake8`

```bash
pipenv install --dev 'flake8>=4.0'
```

### `pyproject.toml`

```toml
[project.optional-dependencies]
test = [
    ...
    "flake8 >= 4.0",
]

[tool.flake8]
max_complexity = 20
max-line-length = 88
benchmark = true
```

### `.pre-commit-config.yaml`

```yaml
- repo: https://github.com/PyCQA/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
```

## `pyupgrade`

```bash
pipenv install --dev pyupgrade
```

### `pyproject.toml`

```toml
[project.optional-dependencies]
test = [
    ...
    "pyupgrade",
]
```

### `.pre-commit-config.yaml`

```yaml
- repo: https://github.com/asottile/pyupgrade
    rev: v2.32.1
    hooks:
      - id: pyupgrade
```

## `pytest`

```bash
pipenv install --dev pytest
```

### `pyproject.toml`

```toml
[project.optional-dependencies]
test = [
    ...
    "pytest >= 7.1",
]

[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "serial",
]
addopts = [
    "--strict-markers"
]
```

### GitHub Action

```yaml
- name: Run Pytest
  run: pipenv run pytest
```

## `coverage`

```bash
pipenv install --dev coverage[toml] pytest-cov
```

### `pyproject.toml`

```toml
[project.optional-dependencies]
test = [
    ...
    "coverage[toml] >= 6.4",
    "pytest-cov >= 3.0",
]

[tool.pytest.ini_options]
...
addopts = [
    ...
    "--cov",
    "--cov-append",
]

[tool.coverage.run]
parallel = true

[tool.coverage.report]
skip_empty = true
```

### GitHub Action

```yaml
- name: Run Pytest(coverage)
  run: pipenv run pytest
```

## Publish Package

### `~/.pypirc`

```ini
[distutils]
index-servers =
   pypi
   testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-***

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-***
```

```bash
chmod 600 ~/.pypirc
```

### Publish

```bash
flit publish [--repository pypi|testpypi]
```

## References

- [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [PEP 517 - A build-system independent format for source trees](https://peps.python.org/pep-0517/)
- [PEP 518 – Specifying Minimum Build System Requirements for Python Projects](https://peps.python.org/pep-0518/)
- [`flit` Documentation](https://flit.pypa.io/en/latest/)
- [TOML 1.0](https://toml.io/en/v1.0.0)
- [PEP 621 – Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [PEP 508 – Dependency specification for Python Software Packages](https://peps.python.org/pep-0508)
- [`pre-commit` Documentation](https://pre-commit.com/)
- [`black` Documentation](https://black.readthedocs.io/en/stable/)
- [`isort` Documentation](https://pycqa.github.io/isort/)
- [`mypy` Documentation](https://mypy.readthedocs.io/en/stable/)
- [`flake8` Documentation](https://flake8.pycqa.org/en/latest/)
- [`pytest` Documentation](https://docs.pytest.org/)
- [`coverage` Documentation](https://coverage.readthedocs.io/)
