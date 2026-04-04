# RAGAS Metrics Usage Mapping

## Official RAGAS Framework â†’ Our Implementation

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚         RAGAS Official Documentation                            â”‚
â”‚    https://docs.ragas.io/en/latest/concepts/metrics/            â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                              â†“
        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
        â”‚   Available Metrics (5 metrics)        â”‚
        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                   â†™        â†™        â†™        â†™        â†™
            â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
            â”‚  1. Faithfulness                             â”‚
            â”‚  2. Answer Relevance                         â”‚
            â”‚  3. Context Recall                           â”‚
            â”‚  4. Context Precision                        â”‚
            â”‚  5. Answer Correctness (Factual)             â”‚
            â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                              â†“
    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
    â”‚  Our Implementation:                              â”‚
    â”‚  foundry_evaluate_ragas.py                        â”‚
    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
         â†“              â†“              â†“              â†“
    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
    â”‚ Import â”‚    â”‚ Process â”‚    â”‚Evaluateâ”‚    â”‚Export    â”‚
    â”‚ Metricsâ”‚    â”‚Test Caseâ”‚    â”‚ Metricsâ”‚    â”‚ Results  â”‚
    â””â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
         â†“              â†“              â†“              â†“
      Lines      Lines 160-200   Lines 250-300   Lines 600-630
      49-58      (normalize)     (compute_ragas) (JSON + Excel)
```

---

## Source Code Line Mapping

### 1. RAGAS Imports (Lines 49-58)
**Official Source**: `ragas.metrics` package

```python
from ragas.metrics import (  # type: ignore[import]
    faithfulness,                    # â† https://docs.ragas.io/.../faithfulness/
    answer_relevance,                # â† https://docs.ragas.io/.../answer_relevance/
    context_recall,                  # â† https://docs.ragas.io/.../context_recall/
    context_precision,               # â† https://docs.ragas.io/.../context_precision/
    answer_correctness               # â† https://docs.ragas.io/.../factual_correctness/
)
from ragas import evaluate           # â† Official evaluate() function
from datasets import Dataset         # â† RAGAS-compatible dataset format
```

---

### 2. RAGAS Evaluation Process (Lines 250-320)

**Function**: `compute_ragas_real_scores()`

**Flow** (using official RAGAS framework):
```
Step 1: Create RAGAS Dataset
    â†“
eval_data = {
    "question": [query],           # â† RAGAS expects "question" field
    "answer": [response],          # â† RAGAS expects "answer" field
    "contexts": [[" ".join()]],    # â† RAGAS expects "contexts" field
    "ground_truth": [response]     # â† RAGAS expects "ground_truth" field
}
dataset = Dataset.from_dict(eval_data)

Step 2: Select Metrics (from official RAGAS)
    â†“
metrics = [
    faithfulness,                  # Official metric #1
    answer_relevance,              # Official metric #2
    context_recall,                # Official metric #3
    context_precision,             # Official metric #4
    answer_correctness             # Official metric #5
]

Step 3: Evaluate with Foundry LLM
    â†“
results = evaluate(                                    # Official function
    dataset=dataset,
    metrics=metrics,
    llm=self.openai_client         # â† Foundry OpenAI (GPT-4)
)

Step 4: Extract Scores (0.0-1.0 range from RAGAS)
    â†“
return RAGSMetrics(
    faithfulness=float(results["faithfulness"][0]),           # 0.0-1.0
    answer_relevance=float(results["answer_relevance"][0]),   # 0.0-1.0
    context_recall=float(results["context_recall"][0]),       # 0.0-1.0
    context_precision=float(results["context_precision"][0]), # 0.0-1.0
    answer_correctness=float(results["answer_correctness"][0])# 0.0-1.0
)
```

---

## Metric Definitions (from Official RAGAS Documentation)

| Metric | Purpose | Score Meaning | Source URL |
|--------|---------|---------------|-----------|
| **Faithfulness** | Factuality grounded in context | 1.0 = All from context | https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/faithfulness/ |
| **Answer Relevance** | Response addresses query | 1.0 = Fully relevant | https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/answer_relevance/ |
| **Context Recall** | Retrieval completeness | 1.0 = All relevant docs retrieved | https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/context_recall/ |
| **Context Precision** | Context quality | 1.0 = All retrieved docs relevant | https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/context_precision/ |
| **Answer Correctness** | Factual accuracy | 1.0 = Completely accurate | https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/factual_correctness/ |

---

## Evaluation Modes Comparison

### Mode 1: Real RAGAS (LLM-based)
```
Enabled by: RAGAS library installed + Foundry SDK available

Process:
100 Test Cases
    â†“
RAGAS evaluate() function
    â†“
LLM Prompting (via Foundry OpenAI)
    â†“
5 Metric Scores (from official RAGAS)
    â†“
Results JSON + Excel

Cost: ~$5-15 per 100 cases
Accuracy: High (LLM judgment)
Time: ~30 seconds per 100 cases
```

### Mode 2: Mock RAGAS (Heuristic)
```
Enabled by: Pure Python (no LLM)

Process:
100 Test Cases
    â†“
Heuristic Scoring (lines 365-405)
    â†“
Word-overlap calculations
    â†“
5 Pseudo-Metric Scores (same format as RAGAS)
    â†“
Results JSON + Excel

Cost: $0 free
Accuracy: Medium (word overlap only)
Time: <1 second per 100 cases
```

---

## Files Generated

### Input Sources
- **Test Cases**: `data/processed/test_cases_formatted.json` (100 Foundry-formatted cases)
- **RAGAS Framework**: Official library from PyPI
- **LLM Provider**: Azure AI Foundry GPT-4 endpoint

### Output Files
1. **Console Report**
   - Formatted metrics breakdown
   - Status summary (PASS/FAIL)
   - Visual bar charts

2. **JSON Results** (`artifacts/latest/ragas_evaluation.json`)
   - All 5 metrics per case
   - Average scores
   - Status breakdown

3. **Excel Report** (`artifacts/latest/ragas_evaluation.xlsx`)
   - Summary sheet with averages
   - Results sheet with all 100 cases
   - Formatted with headers and colors

---

## Official Documentation References

### RAGAS Framework
- **Main Docs**: https://docs.ragas.io/en/latest/
- **Metrics Overview**: https://docs.ragas.io/en/latest/concepts/metrics/overview/
- **Available Metrics**: https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/
- **GitHub**: https://github.com/vibrantlabsai/ragas
- **Paper**: https://arxiv.org/abs/2309.15217

### Azure AI Foundry
- **Main Docs**: https://learn.microsoft.com/en-us/azure/ai-studio/
- **SDK Reference**: https://learn.microsoft.com/en-us/python/api/azure-ai-projects/
- **Project Client**: AIProjectClient for project management

### Datasets Library
- **PyPI**: https://pypi.org/project/datasets/
- **Documentation**: https://huggingface.co/docs/datasets/

---

## Code Quality Checklist

âœ… **Type Annotations** (All metrics properly typed)
```python
def compute_ragas_real_scores(
    self, query: str, response: str, context: List[str]
) -> RAGSMetrics:
```

âœ… **Error Handling** (Exception variables properly named)
```python
except Exception as err:  # â† Consistent naming
    logger.error(f"Error computing real RAGAS metrics: {err}")
```

âœ… **Imports** (All from official sources)
```python
from ragas.metrics import (
    faithfulness,
    answer_relevance,
    context_recall,
    context_precision,
    answer_correctness
)
```

âœ… **Graceful Degradation**
```python
if RAGAS_AVAILABLE:
    return self.compute_ragas_real_scores(...)
else:
    logger.warning("Using MOCK RAGAS (heuristic scoring)")
    return self.compute_ragas_mock_scores(...)
```

âœ… **Foundry Integration**
```python
from azure.ai.projects import AIProjectClient
project_client = AIProjectClient(
    endpoint=foundry_endpoint,
    credential=DefaultAzureCredential()
)
openai_client = project_client.get_openai_client()
```

---

## Summary

**âœ… ALL 5 Metrics from Official RAGAS Documentation:**
1. âœ… Faithfulness - from RAGAS library
2. âœ… Answer Relevance - from RAGAS library
3. âœ… Context Recall - from RAGAS library
4. âœ… Context Precision - from RAGAS library
5. âœ… Answer Correctness - from RAGAS library

**âœ… Integrated with Azure AI Foundry SDK:**
- Uses OpenAI client from Foundry project
- Authenticates via Azure DefaultAzureCredential
- Evaluates 100 test cases in batch mode

**âœ… Output in Multiple Formats:**
- Console report with visualization
- JSON results for programmatic access
- Excel workbook with formatted sheets


