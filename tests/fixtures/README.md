# Test Fixtures

Optional folder for test data and fixtures.

## Structure

```
tests/fixtures/
├── data/                    # Test data files
│   ├── test_queries.json
│   ├── test_responses.json
│   └── sample_kb_docs.json
├── mocks/                   # Mock data
└── __init__.py
```

## Using Fixtures

```python
import pytest
from pathlib import Path

@pytest.fixture
def sample_query():
    return "What is PlayReady?"

@pytest.fixture
def test_data_path():
    return Path(__file__).parent / "data"

def test_with_fixture(sample_query):
    assert sample_query == "What is PlayReady?"
```

## Creating Test Data

1. Create `data/` subdirectory
2. Add JSON files with test data
3. Reference in tests via fixtures

Example:
```bash
mkdir tests/fixtures/data
cat > tests/fixtures/data/test_queries.json << EOF
[
  {
    "id": 1,
    "query": "What is PlayReady?"
  }
]
EOF
```

To add fixtures, create new files in this directory.
