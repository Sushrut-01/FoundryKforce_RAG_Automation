# RAGAS Metrics Documentation - Official Sources

## Overview

This document maps the 5 RAGAS metrics used in our evaluation to their official documentation sources and implementation.

**Official RAGAS Documentation**: https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/

---

## 1. Faithfulness 

**Official Source**: https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/faithfulness/

**Import Statement**:
```python
from ragas.metrics import faithfulness
```

**Definition** (from RAGAS official docs):
- Measures how much of the generated response is grounded in the given context/retrieval
- Evaluates if the model's answer contains only factual information present in retrieved context
- Uses LLM-based evaluation by default

**Implementation in our code** (`foundry_evaluate_ragas.py`):
```python
from ragas.metrics import faithfulness
results = evaluate(
    dataset=dataset,
    metrics=[faithfulness, ...],
    llm=self.openai_client
)
return RAGSMetrics(
    faithfulness=float(results["faithfulness"][0]),
    ...
)
```

**Range**: 0.0 - 1.0
- 1.0 = Response is completely grounded in context
- 0.0 = Response contains information NOT in context

---

## 2. Answer Relevance

**Official Source**: https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/answer_relevance/

**Alternative Name in RAGAS**: `response_relevancy`

**Import Statement**:
```python
from ragas.metrics import answer_relevance
```

**Definition** (from RAGAS official docs):
- Measures whether the generated answer is relevant to the given prompt
- Evaluates if the response directly addresses the query
- Uses LLM-based evaluation by default

**Implementation in our code** (`foundry_evaluate_ragas.py`):
```python
from ragas.metrics import answer_relevance
results = evaluate(
    dataset=dataset,
    metrics=[answer_relevance, ...],
    llm=self.openai_client
)
return RAGSMetrics(
    answer_relevance=float(results["answer_relevance"][0]),
    ...
)
```

**Range**: 0.0 - 1.0
- 1.0 = Response directly and completely addresses the query
- 0.0 = Response is not relevant to the query

---

## 3. Context Recall

**Official Source**: https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/context_recall/

**Import Statement**:
```python
from ragas.metrics import context_recall
```

**Definition** (from RAGAS official docs):
- Measures if all relevant documents/context pieces were retrieved
- Evaluates the completeness of retrieved context
- Requires ground truth for comparison
- Uses LLM-based evaluation by default

**Implementation in our code** (`foundry_evaluate_ragas.py`):
```python
from ragas.metrics import context_recall
results = evaluate(
    dataset=dataset,
    metrics=[context_recall, ...],
    llm=self.openai_client
)
return RAGSMetrics(
    context_recall=float(results["context_recall"][0]),
    ...
)
```

**Range**: 0.0 - 1.0
- 1.0 = All relevant context was retrieved
- 0.0 = No relevant context was retrieved

---

## 4. Context Precision

**Official Source**: https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/context_precision/

**Import Statement**:
```python
from ragas.metrics import context_precision
```

**Definition** (from RAGAS official docs):
- Measures whether the retrieved context is relevant to the query
- Evaluates purity/quality of retrieved context (not quantity)
- Checks if all retrieved documents contribute to answering the query
- Uses LLM-based evaluation by default

**Implementation in our code** (`foundry_evaluate_ragas.py`):
```python
from ragas.metrics import context_precision
results = evaluate(
    dataset=dataset,
    metrics=[context_precision, ...],
    llm=self.openai_client
)
return RAGSMetrics(
    context_precision=float(results["context_precision"][0]),
    ...
)
```

**Range**: 0.0 - 1.0
- 1.0 = All retrieved context is relevant to the query
- 0.0 = No retrieved context is relevant to the query

---

## 5. Answer Correctness

**Official Source**: https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/factual_correctness/

**Alternative Name in RAGAS**: Part of general factual correctness metrics

**Import Statement**:
```python
from ragas.metrics import answer_correctness
```

**Definition** (from RAGAS official docs):
- Measures the factual accuracy of the answer
- Evaluates whether the response matches expected/ground truth answer
- Uses LLM-based fact checking by default
- Requires ground truth for accurate evaluation

**Implementation in our code** (`foundry_evaluate_ragas.py`):
```python
from ragas.metrics import answer_correctness
results = evaluate(
    dataset=dataset,
    metrics=[answer_correctness, ...],
    llm=self.openai_client
)
return RAGSMetrics(
    answer_correctness=float(results["answer_correctness"][0]),
    ...
)
```

**Range**: 0.0 - 1.0
- 1.0 = Answer is completely factually correct
- 0.0 = Answer is completely factually incorrect

---

## RAGAS Integration with Foundry SDK

### Dual Evaluation Modes

**1. Real RAGAS Mode** (Production):
```python
# Uses Foundry OpenAI client for LLM-based evaluation
results = evaluate(
    dataset=dataset,
    metrics=[faithfulness, answer_relevance, context_recall, context_precision, answer_correctness],
    llm=self.openai_client  # â† From Azure AI Foundry
)
```

**Data Flow**:
```
Test Cases (100) 
    â†“
RAGAS Dataset (from_dict)
    â†“
evaluate() with Foundry OpenAI LLM
    â†“
5 LLM-based metrics scores
    â†“
Results JSON + Excel Export
```

**2. Mock RAGAS Mode** (Testing/Free):
```python
# Uses heuristic scoring without LLM calls
# Fallback when Foundry SDK not available
faithfulness_score = len(response_words & context_words) / max(len(response_words), 1)
answer_relevance_score = len(query_words & response_words) / max(len(query_words), 1)
# ... etc
```

---

## Official RAGAS Documentation Links

| Metric | Documentation | GitHub |
|--------|----------------|--------|
| **Faithfulness** | [faithfulness/](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/faithfulness/) | [ragas/ragas/metrics/faithfulness.py](https://github.com/vibrantlabsai/ragas/blob/master/src/ragas/metrics/faithfulness.py) |
| **Answer Relevance** | [answer_relevance/](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/answer_relevance/) | [ragas/ragas/metrics/answer_relevance.py](https://github.com/vibrantlabsai/ragas/blob/master/src/ragas/metrics/answer_relevance.py) |
| **Context Recall** | [context_recall/](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/context_recall/) | [ragas/ragas/metrics/context_recall.py](https://github.com/vibrantlabsai/ragas/blob/master/src/ragas/metrics/context_recall.py) |
| **Context Precision** | [context_precision/](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/context_precision/) | [ragas/ragas/metrics/context_precision.py](https://github.com/vibrantlabsai/ragas/blob/master/src/ragas/metrics/context_precision.py) |
| **Factual Correctness** | [factual_correctness/](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/factual_correctness/) | [ragas/ragas/metrics/factual_correctness.py](https://github.com/vibrantlabsai/ragas/blob/master/src/ragas/metrics/factual_correctness.py) |

---

## Foundry SDK Integration

### Azure AI Foundry Reference

**Official Docs**: https://learn.microsoft.com/en-us/azure/ai-studio/

**Our Integration**:
```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Initialize Foundry project client
project_client = AIProjectClient(
    endpoint=foundry_endpoint,
    credential=DefaultAzureCredential()
)

# Get OpenAI client from Foundry
openai_client = project_client.get_openai_client()

# Use with RAGAS evaluation
results = evaluate(
    dataset=dataset,
    metrics=metrics,
    llm=openai_client  # â† Foundry-hosted GPT-4
)
```

**Environment Variables**:
```bash
FOUNDRY_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project-name>
FOUNDRY_PROJECT=<project-name>
OPENAI_API_KEY=<your-key>
```

---

## Implementation Quality Assurance

âœ… **All metrics sourced from official RAGAS library**
- Direct imports from `ragas.metrics`
- No custom implementations (except mock fallback)
- LLM-based evaluation via Foundry SDK OpenAI client

âœ… **Type hints properly annotated**
```python
from typing import Tuple, List

def validate_format(self, test_case: Dict[str, Any]) -> Tuple[bool, List[str]]:
    ...

def compute_ragas_real_scores(
    self, query: str, response: str, context: List[str]
) -> RAGSMetrics:
    ...
```

âœ… **Graceful degradation**
- Real RAGAS: Requires `ragas`, `datasets`, `azure-ai-projects`
- Mock RAGAS: Pure Python fallback with heuristic scoring

âœ… **Output formats**
- JSON results: `ragas_evaluation.json`
- Excel report: `ragas_evaluation.xlsx`
- Console output: Formatted report with metrics visualization

---

## References

1. **RAGAS Official Documentation** - https://docs.ragas.io/
2. **RAGAS GitHub Repository** - https://github.com/vibrantlabsai/ragas
3. **Azure AI Foundry Documentation** - https://learn.microsoft.com/en-us/azure/ai-studio/
4. **RAGAS Paper** - "Ragas: A Comprehensive Framework for Evaluating RAG Applications" - https://arxiv.org/abs/2309.15217


