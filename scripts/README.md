# Scripts Directory

Complete collection of scripts for RAG evaluation pipeline.

## ðŸŽ¯ Evaluation Scripts (Main)

### `foundry_evaluate_ragas.py`
**RAGAS-only evaluation using 5 quality metrics**

- **Purpose**: Evaluate KB quality using RAGAS framework
- **Metrics**: 
  - Faithfulness (response grounded in context)
  - Answer Relevance (response addresses query)
  - Context Recall (relevant context retrieved)
  - Context Precision (all context is relevant)
  - Answer Correctness (factually accurate)
- **Input**: `data/processed/test_cases_formatted.json` (100 test cases)
- **Output**: 
  - `artifacts/latest/ragas_evaluation.json` (48 KB)
  - `artifacts/latest/ragas_evaluation.xlsx`
- **Runtime**: ~5-10 seconds (mock heuristic scoring)
- **Real LLM Scoring**: Requires `FOUNDRY_ENDPOINT` env variable

```bash
python scripts/foundry_evaluate_ragas.py
```

---

### `foundry_evaluate_official.py`
**Foundry Official evaluators (11 total)**

- **Purpose**: Safety + Quality evaluation using Foundry's official evaluators
- **Evaluators**:
  - **Quality** (PASS/FAIL): Task Adherence, Coherence
  - **Safety** (0-7 severity): Violence, Self-Harm, Hate/Unfairness, Sexual
  - **Agent-Specific** (PASS/FAIL): Prohibited Actions, Sensitive Data Leakage
  - **Specialized** (PASS/FAIL): Malicious Behavior, Code Execution, Tool Use
- **Input**: `data/processed/test_cases_formatted.json` (100 test cases)
- **Output**:
  - `artifacts/latest/foundry_official_evaluation.json` (73 KB)
  - `artifacts/latest/foundry_official_evaluation.xlsx`
- **Runtime**: ~2-3 seconds (mock evaluation)
- **Real Evaluation**: Requires Azure Foundry credentials

```bash
python scripts/foundry_evaluate_official.py
```

---

### `run_full_evaluation.py`
**Master orchestrator - Runs all phases sequentially**

- **Purpose**: Complete pipeline execution with error handling
- **Phases**:
  1. Load KB & Populate Context (`load_pdf_knowledge_base.py`)
  2. RAGAS Evaluation (`foundry_evaluate_ragas.py`)
  3. Foundry Official Evaluation (`foundry_evaluate_official.py`)
  4. Generate Combined Report (`generate_combined_report.py`)
- **Features**:
  - Graceful error handling (continues on non-critical failures)
  - Detailed execution logging
  - Verification of output files
  - Phase-by-phase progress reporting
- **Output**:
  - All individual evaluation results
  - `artifacts/latest/combined_evaluation.json` (merged results)
  - `artifacts/latest/execution_log.json` (pipeline execution details)
- **Runtime**: ~15-30 seconds total

```bash
python scripts/run_full_evaluation.py
```

---

## ðŸ“Š Knowledge Base Processing

### `load_pdf_knowledge_base.py`
**Extract KB from PDF/TXT and populate test cases with context**

- **Purpose**: Load PlayReady KB and add context to test cases
- **Features**:
  - Supports PDF extraction (via PyPDF2)
  - Fallback to TXT files if PDF unavailable
  - Auto-chunking (800 tokens per chunk, 400-token overlap)
  - Adds top-3 KB chunks as context to each test case
- **Input**: 
  - PDF/TXT KB file (`data/raw/playready_kb.txt` or `.pdf`)
  - Test cases (`data/processed/test_cases_formatted.json`)
- **Output**: `data/processed/test_cases_with_kb.json` (369 KB, enriched with context)
- **Runtime**: ~2-3 seconds

```bash
python scripts/load_pdf_knowledge_base.py
```

---

### `create_sample_pdf.py`
**Generate sample PlayReady KB PDF for testing**

- **Purpose**: Create test KB if real one not available
- **Features**:
  - Generates professional PDF with PlayReady documentation
  - Fallback to TXT if reportlab unavailable
- **Output**:
  - `data/raw/playready_kb.pdf` (if reportlab installed)
  - `data/raw/playready_kb.txt` (fallback)
- **Runtime**: ~1-2 seconds

```bash
python scripts/create_sample_pdf.py
```

---

## ðŸ“ˆ Report Generation

### `generate_combined_report.py`
**Merge RAGAS + Foundry results into unified report**

- **Purpose**: Combine evaluation results from RAGAS and Foundry Official
- **Features**:
  - 3-sheet Excel workbook:
    1. Summary: Aggregated metrics + status
    2. RAGAS Metrics: Per-case RAGAS scores
    3. Foundry Results: Per-case safety + quality
  - JSON export with merged data
  - Color-coded Excel formatting
- **Input**:
  - `artifacts/latest/ragas_evaluation.json`
  - `artifacts/latest/foundry_official_evaluation.json`
- **Output**:
  - `artifacts/latest/combined_evaluation.json` (merged JSON)
  - `artifacts/latest/combined_evaluation.xlsx` (formatted Excel)
- **Runtime**: ~1-2 seconds

```bash
python scripts/generate_combined_report.py
```

---

## ðŸ”§ Utility Scripts

### `upload_to_foundry.py`
**Upload PDFs and configure Foundry RAG agent**

- **Purpose**: Push KB files to Foundry for production deployment
- **Features**: Connects to Azure Foundry, uploads KB files
- **Requires**: Azure Foundry credentials

```bash
python scripts/upload_to_foundry.py
```

---

### `generate_test_cases.py`
**Generate synthetic test cases**

- **Purpose**: Create test cases from KB content
- **Output**: `data/raw/test_cases.json`

```bash
python scripts/generate_test_cases.py
```

---

### `validate_test_cases.py`
**Validate test case format and structure**

- **Purpose**: Ensure test cases are properly formatted
- **Checks**: Required fields, data types, KB context fields

```bash
python scripts/validate_test_cases.py
```

---

### `generate_responses.py`
**Generate AI responses to test queries**

- **Purpose**: Create responses using LLM
- **Output**: Enriches test cases with responses

```bash
python scripts/generate_responses.py
```

---

### `merge_responses_into_testcases.py`
**Merge generated responses into test case file**

- **Purpose**: Combine responses with existing test cases
- **Output**: `data/processed/test_cases_formatted.json`

```bash
python scripts/merge_responses_into_testcases.py
```

---

## ðŸš€ Quick Start

### Run Complete Pipeline:
```bash
python scripts/run_full_evaluation.py
```
Executes all phases sequentially and generates results.

### Run Individual Evaluations:
```bash
# RAGAS only
python scripts/foundry_evaluate_ragas.py

# Foundry Official only
python scripts/foundry_evaluate_official.py

# Load KB and populate context
python scripts/load_pdf_knowledge_base.py
```

### Generate Reports:
```bash
# Create combined report from existing results
python scripts/generate_combined_report.py
```

---

## ðŸ“‹ Environment Variables

```bash
# Optional: Use real RAGAS evaluation with LLM
export FOUNDRY_ENDPOINT=<your-foundry-endpoint>
export FOUNDRY_PROJECT=<your-project-id>

# Optional: Model selection
export FOUNDRY_MODEL_DEPLOYMENT=gpt-4
```

Without env vars, scripts use **mock evaluation** (heuristic scoring) - perfect for testing!

---

## ðŸ“Š Output Files

| Script | Output File | Size | Format |
|--------|-------------|------|--------|
| `foundry_evaluate_ragas.py` | `ragas_evaluation.json` | 48 KB | JSON + XLSX |
| `foundry_evaluate_official.py` | `foundry_official_evaluation.json` | 73 KB | JSON + XLSX |
| `generate_combined_report.py` | `combined_evaluation.json` | 0.7 KB | JSON + XLSX |
| `load_pdf_knowledge_base.py` | `test_cases_with_kb.json` | 369 KB | JSON |
| `run_full_evaluation.py` | `execution_log.json` | 0.8 KB | JSON |

All outputs go to `artifacts/latest/` directory.

---

## âš™ï¸ Dependencies

**Core (Already Installed)**:
- `azure-ai-projects` - Foundry SDK
- `ragas` - RAG evaluation framework
- `openpyxl` - Excel export
- `PyPDF2` - PDF extraction
- `reportlab` - PDF generation
- `python-dotenv` - Environment configuration

**Install Dependencies**:
```bash
pip install -r requirements.txt
```

---

## ðŸ” Troubleshooting

### "PyPDF2 not available"
```bash
pip install PyPDF2
```

### "openpyxl not available"
```bash
pip install openpyxl
```

### "RAGAS library not available"
```bash
pip install ragas datasets
```

### "Module not found" errors
Ensure you're running from workspace root with virtual environment activated:
```bash
source venv/Scripts/activate  # On Windows: venv\Scripts\Activate.ps1
python scripts/run_full_evaluation.py
```

---

## ðŸ“ Notes

- **Mock vs Real**: Scripts gracefully fall back to mock evaluation when Azure credentials unavailable
- **No Results Files**: Results only created after successful pipeline run
- **Idempotent**: Safe to run multiple times - overwrites previous results
- **Logging**: All phases logged to console and execution_log.json

---

## ðŸŽ“ Architecture

```
Test Cases (100)
      â†“
Load KB & Populate Context
      â†“
Test Cases + Context (369 KB)
      â”œâ”€â†’ RAGAS Evaluation (5 metrics)
      â”‚        â†“
      â”‚   ragas_evaluation.json (48 KB)
      â”‚
      â””â”€â†’ Foundry Official Evaluation (11 evaluators)
               â†“
           foundry_official_evaluation.json (73 KB)
      â†“
Generate Combined Report
      â†“
combined_evaluation.json (merged)
combined_evaluation.xlsx (Excel)
```

---

For questions or issues, see main [README.md](../README.md)


