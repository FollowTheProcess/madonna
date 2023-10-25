# Madonna

[![License](https://img.shields.io/github/license/FollowTheProcess/madonna)](https://github.com/FollowTheProcess/madonna)
[![PyPI](https://img.shields.io/pypi/v/madonna.svg?logo=python)](https://pypi.python.org/pypi/madonna)
[![GitHub](https://img.shields.io/github/v/release/FollowTheProcess/madonna?logo=github&sort=semver)](https://github.com/FollowTheProcess/madonna)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![CI](https://github.com/FollowTheProcess/madonna/workflows/CI/badge.svg)](https://github.com/FollowTheProcess/madonna/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/FollowTheProcess/madonna/branch/main/graph/badge.svg?token=OLMR2P3J6N)](https://codecov.io/gh/FollowTheProcess/madonna)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/FollowTheProcess/madonna/main.svg)](https://results.pre-commit.ci/latest/github/FollowTheProcess/madonna/main)

**A Python semver parsing library.**

* Free software: MIT License

* Documentation: [https://FollowTheProcess.github.io/madonna/](<https://FollowTheProcess.github.io/madonna/>)

## Project Description

Madonna is a small, simple [semver] utility library with support for parsing, writing, and otherwise interacting with semantic versions in code.

**Why the stupid name?**

Get it? "Like a Version"... 👏🏻

Also naming things on PyPI is hard!

## Installation

```shell
pip install madonna
```

## Quickstart

The only construct in madonna is the `Version` object, you can use it for all sorts of useful things...

### Create a New Version

```python
from madonna import Version

v = Version(major=1, minor=2, patch=4)
```

### Parse a Version from a string

```python
from madonna import Version

Version.from_string("v1.2.4-rc.1+build.123")
# Version(major=1, minor=2, patch=4, prerelease="rc.1", buildmetadata="build.123")
```

### Or JSON

```python
from madonna import Version

Version.from_json('{"major": 1, "minor": 2, "patch": 4}')
```

And you can also dump a `Version` to a variety of formats too!

## Contributing

`madonna` is an open source project and, as such, welcomes contributions of all kinds :smiley:

Your best bet is to check out the [contributing guide] in the docs!

### Credits

This package was created with [cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [FollowTheProcess/cookie_pypackage] project template.

[FollowTheProcess/cookie_pypackage]: https://github.com/FollowTheProcess/cookie_pypackage
[contributing guide]: https://FollowTheProcess.github.io/madonna/contributing/contributing.html
[semver]: https://semver.org
