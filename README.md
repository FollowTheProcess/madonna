# Madonna

[![License](https://img.shields.io/github/license/FollowTheProcess/madonna)](https://github.com/FollowTheProcess/madonna)
[![PyPI](https://img.shields.io/pypi/v/madonna.svg?logo=python)](https://pypi.python.org/pypi/madonna)
[![GitHub](https://img.shields.io/github/v/release/FollowTheProcess/madonna?logo=github&sort=semver)](https://github.com/FollowTheProcess/madonna)
[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/FollowTheProcess/madonna)
[![CI](https://github.com/FollowTheProcess/madonna/workflows/CI/badge.svg)](https://github.com/FollowTheProcess/madonna/actions?query=workflow%3ACI)
[![Coverage](https://github.com/FollowTheProcess/madonna/raw/main/docs/img/coverage.svg)](https://github.com/FollowTheProcess/madonna)

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

[cookiecutter]: https://github.com/cookiecutter/cookiecutter
[FollowTheProcess/cookie_pypackage]: https://github.com/FollowTheProcess/cookie_pypackage
[contributing guide]: https://FollowTheProcess.github.io/madonna/contributing/contributing.html
[semver]: https://semver.org
