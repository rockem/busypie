<p align="center">
  <img src="https://raw.githubusercontent.com/rockem/busypie/master/docs/source/_static/busypie_logo.png" width="120"/>
</p>
<p align="center">
  <strong>Easy and expressive busy-waiting for Python</strong>
</p>
<p align="center">
  <a href="https://github.com/rockem/busypie/actions"><img src="https://github.com/rockem/busypie/workflows/Build/badge.svg"/></a>
  <a href="https://github.com/rockem/busypie/releases"><img src="https://img.shields.io/github/v/release/rockem/busypie"/></a>
  <a href="https://github.com/rockem/busypie/blob/master/LICENSE"><img src="http://img.shields.io/:license-apache2.0-blue.svg"/></a>
</p>


Although you wouldn't want to do much busy waiting in your production code, 
testing is a different matter. When testing asynchronous systems, 
it's very helpful to wait for some scenario to finish its course. 
busypie helps you perform busy waiting easily and expressively. 

## Quickstart
Most typical usage will be in test, when we have a scenario 
that require us to wait for something to happen.
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
