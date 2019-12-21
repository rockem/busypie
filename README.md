# BusyPie
[![GitHub Actions](https://github.com/rockem/busypie/workflows/Build/badge.svg)](https://github.com/rockem/busypie/actions)
[![Release](https://img.shields.io/github/v/release/rockem/busypie)](https://github.com/rockem/busypie/releases)
[![License](http://img.shields.io/:license-apache2.0-blue.svg)](https://github.com/rockem/busypie/blob/master/LICENSE)

Although you wouldn't want to do much busy waiting in your production code, 
Testing is a different matter. When testing asynchronous systems, 
it's very helpful to wait for somescenario to finish its course. 
BusyPie will help you to do busy waiting easily and expressively. 

## Installation
To install it using pip 
```shell script
python -m pip install busypie
```
To include it in *requirements.txt* file add
```text
busypie==0.1
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
```
Specify maximum time to meet the condition 
```python
wait().at_most(FIVE_SECONDS).until(condition_function)
wait_at_most(FIVE_SECONDS).until(condition_function)
wait().at_most(10, SECOND).until(condition_function)
wait_at_most(10, SECONDS).until(condition_function)    
```
Ignoring exceptions thrown from condition function
```python
wait().ignore_exceptions().until(condiction_function)
```

## Credits
This project took a lot of inspiration from [Awaitility](https://github.com/awaitility/awaitility)