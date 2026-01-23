<p align="center">
  <img src="https://raw.githubusercontent.com/rockem/busypie/master/docs/source/_static/busypie_logo.png" alt="logo" width="120"/>
</p>
<p align="center">
  <strong>Easy and expressive busy-waiting for Python</strong>
</p>
<p align="center">
  <a href="https://github.com/rockem/busypie/actions/workflows/test.yml">
        <img src="https://github.com/rockem/busypie/actions/workflows/test.yml/badge.svg?branch=master" alt="test badge"/>
        </a>
  <a href="https://pypi.org/project/busypie/">
        <img src="https://img.shields.io/pypi/v/busypie" alt="pypi version"/>
    </a>
  <a href="https://github.com/rockem/busypie/blob/master/LICENSE">
        <img src="http://img.shields.io/:license-apache2.0-blue.svg" alt="license badge"/>
    </a>
</p>

Although you typically wouldn't want to do much busy-waiting in your production code,
testing is a different matter. When testing asynchronous systems,
it's very helpful to wait for some scenario to finish its course.
**busypie** helps you perform busy waiting easily and expressively.

## Installation

```bash
pip install busypie
```

## Quickstart

Most typical usage will be in test, when we have a scenario
that requires us to wait for something to happen.

```python
from busypie import wait, SECOND

def test_create_user():
    create_user_from(USER_DETAILS)
    wait().at_most(2, SECOND).until(lambda: is_user_exists(USER_DETAILS))
```

## Documentation

* [Installation](https://busypie.readthedocs.io/en/latest/install.html)
* [Usage Guide](https://busypie.readthedocs.io/en/latest/index.html)

## Links

This project drew a lot of inspiration from [Awaitility](https://github.com/awaitility/awaitility).
