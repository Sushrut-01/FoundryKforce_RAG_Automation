# Data Documentation

## Overview

This directory contains all test data, evaluation datasets, and expected responses for the PlayReady RAG testing project.

## Files

### test_cases.json
**Description:** Original 100 test cases for PlayReady QA evaluation

**Format:**
```json
{
  "test_suite": "PlayReady RAG QA Testing",
  "version": "1.0",
  "total_cases": 100,
  "test_cases": [
    {
      "id": 1,
      "query": "What is PlayReady?",
      "expected_keywords": ["DRM", "solution", "protect", "content"],
      "category": "general",
      "difficulty": "easy",
      "priority": "low"
    }
  ]
}
```

**Categories:**
- `general` - General PlayReady concepts
- `implementation` - Implementation and deployment
- `troubleshooting` - Problem resolution
- `advanced` - Advanced features and scenarios

**Difficulty Levels:**
- `easy` - Basic concepts
- `medium` - Intermediate knowledge
- `hard` - Advanced topics

### test_cases_formatted.json
**Description:** Test cases formatted for Foundry SDK evaluation (GENERATED)

**Format:** JSON array with Foundry SDK structure
```json
[
  {
    "query": "What is PlayReady?",
    "response": "PlayReady is Microsoft's digital rights management...",
    "context": [],
    "metadata": {
      "id": 1,
      "category": "general",
      "difficulty": "easy"
    }
  }
]
```

**Status:** ✅ 100/100 cases Foundry SDK compliant

### test_queries.json
**Description:** Additional query dataset for testing

**Usage:** Extended test queries for performance and scalability testing

### expected_responses.json
**Description:** Baseline expected responses for evaluation

**Format:**
```json
{
  "1": "PlayReady is a comprehensive DRM solution...",
  "2": "PlayReady protects video and audio content..."
}
```

**Purpose:** Serves as baseline for response quality evaluation

## Data Generation Pipeline

### Step 1: Response Generation
```bash
python scripts/generate_responses.py
→ Output: results/responses.json
```

### Step 2: Format Merging
```bash
python scripts/merge_responses_into_testcases.py
→ Output: data/test_cases_formatted.json
```

### Step 3: Validation
```bash
python scripts/validate_test_cases.py
→ Validates Foundry SDK compliance
```

## Test Distribution

### By Category
- General: 40 cases (40%)
- Implementation: 35 cases (35%)
- Troubleshooting: 15 cases (15%)
- Advanced: 10 cases (10%)

### By Difficulty
- Easy: 30 cases (30%)
- Medium: 50 cases (50%)
- Hard: 20 cases (20%)

### By Priority
- Low: 40 cases (40%)
- Medium: 45 cases (45%)
- High: 15 cases (15%)

## Sample Test Cases

### Easy Test Case
```json
{
  "id": 1,
  "query": "What is PlayReady?",
  "category": "general",
  "difficulty": "easy",
  "priority": "low",
  "expected_keywords": ["DRM", "solution", "protect", "content"]
}
```

### Medium Test Case
```json
{
  "id": 45,
  "query": "How to implement PlayReady with adaptive streaming?",
  "category": "implementation",
  "difficulty": "medium",
  "priority": "medium",
  "expected_keywords": ["adaptive", "bitrate", "streaming", "implementation"]
}
```

### Hard Test Case
```json
{
  "id": 95,
  "query": "What are the performance implications of PlayReady on embedded systems?",
  "category": "advanced",
  "difficulty": "hard",
  "priority": "high",
  "expected_keywords": ["performance", "embedded", "optimization", "resources"]
}
```

## Data Quality

### Validation Checklist
- ✅ All queries are unique
- ✅ All queries are non-empty
- ✅ Categories are valid
- ✅ Difficulty levels are consistent
- ✅ Expected keywords are relevant
- ✅ 100 test cases total

### Foundry SDK Compliance
```
✅ query field: present and non-empty
✅ response field: present for all cases
✅ context field: present for all cases
✅ metadata: preserved and accessible
→ Status: READY FOR EVALUATION
```

## Usage Examples

### Load Test Cases
```python
import json

with open("data/test_cases.json") as f:
    test_data = json.load(f)
    
for test_case in test_data["test_cases"]:
    print(f"ID: {test_case['id']}")
    print(f"Query: {test_case['query']}")
    print(f"Category: {test_case['category']}")
```

### Access Formatted Cases
```python
import json

with open("data/test_cases_formatted.json") as f:
    formatted_cases = json.load(f)
    
for case in formatted_cases:
    print(f"Query: {case['query']}")
    print(f"Response: {case['response']}")
    print(f"Context: {case['context']}")
```

## Data Backup

Backups are maintained in `test_cases_archive/` directory.

To restore from backup:
```bash
cp test_cases_archive/test_cases_backup_YYYYMMDD.json data/test_cases.json
```

## Related Resources

- [Getting Started Guide](../guides/GETTING_STARTED.md) - Data generation guide
- [API Documentation](../api/README.md) - API reference
- [Code Examples](../examples/README.md) - Usage examples

---

Last Updated: April 2026
File Count: 4 core data files
Test Cases: 100 (all Foundry SDK compliant)
