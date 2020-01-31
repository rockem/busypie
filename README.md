<p align="center">
  <img src="https://raw.githubusercontent.com/rockem/busypie/master/doc/readme-logo.png" width="120"/>
</p>
<p align="center">
  <strong>Easy and expressive busy-waiting for Python</strong>
</p>
<p align="center">
  <a href="https://github.com/rockem/busypie/actions"><img src="https://github.com/rockem/busypie/workflows/Build/badge.svg"/></a>
  <a href="https://github.com/rockem/busypie/releases"><img src="https://img.shields.io/github/v/release/rockem/busypie"/></a>
  <a href="https://github.com/rockem/busypie/blob/master/LICENSE"><img src="http://img.shields.io/:license-apache2.0-blue.svg"/></a>
</p>

## Intro
Although you wouldn't want to do much busy waiting in your production code, 
Testing is a different matter. When testing asynchronous systems, 
it's very helpful to wait for some scenario to finish its course. 
BusyPie will help you to do busy waiting easily and expressively. 

## Installation
To install it using pip 
```shell script
python -m pip install busypie
```
To include it in *requirements.txt* file add
```text
busypie==0.2.1
```

## Example
Most typical usage will be in test, when we have a scenario 
that require us to wait for something to happen.
```python
def test_event_should_be_dispatched():
    dispatcher.dispatch(event)
    wait().at_most(2, SECONDS).until(event_dispatched)
```

## Usage
Wait for a condition. Default wait time is 10 seconds.
```python
wait().until(condiction_function)
wait().during(condition_function)
```
Specify maximum time to meet the condition 
```python
wait().at_most(FIVE_SECONDS).until(condition_function)
wait_at_most(FIVE_SECONDS).until(condition_function)
wait().at_most(10, SECOND).until(condition_function)
wait_at_most(10, SECONDS).until(condition_function)    
```
Ignoring exceptions thrown from a condition function
```python
given().ignore_exceptions().wait().until(condiction_function)
wait().ignore_exceptions(ZeroDevisionError).until(condiction_function)
```
Changing poll interval
```python
wait().poll_interval(FIVE_HUNDRED_MILLISECONDS).until(condiction_function)
wait().poll_interval(2, SECOND).until(condiction_function)
```
Changing polling delay
```python
wait().poll_delay(SECOND).during(app_is_pending)
```
Changing the default values of busypie
```python
set_default_timeout(60, SECONDS) # Default is 10 seconds
```
Resetting default values
```python
reset_defaults()
```


## Credits
This project took a lot of inspiration from [Awaitility](https://github.com/awaitility/awaitility)
