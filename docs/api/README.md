# API Documentation

## Overview

This document provides comprehensive API reference for the PlayReady RAG evaluation system.

## Core Services

### Response Generator
**Module:** `scripts/generate_responses.py`

Generates LLM responses for test queries.

```python
from scripts.generate_responses import generate_response_for_query

response = generate_response_for_query(
    query="What is PlayReady?",
    query_id=1
)
```

**Parameters:**
- `query` (str): The test query
- `query_id` (int): Unique identifier for the query

**Returns:**
- `str`: Generated response text

### Test Case Merger
**Module:** `scripts/merge_responses_into_testcases.py`

Merges responses with test cases to create Foundry SDK format.

```python
from scripts.merge_responses_into_testcases import merge_responses_into_testcases
from pathlib import Path

formatted = merge_responses_into_testcases(
    test_cases_path=Path("data/raw/test_cases.json"),
    responses_path=Path("artifacts/latest/responses.json"),
    output_path=Path("data/processed/test_cases_formatted.json")
)
```

### Validation Service
**Module:** `scripts/validate_test_cases.py`

Validates test cases against Foundry SDK criteria.

```python
from scripts.validate_test_cases import validate_foundry_sdk_format
from pathlib import Path

results = validate_foundry_sdk_format(
    Path("data/processed/test_cases_formatted.json")
)
```

**Returns:**
```python
{
    "total": 100,
    "valid": 100,
    "with_query": 100,
    "with_response": 100,
    "with_context": 100,
    "status": "READY"
}
```

## Data Models

### Test Case

```json
{
  "id": 1,
  "query": "What is PlayReady?",
  "expected_keywords": ["DRM", "solution", "protect", "content"],
  "category": "general",
  "difficulty": "easy",
  "priority": "low"
}
```

### Formatted Test Case (Foundry SDK)

```json
{
  "query": "What is PlayReady?",
  "response": "PlayReady is a comprehensive digital rights management...",
  "context": [],
  "metadata": {
    "id": 1,
    "category": "general",
    "difficulty": "easy",
    "priority": "low",
    "expected_keywords": ["DRM", "solution", "protect", "content"]
  }
}
```

### Response Object

```json
{
  "id": 1,
  "query": "What is PlayReady?",
  "response": "PlayReady is Microsoft's DRM solution...",
  "timestamp": "2026-04-04T10:30:45.123456"
}
```

## Endpoints (REST API)

### Generate Responses
**Endpoint:** `POST /api/v1/responses/generate`

**Request:**
```json
{
  "test_case_ids": [1, 2, 3],
  "use_azure_kb": true
}
```

**Response:**
```json
{
  "status": "success",
  "responses_generated": 3,
  "file_path": "artifacts/latest/responses.json"
}
```

### Validate Test Cases
**Endpoint:** `POST /api/v1/validate`

**Request:**
```json
{
  "file_path": "data/processed/test_cases_formatted.json"
}
```

**Response:**
```json
{
  "status": "success",
  "total": 100,
  "valid": 100,
  "errors": [],
  "message": "All 100 cases pass Foundry SDK criteria"
}
```

### Run Evaluation
**Endpoint:** `POST /api/v1/evaluate`

**Request:**
```json
{
  "test_file": "data/processed/test_cases_formatted.json",
  "use_azure_kb": true,
  "output_format": "json"
}
```

**Response:**
```json
{
  "status": "success",
  "evaluation_id": "eval_123456",
  "total_cases": 100,
  "results_file": "artifacts/latest/evaluation_results.json"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "BadRequest",
  "message": "Invalid test case format",
  "details": "Missing 'query' field in test case"
}
```

### 404 Not Found
```json
{
  "error": "NotFound",
  "message": "Test file not found",
  "path": "data/raw/test_cases.json"
}
```

### 500 Internal Server Error
```json
{
  "error": "InternalError",
  "message": "Evaluation failed",
  "details": "Azure KB connection error"
}
```

## Configuration

**Environment Variables:**
- `AZURE_OPENAI_API_KEY` - Azure OpenAI API key
- `AZURE_KB_ENDPOINT` - Knowledge base endpoint URL
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `OUTPUT_FORMAT` - Output format (json, csv, markdown)

## Rate Limits

- Response generation: 100 queries/minute
- Validation: 1000 files/minute
- Evaluation: 10 evaluations/minute

## Versioning

Current API Version: **1.0**

Updates and changes are documented in [CHANGELOG](../CHANGELOG.md)

---

Last Updated: April 2026


