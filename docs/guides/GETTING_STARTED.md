# Getting Started Guide

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip or conda
- Git
- 2GB disk space (including venv)
- Azure OpenAI credentials (optional)

### Step 1: Clone Repository

```bash
git clone https://github.com/Sushrut-01/FoundryKforce_RAG_Automation.git
cd foundry-playready-rag-testing
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name

# Knowledge Base Configuration
AZURE_KB_ENDPOINT=https://your-kb.cognitiveservices.azure.com/
AZURE_KB_KEY=your_kb_key_here

# Foundry Configuration
FOUNDRY_API_KEY=your_foundry_key
FOUNDRY_ENDPOINT=https://foundry.example.com/api

# Logging
LOG_LEVEL=INFO
```

## Running the Project

### Quick Start: Generate & Validate Test Data

**1. Generate responses for all test queries:**
```bash
python scripts/generate_responses.py
```

Expected output:
```
======================================================================
Generating responses for 100 test queries...
======================================================================
✓ Generated response 10/100: ...
✓ Generated response 20/100: ...
...
✅ Generated 100 responses
✅ Saved to: results/responses.json
```

**2. Merge responses into Foundry SDK format:**
```bash
python scripts/merge_responses_into_testcases.py
```

Expected output:
```
✅ All cases passed Foundry SDK format validation
✅ Formatted 100 test cases
✅ Saved to: data/test_cases_formatted.json
Status: READY FOR FOUNDRY SDK ✓
```

**3. Validate format compliance:**
```bash
python scripts/validate_test_cases.py
```

Expected output:
```
Total test cases: 100
With 'query' field: 100/100 ✓
With 'response' field: 100/100 ✓
With 'context' field: 100/100 ✓
Valid cases (all required fields): 100/100

✅ ALL 100 CASES PASS FOUNDRY SDK CRITERIA ✅
```

### Run Integration Tests

**Run all integration tests:**
```bash
pytest tests/integration/ -v
```

**Run specific test:**
```bash
pytest tests/integration/test_playready_qa.py::test_response_generation -v
```

### Run Evaluation

**Full evaluation with Azure KB:**
```bash
python scripts/foundry_evaluate_with_azure_kb.py
```

**Upload results to Foundry:**
```bash
python scripts/upload_to_foundry.py
```

## Project Structure Guide

### data/
- `test_cases.json` - Original 100 test cases
- `test_cases_formatted.json` - Foundry SDK compliant format (generated)
- `test_queries.json` - Query dataset

### scripts/
- `generate_responses.py` - LLM response generation
- `validate_test_cases.py` - Format validation
- `merge_responses_into_testcases.py` - Data merging
- `foundry_evaluate_with_azure_kb.py` - Main evaluation runner
- `upload_to_foundry.py` - Foundry platform upload

### src/
- `core/` - Core functionality (config, uploaders)
- `agents/` - Agent implementations
- `evaluators/` - Evaluation metrics
- `utils/` - Utility functions

### tests/
- `unit/` - Unit tests for components
- `integration/` - Integration tests
- `fixtures/` - Test data and fixtures

### results/
- `responses.json` - Generated responses
- Evaluation output files (generated)

## Common Tasks

### Task 1: Generate Test Responses
```bash
cd c:\Users\SushrutNistane\foundry-playready-rag-testing
python scripts\generate_responses.py
```

### Task 2: Format for Foundry SDK
```bash
python scripts\merge_responses_into_testcases.py
```

### Task 3: Validate Compliance
```bash
python scripts\validate_test_cases.py
```

### Task 4: Run Full Evaluation
```bash
python scripts\foundry_evaluate_with_azure_kb.py
```

### Task 5: Upload to Foundry
```bash
python scripts\upload_to_foundry.py
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named..."

**Solution:** Ensure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: "Azure credentials not found"

**Solution:** Set environment variables before running:
```bash
# Windows PowerShell
$env:AZURE_OPENAI_API_KEY = "your_key_here"

# Or edit .env file
AZURE_OPENAI_API_KEY=your_key_here
```

### Issue: "Test cases validation failed"

**Solution:** Check test case format:
```bash
python scripts\validate_test_cases.py
# Review the detailed error report
```

### Issue: "Connection timeout to Azure KB"

**Solution:** Verify endpoint and credentials:
```bash
# Test connectivity
curl https://your-kb.cognitiveservices.azure.com/
```

## Next Steps

1. ✅ Generate test responses
2. ✅ Validate Foundry SDK format
3. ✅ Run integration tests
4. ✅ Execute full evaluation
5. ✅ Upload results to Foundry
6. ✅ Review and analyze results

## Additional Resources

- [API Documentation](../api/README.md) - API reference
- [Code Examples](../examples/README.md) - Implementation examples
- [Main README](../../README.md) - Project overview

---

**Support:** For issues, check repository issues or contact the development team.

Last Updated: April 2026
