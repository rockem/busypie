# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

busypie is a Python library for expressive busy-waiting,
primarily used in tests when waiting for asynchronous conditions to be met.

## Common Commands

```bash
# Install test dependencies
pip install ".[test]"

# Install dev dependencies (includes mypy)
pip install ".[dev]"

# Run all tests
pytest

# Run a single test file
pytest tests/test_wait.py

# Run a specific test
pytest tests/test_wait.py::test_wait_until_true -v

# Lint with flake8
flake8 .

# Type check with mypy
mypy busypie
```

## Architecture

The library uses a fluent builder pattern for constructing wait conditions:

- **`core.py`** - Public API entry points (`wait()`, `wait_at_most()`, `given()`, `set_default_timeout()`)
- **`condition.py`** - `ConditionBuilder` (fluent interface) and `Condition` (configuration holder)
- **`awaiter.py`** - `AsyncConditionAwaiter` handles the actual polling loop and timeout logic
- **`checker.py`** - Evaluator functions (`check`, `negative_check`, `assert_check`) that determine success
- **`runner.py`** - Bridges sync/async by running coroutines in appropriate event loop
- **`durations.py`** - Time constants (`SECOND`, `MINUTE`, `ONE_HUNDRED_MILLISECONDS`, etc.)

Flow: `wait().at_most(2, SECOND).until(condition)` → `ConditionBuilder` → `AsyncConditionAwaiter.wait_for()` →
polls until condition is true or timeout.

## Testing

This project uses TDD as a development method. Which means that each functionality is being tested
before it's implemented. This is to makre sure all business logic is covered and that we don't have uneeded complexed
code.

## Documentation

Documentation files are located in the `docs/` directory and use reStructuredText (RST) format.
