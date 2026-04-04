# Unit Tests

Optional folder for unit tests of individual components.

## Structure

```
tests/unit/
â”œâ”€â”€ test_config.py           # Config loading tests
â”œâ”€â”€ test_evaluators.py       # Evaluator tests
â”œâ”€â”€ test_utils.py            # Utility function tests
â””â”€â”€ conftest.py              # pytest configuration
```

## Running Unit Tests

```bash
# Run all unit tests
pytest tests/unit/ -v

# Run specific test file
pytest tests/unit/test_config.py -v

# Run with coverage
pytest tests/unit/ --cov=src
```

## Example Test

```python
import pytest
from src.core.config import Config

def test_config_loading():
    config = Config()
    assert config is not None
    assert config.environment in ['dev', 'prod', 'test']
```

To add unit tests, create new test files (test_*.py) in this directory.


