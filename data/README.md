# Data Documentation

## Overview

This directory contains all test data, evaluation datasets, and expected responses for the PlayReady RAG testing project.

## Files

### `raw/test_cases.json`
**Description:** Original 100 test cases for PlayReady QA evaluation.

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

### `raw/playready_kb.pdf` / `raw/playready_kb.txt`
**Description:** Source knowledge base used to populate RAG context locally.

### `processed/test_cases_formatted.json`
**Description:** Generated evaluation-ready test cases with `query`, `response`, and `metadata`.

### `processed/test_cases_with_kb.json`
**Description:** Formatted test cases enriched with KB context chunks.

### `processed/test_cases_smoke.json`
**Description:** Small subset for quick smoke validation runs.

### `processed/test_cases_regression.json`
**Description:** Larger subset for regression testing.

### `archived/`
**Description:** Timestamped snapshots of previous test input files created automatically before new runs.

## Data Generation Pipeline

### Step 1: Response Generation
```bash
python scripts/generate_responses.py
â†’ Output: artifacts/latest/responses.json
```

### Step 2: Format Merging
```bash
python scripts/merge_responses_into_testcases.py
â†’ Output: data/processed/test_cases_formatted.json
```

### Step 3: Validation
```bash
python scripts/validate_test_cases.py
â†’ Validates Foundry SDK compliance
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
- âœ… All queries are unique
- âœ… All queries are non-empty
- âœ… Categories are valid
- âœ… Difficulty levels are consistent
- âœ… Expected keywords are relevant
- âœ… 100 test cases total

### Foundry SDK Compliance
```
âœ… query field: present and non-empty
âœ… response field: present for all cases
âœ… context field: present for all cases
âœ… metadata: preserved and accessible
â†’ Status: READY FOR EVALUATION
```

## Usage Examples

### Load Test Cases
```python
import json

with open("data/raw/test_cases.json") as f:
    test_data = json.load(f)
    
for test_case in test_data["test_cases"]:
    print(f"ID: {test_case['id']}")
    print(f"Query: {test_case['query']}")
    print(f"Category: {test_case['category']}")
```

### Access Formatted Cases
```python
import json

with open("data/processed/test_cases_formatted.json") as f:
    formatted_cases = json.load(f)
    
for case in formatted_cases:
    print(f"Query: {case['query']}")
    print(f"Response: {case['response']}")
    print(f"Context: {case['context']}")
```

## Data Backup

Backups are maintained in `data/archived/` directory.

To restore from backup:
```bash
cp data/archived/test_cases_backup_YYYYMMDD.json data/raw/test_cases.json
```

## Related Resources

- [Getting Started Guide](../guides/GETTING_STARTED.md) - Data generation guide
- [API Documentation](../api/README.md) - API reference
- [Code Examples](../examples/README.md) - Usage examples

---

Last Updated: April 2026
File Count: 4 core data files
Test Cases: 100 (all Foundry SDK compliant)


