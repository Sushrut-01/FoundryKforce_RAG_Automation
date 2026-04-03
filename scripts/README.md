# Scripts Directory

## Overview

This directory contains all automation and utility scripts for the PlayReady RAG testing project.

## Core Scripts

### generate_responses.py
**Purpose:** Generate LLM responses for all test queries

**Usage:**
```bash
python scripts/generate_responses.py
```

**Output:** `results/responses.json` (100 responses)

**Features:**
- Batch response generation
- Azure OpenAI integration (optional)
- Fallback to contextual responses
- Progress tracking

### merge_responses_into_testcases.py
**Purpose:** Merge responses with test cases into Foundry SDK format

**Usage:**
```bash
python scripts/merge_responses_into_testcases.py
```

**Input:**
- `data/test_cases.json`
- `results/responses.json`

**Output:** `data/test_cases_formatted.json` (Foundry SDK compliant)

**Features:**
- Format validation
- Metadata preservation
- Error reporting

### validate_test_cases.py
**Purpose:** Validate test cases against Foundry SDK acceptance criteria

**Usage:**
```bash
python scripts/validate_test_cases.py
```

**Checks:**
- Required fields (query, response, context)
- Field types and formats
- Non-empty content
- Metadata consistency

**Output:** Validation report

### foundry_evaluate_with_azure_kb.py
**Purpose:** Run comprehensive evaluation with Azure Knowledge Base

**Usage:**
```bash
python scripts/foundry_evaluate_with_azure_kb.py
```

**Features:**
- KB integration
- Response quality evaluation
- Performance metrics
- Result aggregation

### upload_to_foundry.py
**Purpose:** Upload evaluation results to Foundry platform

**Usage:**
```bash
python scripts/upload_to_foundry.py
```

**Features:**
- Credential validation
- Batch upload
- Error handling
- Status confirmation

### generate_test_cases.py
**Purpose:** Generate new test cases from templates

**Usage:**
```bash
python scripts/generate_test_cases.py --count 50
```

## Subdirectories

### deploy/
Deployment and infrastructure scripts

### maintenance/
System maintenance and cleanup scripts

### setup/
Initial setup and configuration scripts

## Script Execution Order

For complete workflow:

```bash
# Step 1: Generate responses
python scripts/generate_responses.py

# Step 2: Merge into Foundry format
python scripts/merge_responses_into_testcases.py

# Step 3: Validate format
python scripts/validate_test_cases.py

# Step 4: Run evaluation
python scripts/foundry_evaluate_with_azure_kb.py

# Step 5: Upload results
python scripts/upload_to_foundry.py
```

## Quick Commands

### Quick Check
```bash
# Generate, merge, and validate
python scripts/generate_responses.py && \
python scripts/merge_responses_into_testcases.py && \
python scripts/validate_test_cases.py
```

### Full Pipeline
```bash
# Complete workflow
python scripts/foundry_evaluate_with_azure_kb.py
```

### Validate Only
```bash
python scripts/validate_test_cases.py
```

## Troubleshooting

### Script Not Found
```bash
# Ensure you're in project root
cd c:\Users\SushrutNistane\foundry-playready-rag-testing

# Run with explicit path
python scripts\script_name.py
```

### Import Errors
```bash
# Install dependencies
pip install -r requirements.txt

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Script Hangs
- Check Azure credentials
- Verify network connectivity
- Review logs in `logs/` directory

## Performance Notes

| Script | Input Size | Typical Time |
|--------|-----------|--------------|
| generate_responses.py | 100 queries | 5-10 seconds |
| merge_responses_into_testcases.py | 100 cases | 1-2 seconds |
| validate_test_cases.py | 100 cases | <1 second |
| foundry_evaluate_with_azure_kb.py | 100 cases | 30-60 seconds |
| upload_to_foundry.py | results | 10-20 seconds |

## Development Notes

### Adding New Scripts

1. Create script in `scripts/` directory
2. Add shebang: `#!/usr/bin/env python3`
3. Include docstring
4. Add main() function
5. Update this README

### Script Template

```python
#!/usr/bin/env python3
"""
Brief description of script purpose.
Longer detailed explanation.
"""

import sys
from pathlib import Path

def main():
    """Main execution function."""
    print("Starting process...")
    
    # Your code here
    
    print("Process complete!")

if __name__ == "__main__":
    main()
```

## Related Documentation

- [Getting Started Guide](../docs/guides/GETTING_STARTED.md) - Usage guide
- [API Documentation](../docs/api/README.md) - API reference
- [Data Documentation](../data/README.md) - Data format reference

---

Last Updated: April 2026
Total Scripts: 6 core + 3 categories of utilities
