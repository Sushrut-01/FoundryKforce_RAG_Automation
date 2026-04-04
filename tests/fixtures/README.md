# Test Fixtures

Optional folder for test data and fixtures.

## Structure

```
tests/fixtures/
â”œâ”€â”€ data/                    # Test data files
â”‚   â”œâ”€â”€ test_queries.json
â”‚   â”œâ”€â”€ test_responses.json
â”‚   â””â”€â”€ sample_kb_docs.json
â”œâ”€â”€ mocks/                   # Mock data
â””â”€â”€ __init__.py
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


