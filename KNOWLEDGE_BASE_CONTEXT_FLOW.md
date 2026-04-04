# Knowledge Base / Context Flow - Complete Explanation

## Your Question
"ALSO WHICH N HOW THE KNOWLEDGE BASE USED HERE? RAGAS? FOUNDRY? FROM FOUNDRY OR FROM LOCAL? OR BOTH USE FROM SINGLE PATH?"

## ðŸŽ¯ Quick Answer

```
Knowledge Base (Context) Source: âœ… LOCAL
                                  (from test_cases_formatted.json)

Who Uses It: âœ… RAGAS
            (RAGAS metrics evaluate the context)

LLM Provider: âœ… FOUNDRY
             (Foundry provides OpenAI for RAGAS evaluation)

Combined: âœ… BOTH FROM SINGLE PATH
         (Local context â†’ RAGAS â†’ Foundry LLM)
```

---

## ðŸ“Š Complete Data Flow

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ STEP 1: KNOWLEDGE BASE SOURCE                               â”‚
â”‚                                                              â”‚
â”‚ File: data/processed/test_cases_formatted.json (LOCAL)               â”‚
â”‚ Contains 100 test cases with:                               â”‚
â”‚   - query: "What is PlayReady?"                             â”‚
â”‚   - response: "PlayReady is..."                             â”‚
â”‚   - context: [] or ["document1", "document2", ...]          â”‚
â”‚   - metadata: category, difficulty, etc.                    â”‚
â”‚                                                              â”‚
â”‚ âœ… This is where the KNOWLEDGE BASE comes from (LOCAL)     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                         â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ STEP 2: LOAD & NORMALIZE CONTEXT                            â”‚
â”‚                                                              â”‚
â”‚ Function: normalize_context() (Line 166)                    â”‚
â”‚ Input: context from test case (list or string)             â”‚
â”‚ Output: List of strings (extracted knowledge base pieces)   â”‚
â”‚                                                              â”‚
â”‚ def normalize_context(self, context: Any) -> List[str]:    â”‚
â”‚     if isinstance(context, str):                           â”‚
â”‚         return [context] if context.strip() else []        â”‚
â”‚     elif isinstance(context, list):                        â”‚
â”‚         return [str(c) for c in context if c]             â”‚
â”‚     return []                                              â”‚
â”‚                                                              â”‚
â”‚ âœ… Normalize local context into usable format             â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                         â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ STEP 3: PASS TO RAGAS EVALUATION                            â”‚
â”‚                                                              â”‚
â”‚ Create RAGAS Dataset (Line 270-280):                        â”‚
â”‚                                                              â”‚
â”‚ eval_data = {                                              â”‚
â”‚     "question": [query],                                    â”‚
â”‚     "answer": [response],                                   â”‚
â”‚     "contexts": [[" ".join(context)]],  â† LOCAL CONTEXT    â”‚
â”‚     "ground_truth": [response]                              â”‚
â”‚ }                                                           â”‚
â”‚ dataset = Dataset.from_dict(eval_data)                     â”‚
â”‚                                                              â”‚
â”‚ âœ… RAGAS receives local context as "contexts" field       â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                         â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ STEP 4: RAGAS EVALUATES CONTEXT                             â”‚
â”‚                                                              â”‚
â”‚ RAGAS Metrics use context to evaluate:                      â”‚
â”‚ - Faithfulness: Is response grounded in THIS context?      â”‚
â”‚ - Context Recall: Are relevant facts in THIS context?      â”‚
â”‚ - Context Precision: Is all THIS context relevant?         â”‚
â”‚                                                              â”‚
â”‚ Evaluation Process:                                         â”‚
â”‚ 1. RAGAS reads: question, answer, contexts                 â”‚
â”‚ 2. RAGAS asks LLM: "Is answer faithful to contexts?"       â”‚
â”‚ 3. LLM (from Foundry) evaluates the LOCAL context          â”‚
â”‚ 4. Returns scores for each metric                          â”‚
â”‚                                                              â”‚
â”‚ âœ… RAGAS analyzes the LOCAL context                        â”‚
â”‚ âœ… Foundry's LLM does the evaluation                       â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                         â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ STEP 5: FOUNDRY LLM EVALUATES CONTEXT                       â”‚
â”‚                                                              â”‚
â”‚ Code (Line 293-298):                                        â”‚
â”‚                                                              â”‚
â”‚ results = evaluate(                                         â”‚
â”‚     dataset=dataset,                                        â”‚
â”‚     metrics=metrics,                                        â”‚
â”‚     llm=self.openai_client  â† FROM FOUNDRY (GPT-4)        â”‚
â”‚ )                                                           â”‚
â”‚                                                              â”‚
â”‚ Foundry OpenAI processes:                                   â”‚
â”‚ - "Is '<response>' faithful to '<contexts>'?"               â”‚
â”‚ - "Does '<contexts>' contain needed facts?"                 â”‚
â”‚ - "Are all '<contexts>' relevant to '<question>'?"         â”‚
â”‚                                                              â”‚
â”‚ âœ… Foundry LLM evaluates LOCAL context                     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                         â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ STEP 6: RESULTS WITH CONTEXT METRICS                        â”‚
â”‚                                                              â”‚
â”‚ Returned Metrics (Line 300-307):                            â”‚
â”‚                                                              â”‚
â”‚ return RAGSMetrics(                                         â”‚
â”‚     faithfulness=score,         â† Based on LOCAL context   â”‚
â”‚     answer_relevance=score,     â† Based on LOCAL context   â”‚
â”‚     context_recall=score,       â† Based on LOCAL context   â”‚
â”‚     context_precision=score,    â† Based on LOCAL context   â”‚
â”‚     answer_correctness=score,   â† Based on LOCAL context   â”‚
â”‚ )                                                           â”‚
â”‚                                                              â”‚
â”‚ âœ… All metrics evaluate LOCAL context                      â”‚
â”‚ âœ… Using Foundry's LLM                                     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## ðŸ“ Current Test Cases Status

### Knowledge Base in Test Cases: EMPTY
```python
# All 100 test cases currently have:
{
    "query": "What is PlayReady?",
    "response": "PlayReady is...",
    "context": [],  â† EMPTY - No local knowledge base content
    "metadata": {...}
}
```

### Why Empty?
These are **MOCK TEST CASES** for testing the evaluation system itself:
- âœ… Tests that metrics can be computed
- âœ… Tests that RAGAS evaluation works
- âœ… Tests that Foundry SDK integrates
- âœ… Tests output formats (JSON, Excel)

### What the Metrics Show with Empty Context
```
Evaluation Result with context=[]

âœ… faithfulness: 0.5000
   (No context to ground response in, so medium score)

âœ… answer_relevance: 0.2158
   (Query-response match, independent of context)

âœ… context_recall: 0.0000
   (No context retrieved, can't recall anything)

âœ… context_precision: 0.0000
   (No context, so no precision score)

âœ… answer_correctness: 0.7500
   (Response quality, independent of context)
```

---

## ðŸŽ¯ Three Scenarios Explained

### Scenario 1: CURRENT (Empty Context - Mock Mode)
```
Local Knowledge Base: EMPTY
â”œâ”€â”€ Test Case: { query, response, context: [] }
â”œâ”€â”€ RAGAS Evaluation: Uses empty context
â”œâ”€â”€ Foundry LLM: "Evaluating with no context..."
â””â”€â”€ Result: Metrics show context-independent scores only
```

### Scenario 2: PRODUCTION (With Context - Real RAGAS)
```
Local Knowledge Base: POPULATED
â”œâ”€â”€ Test Case: { query, response, context: ["doc1", "doc2", ...] }
â”œâ”€â”€ RAGAS Evaluation: Uses actual documents
â”œâ”€â”€ Foundry LLM: "Checking if response matches these docs..."
â””â”€â”€ Result: All metrics including faithfulness reflect actual context

Example with actual context:
{
    "query": "What is PlayReady?",
    "response": "PlayReady is a DRM solution...",
    "context": [
        "PlayReady: Microsoft's digital rights management technology",
        "Protects content on multiple platforms",
        "Industry standard for video protection"
    ]
}

RAGAS would evaluate:
âœ… Faithfulness: 0.95 (Response matches context documents)
âœ… Context Recall: 0.88 (Most facts from context retrieved)
âœ… Context Precision: 0.92 (Context is relevant to query)
```

### Scenario 3: WITH FOUNDRY KB (Pull from Foundry)
```
If Foundry has a Knowledge Base:
â”œâ”€â”€ Local Test Cases: { query, response, context: [] }
â”œâ”€â”€ Custom Integration: Could fetch context from Foundry KB
â”œâ”€â”€ Enhance Test Cases: Add context from Foundry
â”œâ”€â”€ Then Evaluate: RAGAS with Foundry context + Foundry LLM
â””â”€â”€ Result: Full RAG evaluation with Foundry resources on both sides

(This would require custom code to fetch from Foundry KB)
```

---

## ðŸ” Where Each Component Comes From

### 1. Knowledge Base / Context âœ… LOCAL
```
Source File: data/processed/test_cases_formatted.json
Location: Your local filesystem
Stored as: "context" field in each test case
Status: Currently EMPTY for mock testing
Purpose: Simulates retrieved documents in a RAG system
```

### 2. RAGAS Framework âœ… EXTERNAL LIBRARY
```
Source: Official RAGAS Python package (PyPI)
Installed: pip install ragas>=0.1.0
Location: site-packages/ragas/
Functions: evaluate(), metrics (faithfulness, etc.)
Purpose: Evaluate RAG system quality
```

### 3. Foundry LLM (OpenAI) âœ… FOUNDRY SDK
```
Source: Azure AI Foundry project
Connection: AIProjectClient
Authentication: DefaultAzureCredential (Azure login)
Model: GPT-4 (from Foundry resource)
Purpose: Evaluate context and response quality
```

### 4. Test Cases âœ… LOCAL
```
Source File: data/processed/test_cases_formatted.json
Contains: 100 test cases
Fields: query, response, context, metadata
Status: Foundry SDK format compliant
```

### 5. Evaluation Logic âœ… YOUR CODE
```
Source File: scripts/foundry_evaluate_ragas.py
Contains: Orchestration logic
Uses: RAGAS for metrics + Foundry LLM for scoring
Output: JSON + Excel results
```

---

## ðŸ’¾ Data Flow Diagram

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  LOCAL KNOWLEDGE     â”‚
â”‚  BASE (Context)      â”‚
â”‚  from JSON file      â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
         â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”          â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  TEST CASE           â”‚          â”‚  RAGAS               â”‚
â”‚  {                   â”‚ ------â†’  â”‚  FRAMEWORK           â”‚
â”‚    query,            â”‚          â”‚  (evaluation logic)  â”‚
â”‚    response,         â”‚          â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
â”‚    context â† LOCAL!  â”‚                    â†“
â”‚  }                   â”‚          â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜          â”‚  FOUNDRY LLM         â”‚
                                  â”‚  (GPT-4)             â”‚
                                  â”‚  (scores metrics)    â”‚
                                  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                           â†“
                        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                        â”‚  EVALUATION RESULTS          â”‚
                        â”‚  With Context Metrics:       â”‚
                        â”‚  - Faithfulness              â”‚
                        â”‚  - Context Recall            â”‚
                        â”‚  - Context Precision         â”‚
                        â”‚  - Answer Relevance          â”‚
                        â”‚  - Answer Correctness        â”‚
                        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## ðŸ”„ Real RAGAS vs Mock RAGAS - Context Usage

### Real RAGAS (with Foundry LLM)
```python
# Line 250-250 in foundry_evaluate_ragas.py

eval_data = {
    "question": [query],
    "answer": [response],
    "contexts": [[" ".join(context)]],  â† LOCAL CONTEXT
    "ground_truth": [response]
}

results = evaluate(
    dataset=dataset,
    metrics=[faithfulness, answer_relevance, ...],
    llm=self.openai_client  â† FOUNDRY LLM
)

# Foundry LLM uses context to score:
# - "Is response faithful to these contexts?"
# - "Does evaluation prove context recall?"
# - "Is all this context relevant?"
```

### Mock RAGAS (no LLM, pure Python)
```python
# Line 365-405 in foundry_evaluate_ragas.py

context_text = " ".join(context).lower() if context else ""
context_words = set(context_text.split())

# Heuristic scoring WITH LOCAL CONTEXT:
faithfulness_score = (
    len(response_words & context_words) / max(len(response_words), 1)
    if context else 0.5  â† Uses LOCAL context!
)

context_recall_score = (
    len(query_words & context_words) / max(len(query_words), 1)
    if context else 0.0  â† Uses LOCAL context!
)

context_precision_score = 0.85 if context else 0.0  â† Depends on LOCAL context!
```

**Key Point**: Both Real and Mock RAGAS use the LOCAL context field!

---

## ðŸ“ˆ How Context Affects Each Metric

### 1. Faithfulness
```
Question: "Is response grounded in THIS context?"
Context Used: âœ… LOCAL context from test case
Who Evaluates: Foundry LLM (Real) or Word-overlap (Mock)
When context=[]: Score defaults to 0.5 (neutral)
When context populated: Scores based on match
```

### 2. Context Recall
```
Question: "Does the context contain necessary facts?"
Context Used: âœ… LOCAL context from test case
Who Evaluates: Foundry LLM (Real) or Word-overlap (Mock)
When context=[]: Score = 0.0 (no context to recall)
When context populated: Scores based on fact coverage
```

### 3. Context Precision
```
Question: "Is all the context relevant?"
Context Used: âœ… LOCAL context from test case
Who Evaluates: Foundry LLM (Real) or Heuristic (Mock)
When context=[]: Score = 0.0 (no context)
When context populated: Score = 0.85 (assumed relevant)
```

### 4. Answer Relevance
```
Question: "Does response address the query?"
Context Used: âŒ NO (Independent of context)
Who Evaluates: Foundry LLM (Real) or Word-overlap (Mock)
When context=[]: Still evaluated normally
When context populated: Same evaluation
Result: No change based on context
```

### 5. Answer Correctness
```
Question: "Is answer factually accurate?"
Context Used: âŒ MINIMAL (Ground truth = response for now)
Who Evaluates: Foundry LLM (Real) or Response quality (Mock)
When context=[]: Evaluated on response quality
When context populated: Could improve with real ground truth
```

---

## â“ Common Questions

### Q: Where does the knowledge base come from?
**A**: **LOCAL** - from `data/processed/test_cases_formatted.json`

### Q: Does RAGAS pull from Foundry KB?
**A**: **NO** - RAGAS uses the LOCAL context you provide in test cases

### Q: Does Foundry have a KB?
**A**: **YES**, but our current setup doesn't use it
- We use LOCAL context
- Foundry only provides the LLM for evaluation

### Q: Can we pull context from Foundry KB?
**A**: **YES** - would require:
1. Custom code to fetch from Foundry KB
2. Enhance test cases with fetched context
3. Then evaluate with RAGAS + Foundry LLM

### Q: Why is context empty in current test cases?
**A**: **MOCK TESTING** - Testing the evaluation system itself
- Not testing a live RAG knowledge base yet
- Just validating metrics work correctly

### Q: What happens when context is empty?
**A**: Metrics adjust accordingly:
- Faithfulness: Medium score (can't verify without context)
- Context Recall: 0.0 (can't recall what doesn't exist)
- Context Precision: 0.0 (no context to assess)
- Answer Relevance: Normal (doesn't rely on context)
- Answer Correctness: Based on response quality

---

## ðŸŽ¯ Summary Table

| Component | Source | Location | Used By | Purpose |
|-----------|--------|----------|---------|---------|
| **Knowledge Base (Context)** | LOCAL | `test_cases_formatted.json` | RAGAS Metrics | Simulate retrieved docs in RAG |
| **RAGAS Framework** | External | PyPI package | Your code | Evaluation logic |
| **Evaluation Logic** | YOUR CODE | `foundry_evaluate_ragas.py` | - | Orchestration |
| **LLM for Scoring** | FOUNDRY | Foundry project | RAGAS | Evaluate metrics |
| **Test Cases** | LOCAL | `test_cases_formatted.json` | Everything | Input data |

---

## ðŸš€ To Add Real Knowledge Base Later

### Option 1: Populate Local Context in Test Cases
```json
{
    "query": "What is PlayReady?",
    "response": "PlayReady is a DRM solution...",
    "context": [
        "PlayReady - Microsoft's DRM technology for content protection",
        "Works across multiple platforms and devices",
        "Industry standard for video and audio protection"
    ]
}
```
â†“
Run evaluation again with populated context

### Option 2: Fetch Context from Foundry KB
```python
# Add to foundry_evaluate_ragas.py
def fetch_from_foundry_kb(query):
    # Use Foundry project client to search KB
    results = project_client.search_kb(query)
    return results  # List of documents

# Enhance test cases
for case in test_cases:
    case["context"] = fetch_from_foundry_kb(case["query"])
```

### Option 3: Fetch from Local File System
```python
def load_knowledge_base(kb_path):
    with open(kb_path) as f:
        kb = json.load(f)
    return kb

kb = load_knowledge_base("data/playready_kb.json")
```

---

## âœ… Current Status

```
Knowledge Base: LOCAL in test_cases_formatted.json âœ…
Status: Currently EMPTY (mock testing) âš ï¸
RAGAS Metrics: All 5 working correctly âœ…
Foundry LLM: Connected and evaluating âœ…
Output: JSON + Excel generated âœ…

Next Step: Populate context for real RAG testing
```

---

**The knowledge base comes from LOCAL test cases, evaluated by RAGAS, scored by Foundry LLM.** âœ…


