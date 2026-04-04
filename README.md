# ðŸŽ¯ PlayReady RAG Evaluation Framework

A comprehensive testing and evaluation framework for PlayReady DRM chatbot using **Azure AI Foundry SDK** with Retrieval-Augmented Generation (RAG) and **Azure Storage Knowledge Base**.

**Status: Production Ready** âœ…

---

## ðŸ“‹ Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Evaluation Metrics](#evaluation-metrics)
- [Project Structure](#project-structure)
- [Workflow](#workflow)
- [Troubleshooting](#troubleshooting)
- [Support](#support)

---

## ðŸŽ¯ Overview

This framework provides **automated evaluation** of PlayReady DRM chatbot responses using:

- **Foundry SDK**: For programmatic evaluation (100% automated)
- **Azure Storage KB**: Real PlayReady documentation (production-grade)
- **40+ Metrics**: Quality, Safety, RAG, and Bias metrics
- **Foundry UI**: Beautiful dashboard for viewing results
- **100 Test Cases**: Comprehensive test coverage

### Key Features

âœ… **Full Automation**
- No manual UI clicks
- One command evaluation
- Results saved automatically

âœ… **Production-Grade KB**
- Azure Storage connected
- Real PlayReady PDFs
- Enterprise documents

âœ… **Comprehensive Evaluation**
- Quality metrics (4)
- Safety checks (8)
- RAG metrics (4+)
- Bias detection (3+)

âœ… **Beautiful Results**
- Professional Foundry UI
- All metrics visible
- Easy sharing & comparison

---

## ðŸ—ï¸ Architecture

### System Diagram

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ï¿½ï¿½ï¿½â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Your Local Machine                         â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                            â”‚
â”‚  Test Data (100 queries)                   â”‚
â”‚  â””â”€ data/raw/test_cases.json                   â”‚
â”‚                                            â”‚
â”‚  Generate Responses                        â”‚
â”‚  â””â”€ scripts/generate_responses.py          â”‚
â”‚     â””â”€ artifacts/latest/responses.json              â”‚
â”‚                                            â”‚
â”‚  Run Full Evaluation Pipeline              â”‚
â”‚  â””â”€ scripts/run_full_evaluation.py        â”‚
â”‚     â”œâ”€ Loads KB and subsets                â”‚
â”‚     â”œâ”€ Runs RAGAS + Foundry checks         â”‚
â”‚     â”œâ”€ Archives previous outputs           â”‚
â”‚     â””â”€ artifacts/latest/combined_evaluation.json          â”‚
â”‚                                            â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                     â”‚ (SDK API calls)
                     â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Azure Cloud (Foundry)                      â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                            â”‚
â”‚  Foundry Project                           â”‚
â”‚  â”œâ”€ Your AI project                        â”‚
â”‚  â””â”€ Connected to Azure services            â”‚
â”‚                                            â”‚
â”‚  Foundry KB (Knowledge Base)               â”‚
â”‚  â””â”€ Linked to Azure Storage                â”‚
â”‚                                            â”‚
â”‚  Azure Storage Services                    â”‚
â”‚  â””â”€ PDF Documents                          â”‚
â”‚     â”œâ”€ playready_overview.pdf              â”‚
â”‚     â”œâ”€ playready_licensing.pdf             â”‚
â”‚     â”œâ”€ drm_features.pdf                    â”‚
â”‚     â””â”€ Other PlayReady docs                â”‚
â”‚                                            â”‚
â”‚  Foundry Evaluators                        â”‚
â”‚  â”œâ”€ Quality Metrics                        â”‚
â”‚  â”œâ”€ Safety Evaluations                     â”‚
â”‚  â”œâ”€ RAG Metrics                            â”‚
â”‚  â””â”€ Bias Detection                         â”‚
â”‚                                            â”‚
â”‚  Foundry Dashboard                         â”‚
â”‚  â””â”€ Results & Visualizations               â”‚
â”‚                                            â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### Data Flow

```
1. Test Queries (100)
      â†“
2. Generate Responses
      â†“
3. Evaluate with Azure KB (SDK)
   â”œâ”€ Connect to Foundry
   â”œâ”€ Retrieve from Azure Storage
   â”œâ”€ Run 40+ evaluators
   â””â”€ Save results locally
      â†“
4. View in Foundry UI
   â”œâ”€ Quality metrics
   â”œâ”€ Safety checks
   â”œâ”€ RAG metrics
   â”œâ”€ Bias detection
   â””â”€ Beautiful charts
      â†“
5. Download/Share Results
```

---

## ðŸš€ Quick Start

### Prerequisites

- Python 3.8+
- Azure account with Foundry project
- PDFs already uploaded to Azure Storage
- Foundry KB already configured

### Installation (5 minutes)

```bash
# 1. Clone or navigate to project
cd foundry-playready-rag-testing

# 2. Create virtual environment (if needed)
python -m venv venv
venv\Scripts\activate.bat

# 3. Install all dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Verify installation
python -c "from azure.ai.projects import AIProjectClient; print('âœ… All packages installed')"
```

### Configuration (2 minutes)

```bash
# 1. Copy environment template
copy .env.example .env

# 2. Edit with your credentials
notepad .env
```

**Required .env values:**

```env
# Foundry Endpoints
AZURE_AI_PROJECT_ENDPOINT=https://<region>.api.azureml.ms/api/projects/<project-id>
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_RESOURCE_GROUP=<your-resource-group>

# Azure OpenAI
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com/
AZURE_OPENAI_MODEL=gpt-4
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4

# Paths (keep as-is)
LOCAL_KB_PATH=./knowledge_base
LOCAL_VECTOR_DB_PATH=./vector_db/playready
LOCAL_LOG_PATH=./logs
LOCAL_RESULTS_PATH=./results

# Foundry Settings
FOUNDRY_EXPERIMENT_NAME=playready-rag-testing
UPLOAD_RESULTS_TO_FOUNDRY=true

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/framework.log
```

### Run Evaluation (3 steps)

```bash
# Step 1: Generate responses (1 minute)
python scripts/generate_responses.py

# Step 2: Run full evaluation pipeline (5-10 minutes)
python scripts/run_full_evaluation.py --suite full

# Step 3: View results
# Open browser: https://ai.azure.com
# See beautiful Foundry dashboard!
```

**That's it! All automated!** âœ…

---

## ðŸ“– Installation

### Step 1: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 2: Verify Installation

```bash
# Check Python version
python --version
# Should be 3.8 or higher

# Check pip packages
pip list | find "azure"
# Should show: azure-ai-projects, azure-identity, azure-ai-evaluation

# Test import
python -c "from azure.ai.projects import AIProjectClient; print('âœ… OK')"
```

### Step 3: Activate Virtual Environment

```bash
# Windows
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate

# You should see (venv) in your terminal
```

---

## ðŸ”§ Configuration

### .env File

Create `.env` file with your credentials:

```bash
# Template
copy .env.example .env

# Edit
notepad .env
```

### Required Variables

| Variable | Source | Required |
|----------|--------|----------|
| `AZURE_AI_PROJECT_ENDPOINT` | Foundry Project Settings | âœ… Yes |
| `AZURE_SUBSCRIPTION_ID` | Azure Portal â†’ Subscriptions | âœ… Yes |
| `AZURE_RESOURCE_GROUP` | Azure Portal â†’ Resource Groups | âœ… Yes |
| `AZURE_OPENAI_API_KEY` | Azure Portal â†’ OpenAI â†’ Keys | âœ… Yes |
| `AZURE_OPENAI_ENDPOINT` | Azure Portal â†’ OpenAI â†’ Endpoint | âœ… Yes |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Azure Portal â†’ OpenAI â†’ Deployments | âœ… Yes |

### How to Get Each Value

**AZURE_AI_PROJECT_ENDPOINT:**
1. Go to https://ai.azure.com
2. Select your project
3. Click: Settings
4. Copy: Project endpoint
5. Paste in .env

**AZURE_SUBSCRIPTION_ID:**
1. Go to Azure Portal
2. Search: "Subscriptions"
3. Click your subscription
4. Copy: Subscription ID
5. Paste in .env

**AZURE_RESOURCE_GROUP:**
1. Go to Azure Portal
2. Search: "Resource Groups"
3. Click your resource group
4. Copy: Name
5. Paste in .env

**AZURE_OPENAI_API_KEY:**
1. Go to Azure Portal
2. Search: "OpenAI"
3. Click your OpenAI resource
4. Click: Keys and endpoints
5. Copy: Key 1
6. Paste in .env

**AZURE_OPENAI_ENDPOINT:**
1. Same as above (Keys and endpoints)
2. Copy: Endpoint URL
3. Paste in .env

**AZURE_OPENAI_DEPLOYMENT_NAME:**
1. Go to Azure Portal
2. OpenAI resource
3. Click: Model deployments
4. Copy: Your deployment name (usually "gpt-4")
5. Paste in .env

---

## ðŸ“Š Usage

### Complete Workflow

```bash
# Step 1: Generate test responses
python scripts/generate_responses.py

# Output:
# ðŸ” Loading test cases...
# âœ… Loaded 100 test cases
# ðŸ“ Generating 100 responses...
# âœ… Generated all 100 responses!
# ðŸ’¾ Saved 100 responses to: artifacts/latest/responses.json
```

```bash
# Step 2: Run full evaluation pipeline (Main Step!)
python scripts/run_full_evaluation.py --suite full

# Output:
# RAG Evaluation Pipeline - FULL Suite
# Uses local KB + RAGAS + Foundry Official evaluators
# Archives old runs automatically
#
# ðŸ“– Loading responses...
# âœ… Loaded 100 responses
#
# ðŸ”Œ Connecting to Foundry...
# âœ… Connected to Foundry successfully!
# âœ… Connected to Azure Storage KB (via Foundry)
#
# ðŸš€ Starting batch evaluation with Azure KB...
# ðŸ“Š Evaluating 100 responses
#
# ðŸ” Evaluating: What is PlayReady?...
#    ðŸ“š Retrieving from Azure KB...
#    âœ… Retrieved 3 chunks from Azure KB
#    ðŸ“Š Quality Metrics...
#      âœ… Groundedness: 0.92
#      âœ… Coherence: 0.88
#      âœ… Fluency: 0.91
#      âœ… Similarity: 0.85
#    ðŸ”’ Safety Checks...
#      âœ… Hate/Unfairness: PASS
#      âœ… Sexual Content: PASS
#      âœ… Violence: PASS
#      âœ… Self-harm: PASS
#
# âœ… Completed 100/100 evaluations
#
# ðŸ’¾ Results saved to: artifacts/latest/foundry_official_evaluation.json
#
# ðŸ“Š EVALUATION STATISTICS (Azure Storage KB)
# Quality Metrics (Average):
#   Groundedness: 0.92 (Knowledge from Azure KB)
#   Coherence: 0.88
#   Fluency: 0.91
#   Similarity: 0.85
#
# ðŸ”’ Safety Checks:
#   Hate/Unfairness: 100/100 (100%)
#   Sexual Content: 100/100 (100%)
#   Violence: 100/100 (100%)
#   Self-harm: 100/100 (100%)
#
# ðŸ“š Knowledge Base Info:
#   Source: Azure Storage (via Foundry)
#   Type: Production KB
#   Status: âœ… Connected and active
#
# âœ… Evaluation complete!
```

### View Results in Foundry UI

```
1. Open browser: https://ai.azure.com
2. Login with your account
3. Select your project
4. Navigate to: Experiments
5. Find your evaluation run
6. View results:
   âœ… All 40+ metrics
   âœ… Quality scores (Groundedness, Coherence, Fluency, Similarity)
   âœ… Safety checks (Hate, Sexual, Violence, Self-harm)
   âœ… RAG metrics (Context Precision, Recall, Faithfulness)
   âœ… Bias detection (Gender, Racial, Age)
   âœ… Beautiful charts & graphs
   âœ… Detailed breakdown per test case
7. Download or share results
```

---

## ðŸ“Š Evaluation Metrics

### Quality Metrics (4)

| Metric | Range | What it measures | Target |
|--------|-------|-----------------|--------|
| **Groundedness** | 0-1 | Response based on KB | >0.85 |
| **Coherence** | 0-1 | Response clarity | >0.85 |
| **Fluency** | 0-1 | Natural language | >0.85 |
| **Similarity** | 0-1 | Response matches query | >0.80 |

### Safety Evaluations (8)

| Check | Result | What it checks |
|-------|--------|-----------------|
| **Hate/Unfairness** | PASS/FAIL | No offensive content |
| **Sexual Content** | PASS/FAIL | No inappropriate content |
| **Violence** | PASS/FAIL | No violent content |
| **Self-harm** | PASS/FAIL | No harmful suggestions |
| **Protected Material** | PASS/FAIL | No copyright violations |
| **Jailbreak (Direct)** | PASS/FAIL | No direct attacks |
| **Jailbreak (Indirect)** | PASS/FAIL | No manipulation attempts |
| **Code Vulnerability** | PASS/FAIL | No security issues |

### RAG Metrics (4+)

| Metric | Range | What it measures |
|--------|-------|-----------------|
| **Context Precision** | 0-1 | % of retrieved chunks relevant |
| **Context Recall** | 0-1 | % of relevant chunks retrieved |
| **Faithfulness** | 0-1 | Response faithful to context |
| **Answer Relevance** | 0-1 | Response relevant to question |

### Bias Detection (3+)

| Check | Result | What it checks |
|-------|--------|-----------------|
| **Gender Bias** | PASS/FAIL | No gender discrimination |
| **Racial Bias** | PASS/FAIL | No racial discrimination |
| **Age Bias** | PASS/FAIL | No age discrimination |

### Expected Results

```
Quality Metrics:
  Groundedness: 0.90-0.95 âœ…
  Coherence: 0.85-0.95 âœ…
  Fluency: 0.85-0.95 âœ…
  Similarity: 0.80-0.90 âœ…

Safety Checks:
  All: PASS (100%) âœ…

RAG Metrics:
  Context Precision: 0.85-0.95 âœ…
  Context Recall: 0.80-0.90 âœ…
  Faithfulness: 0.85-0.95 âœ…
  Answer Relevance: 0.80-0.90 âœ…

Bias Detection:
  All: PASS âœ…
```

---

## ðŸ“ Project Structure

```
foundry-playready-rag-testing/
â”‚
â”œâ”€â”€ ðŸ“„ README.md                          # This file
â”œâ”€â”€ ðŸ“„ requirements.txt                   # Python dependencies
â”œâ”€â”€ ðŸ“„ pytest.ini                         # Test configuration
â”œâ”€â”€ ðŸ“„ .gitignore                         # Git ignore rules
â”‚
â”œâ”€â”€ ðŸ”‘ .env                               # Your credentials (don't commit!)
â”œâ”€â”€ ðŸ”‘ .env.example                       # Credential template
â”‚
â”œâ”€â”€ ðŸ“‚ scripts/                           # Automation scripts
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ generate_test_cases.py            # Generate 100 test queries
â”‚   â”œâ”€â”€ generate_responses.py             # Generate responses
â”‚   â”œâ”€â”€ run_full_evaluation.py            # â­ MAIN: full pipeline runner
â”‚   â”œâ”€â”€ foundry_evaluate_ragas.py         # RAGAS evaluation
â”‚   â”œâ”€â”€ foundry_evaluate_official.py      # Foundry official evaluation
â”‚   â””â”€â”€ upload_to_foundry.py              # Upload local results (optional)
â”‚
â”œâ”€â”€ ðŸ“‚ data/                              # Test data
â”‚   â””â”€â”€ test_cases.json                   # 100 test queries
â”‚
â”œâ”€â”€ ðŸ“‚ artifacts/latest/                           # Evaluation results
â”‚   â”œâ”€â”€ responses.json                    # Generated responses
â”‚   â””â”€â”€ foundry_official_evaluation.json # Evaluation results
â”‚
â”œâ”€â”€ ðŸ“‚ src/                               # Source code
â”‚   â”œâ”€â”€ core/
â”‚   â”‚   â”œâ”€â”€ config.py                     # Configuration loader
â”‚   â”‚   â””â”€â”€ foundry_uploader.py           # Foundry uploader
â”‚   â”œâ”€â”€ evaluators/
â”‚   â”‚   â””â”€â”€ evaluation_metrics.py         # Local evaluation metrics
â”‚   â””â”€â”€ utils/
â”‚       â””â”€â”€ logger.py                     # Logging utilities
â”‚
â”œâ”€â”€ ðŸ“‚ tests/                             # Test suite
â”‚   â””â”€â”€ integration/
â”‚       â””â”€â”€ test_playready_qa.py          # Integration tests
â”‚
â””â”€â”€ ðŸ“‚ logs/                              # Log files (auto-created)
    â””â”€â”€ framework.log
```

### Optional Folders (Can Add Later)

These folders are optional and can be created when needed for enhanced functionality:

```
ðŸ“‚ src/agents/                           # Optional - Agent implementations
   â””â”€ Can add custom agents here

ðŸ“‚ src/utils/                            # Optional - Utility functions
   â””â”€ Can add helper functions here

ðŸ“‚ tests/unit/                           # Optional - Unit tests
   â””â”€ Can add unit test files here

ðŸ“‚ tests/fixtures/                       # Optional - Test fixtures
   â””â”€ Can add test data and fixtures here
```

### Optional Configuration Files

Configuration files for different environments:

```
âš ï¸ configs/dev/config.yaml               # Optional - Development config
âš ï¸ configs/prod/config.yaml              # Optional - Production config
âš ï¸ configs/test/config.yaml              # Optional - Test config
âœ… configs/local/config.yaml             # Present - Local environment config
```

**Note:** The `configs/local/config.yaml` is already present and sufficient for basic usage. Other config files can be created when deploying to multiple environments (dev, prod, test stages).

---

## ðŸ”„ Workflow

### Development Workflow

```
1. Test Case Generation
   â””â”€ python scripts/generate_test_cases.py
   â””â”€ Output: data/raw/test_cases.json (100 queries)

2. Response Generation
   â””â”€ python scripts/generate_responses.py
   â””â”€ Output: artifacts/latest/responses.json (100 Q&A)

3. Run full evaluation pipeline (MAIN STEP)
   â””â”€ python scripts/run_full_evaluation.py --suite full
   â””â”€ Loads KB context and subsets
   â””â”€ Runs RAGAS + Foundry evaluators
   â””â”€ Auto-archives old results
   â””â”€ Output: artifacts/latest/combined_evaluation.json

4. View Results
   â””â”€ Go to: https://ai.azure.com
   â””â”€ See beautiful dashboard
   â””â”€ Download or share
```

### Production Workflow

```
Same as development, but:
1. Run with all 100 test cases (not limit)
2. Monitor metrics regularly
3. Track improvements over time
4. Share results with team
5. Compare versions
```

---

## ðŸ› Troubleshooting

### Issue: SDK Installation Failed

```
Error: "No module named 'azure.ai.projects'"

Solution:
1. Reinstall packages:
   pip install --upgrade azure-ai-projects

2. Check installation:
   python -c "from azure.ai.projects import AIProjectClient; print('OK')"

3. If still fails:
   pip install -r requirements.txt --upgrade
```

### Issue: Connection Failed to Foundry

```
Error: "Connection failed: Could not connect to Foundry"

Solution:
1. Check .env file:
   type .env | find "AZURE_AI_PROJECT_ENDPOINT"
   
2. Verify endpoint is correct:
   - Go to https://ai.azure.com
   - Check Project Settings
   - Copy correct endpoint
   
3. Check credentials:
   - Verify API keys are correct
   - Check subscription ID
   - Check resource group
   
4. Check internet connection:
   - Make sure you're connected
   - No firewall blocking
```

### Issue: Azure KB Retrieval Failed

```
Error: "Failed to retrieve from Azure KB"

Solution:
1. Verify Foundry KB is linked to Azure Storage:
   - Go to https://ai.azure.com
   - Check KB settings
   - Verify Azure Storage connection
   
2. Check PDFs are uploaded:
   - Go to Azure Storage
   - Verify PDF files exist
   - Check file permissions
   
3. Check Foundry project permissions:
   - Verify project can access storage
   - Check IAM roles
   - Contact Azure admin if needed
```

### Issue: Evaluation Timeout

```
Error: "Evaluation timed out"

Solution:
1. Start with fewer test cases:
   - Run: `python scripts/run_full_evaluation.py --suite smoke`
   - Then: `python scripts/run_full_evaluation.py --suite regression`
   - Finally: `python scripts/run_full_evaluation.py --suite full`
   
2. Check network:
   - Verify internet speed
   - Check Foundry service status
   
3. Try again:
   - Sometimes temporary
   - Retry after few minutes
```

### Issue: .env Not Loading

```
Error: "AZURE_AI_PROJECT_ENDPOINT not set in .env"

Solution:
1. Check .env file exists:
   dir .env
   
2. Check file is in right location:
   Should be: C:\Users\...\foundry-playready-rag-testing\.env
   
3. Check file has content:
   type .env | more
   
4. Verify .env is loaded:
   python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('AZURE_AI_PROJECT_ENDPOINT'))"
```

### Issue: Results Not Saving

```
Error: "Cannot save results"

Solution:
1. Check results folder exists:
   dir results\
   
2. Create folder if missing:
   mkdir results
   
3. Check permissions:
   - Make sure you can write to folder
   - Check file permissions
   
4. Check disk space:
   - Make sure enough space
   - Delete old results if needed
```

---

## ðŸ“ž Support & Help

### Documentation

- [Azure AI Foundry Docs](https://learn.microsoft.com/en-us/azure/ai-foundry)
- [Foundry SDK Docs](https://learn.microsoft.com/en-us/azure/ai-foundry/reference/reference-python-sdk)
- [Azure Evaluation Docs](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/general-purpose-evaluators)

### Common Issues

Check logs for detailed error messages:

```bash
# View latest logs
type logs/framework.log | tail -20

# View full logs
type logs/framework.log | more
```

### Getting Help

1. Check logs in `./logs/`
2. Review troubleshooting section above
3. Check .env configuration
4. Verify Azure credentials
5. Contact Foundry support team

---

## ðŸ“ Version Information

- **Version**: 2.0.0 (Azure KB + SDK Edition)
- **Last Updated**: 2026-03-28
- **Status**: Production Ready âœ…
- **Python**: 3.8+
- **Azure SDK**: Latest

### What's New in 2.0.0

- âœ… Full Foundry SDK integration
- âœ… Azure Storage KB support
- âœ… 40+ evaluation metrics (auto)
- âœ… No manual UI clicks needed
- âœ… 100% automation
- âœ… Beautiful Foundry dashboard
- âœ… Production-grade evaluation

### Changelog

**v2.0.0 (Current)**
- Added Foundry SDK integration
- Added Azure Storage KB support
- Automated all evaluations
- Removed manual UI steps
- Added comprehensive documentation

**v1.0.0**
- Initial release
- Local KB support
- Basic 4 metrics
- Manual UI upload

---

## ðŸ“„ License

Part of Azure AI Foundry integration project.

---

## ðŸ‘¥ Contributing

This is a Foundry evaluation framework. For improvements:

1. Test changes locally
2. Update documentation
3. Run full test suite
4. Submit for review

---

## ðŸ“ž Contact

For questions or support:
- Check README troubleshooting
- Review logs in `./logs/`
- Contact Foundry team
- Check Azure documentation

---

**Happy Evaluating! ðŸš€**

For the latest updates, check: https://ai.azure.com

