# Knowledge Base - Visual Quick Reference

## ðŸŽ¯ The Single Unified Path

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  WHERE DOES KNOWLEDGE BASE COME FROM?                       â”‚
â”‚                                                              â”‚
â”‚  Answer: âœ… SINGLE LOCAL PATH                               â”‚
â”‚                                                              â”‚
â”‚  data/processed/test_cases_formatted.json                             â”‚
â”‚    â†“                                                         â”‚
â”‚    { "query": "...",                                         â”‚
â”‚      "response": "...",                                      â”‚
â”‚      "context": [LOCAL KNOWLEDGE BASE ITEMS] â† HERE          â”‚
â”‚    }                                                         â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## ðŸ”„ Complete Single Path Flow

```
â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—
â•‘ YOUR LOCAL KNOWLEDGE BASE (context field in JSON)           â•‘
â•‘ Currently: [] (empty for mock testing)                       â•‘
â•‘ Eventually: ["doc1", "doc2", "doc3", ...] (real KB)          â•‘
â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
               â†“
â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—
â•‘ STEP 1: Test Case Created                                   â•‘
â•‘                                                              â•‘
â•‘ {                                                            â•‘
â•‘   "query": "What is PlayReady?",                             â•‘
â•‘   "response": "PlayReady is...",                             â•‘
â•‘   "context": [] â† Your KB comes here (LOCAL)                 â•‘
â•‘ }                                                            â•‘
â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
               â†“
â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—
â•‘ STEP 2: Load Test Cases                                     â•‘
â•‘                                                              â•‘
â•‘ test_cases = json.load("test_cases_formatted.json")          â•‘
â•‘ # test_cases[0]["context"] = [] â† Your LOCAL KB              â•‘
â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
               â†“
â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—
â•‘ STEP 3: Pass to RAGAS (The framework that uses KB)           â•‘
â•‘                                                              â•‘
â•‘ eval_data = {                                               â•‘
â•‘   "question": query,                                        â•‘
â•‘   "answer": response,                                       â•‘
â•‘   "contexts": [context],  â† From LOCAL KB                    â•‘
â•‘   "ground_truth": response                                  â•‘
â•‘ }                                                            â•‘
â•‘                                                              â•‘
â•‘ RAGAS evaluates:                                            â•‘
â•‘ - Is response faithful to THESE contexts (YOUR KB)?         â•‘
â•‘ - Can we recall facts from THESE contexts (YOUR KB)?        â•‘
â•‘ - Is THESE contexts (YOUR KB) relevant?                     â•‘
â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
               â†“
â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—
â•‘ STEP 4: Foundry LLM Scores the KB (via RAGAS)               â•‘
â•‘                                                              â•‘
â•‘ results = evaluate(                                         â•‘
â•‘   dataset=dataset,                                          â•‘
â•‘   metrics=[...],                                            â•‘
â•‘   llm=foundry_openai_client  â† Uses Foundry LLM            â•‘
â•‘ )                                                           â•‘
â•‘                                                              â•‘
â•‘ Foundry LLM asks:                                           â•‘
â•‘ â€¢ "Is '<response>' faithful to '<YOUR LOCAL KB>'?"          â•‘
â•‘ â€¢ "Is '<YOUR LOCAL KB>' complete for the query?"           â•‘
â•‘ â€¢ "Is all '<YOUR LOCAL KB>' relevant?"                     â•‘
â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
               â†“
â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—
â•‘ STEP 5: Results Reflect YOUR KB Quality                     â•‘
â•‘                                                              â•‘
â•‘ Metrics Based on YOUR KB:                                   â•‘
â•‘ âœ“ Faithfulness    - how well response matches YOUR KB       â•‘
â•‘ âœ“ Context Recall  - what YOUR KB covered                    â•‘
â•‘ âœ“ Context Precision - relevance of YOUR KB                  â•‘
â•‘ âœ“ Answer Relevance  - query-response match                  â•‘
â•‘ âœ“ Answer Correctness - response quality                     â•‘
â•‘                                                              â•‘
â•‘ Output:                                                      â•‘
â•‘ {                                                            â•‘
â•‘   "faithfulness": 0.X,                                       â•‘
â•‘   "context_recall": 0.X,  â† Based on YOUR KB                â•‘
â•‘   "context_precision": 0.X  â† Based on YOUR KB              â•‘
â•‘   ...                                                        â•‘
â•‘ }                                                            â•‘
â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
               â†“
â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—
â•‘ FINAL: JSON + Excel Export                                  â•‘
â•‘ Shows how good YOUR KB is for each query                    â•‘
â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
```

---

## ðŸŽ¯ Three Component Sources

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ 1. KNOWLEDGE BASE (Context)                                  â”‚
â”‚    Source: âœ… YOUR LOCAL FILE                                â”‚
â”‚    File: data/processed/test_cases_formatted.json                      â”‚
â”‚    Field: "context": []                                      â”‚
â”‚    Status: Currently empty for mock testing                  â”‚
â”‚    Will become: Your real KB when populated                  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ 2. RAGAS EVALUATION FRAMEWORK                                â”‚
â”‚    Source: âœ… EXTERNAL LIBRARY (PyPI)                        â”‚
â”‚    Package: ragas                                            â”‚
â”‚    Purpose: Defines metrics & evaluation logic               â”‚
â”‚    Uses: YOUR LOCAL KB to evaluate                           â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ 3. FOUNDRY LLM (for scoring)                                 â”‚
â”‚    Source: âœ… AZURE AI FOUNDRY                               â”‚
â”‚    Component: OpenAI GPT-4 endpoint                          â”‚
â”‚    Purpose: Uses LLM to score against YOUR KB                â”‚
â”‚    Used by: RAGAS for metric calculations                    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## ðŸ“Š Component Interaction

```
YOUR PROJECT
â”œâ”€â”€ LOCAL KB (context in JSON)
â”‚   â†“
â”‚   â”Œâ”€â†’ normalize_context() â†’ List[str]
â”‚   â”‚
â”‚   â””â”€â†’ Test Case Dict
â”‚       â”œâ”€â”€ query
â”‚       â”œâ”€â”€ response
â”‚       â””â”€â”€ context â† YOUR KB HERE
â”‚           â†“
â”‚           â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚           â”‚  RAGAS Framework        â”‚
â”‚           â”‚  (evaluate function)    â”‚
â”‚           â”‚                         â”‚
â”‚           â”‚  Metrics:               â”‚
â”‚           â”‚  - faithfulness         â”‚
â”‚           â”‚  - answer_relevance     â”‚
â”‚           â”‚  - context_recall â† uses YOUR KB
â”‚           â”‚  - context_precision â† uses YOUR KB
â”‚           â”‚  - answer_correctness   â”‚
â”‚           â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
â”‚                    â†“
â”‚           â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚           â”‚  Foundry LLM (GPT-4)    â”‚
â”‚           â”‚  (OpenAI from Foundry)  â”‚
â”‚           â”‚                         â”‚
â”‚           â”‚  Scores against:        â”‚
â”‚           â”‚  YOUR KB (context)      â”‚
â”‚           â”‚                         â”‚
â”‚           â”‚  Returns: Scores 0.0-1.0 â”‚
â”‚           â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
â”‚                    â†“
â”‚           EVALUATION RESULTS
â”‚           {
â”‚             "faithfulness": score based on YOUR KB
â”‚             "context_recall": score based on YOUR KB
â”‚             "context_precision": score based on YOUR KB
â”‚             ...
â”‚           }
â”‚                    â†“
â”‚           JSON + EXCEL EXPORT
â”‚           Shows YOUR KB quality
```

---

## ðŸ” Three Use Scenarios

### Scenario A: CURRENT (Empty KB - Testing mode)
```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ "context": []                                                â”‚
â”‚                                                              â”‚
â”‚ Flow:                                                        â”‚
â”‚ Empty KB â†’ RAGAS evaluates with empty â†’ Foundry scores      â”‚
â”‚                                                              â”‚
â”‚ Results:                                                     â”‚
â”‚ â€¢ Faithfulness: 0.5 (can't verify without KB)               â”‚
â”‚ â€¢ Context Recall: 0.0 (nothing to recall)                   â”‚
â”‚ â€¢ Context Precision: 0.0 (no KB)                            â”‚
â”‚ â€¢ Answer Relevance: 0.22 (query-response match)             â”‚
â”‚ â€¢ Answer Correctness: 0.75 (response quality)               â”‚
â”‚                                                              â”‚
â”‚ âœ… Validates the evaluation system works                    â”‚
â”‚ âœ… No actual KB content needed yet                          â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### Scenario B: Populated LOCAL KB
```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ "context": ["PlayReady protects media", "Multi-platform", ...]
â”‚                                                              â”‚
â”‚ Flow:                                                        â”‚
â”‚ Your KB â†’ RAGAS evaluates â†’ Foundry scores                  â”‚
â”‚                                                              â”‚
â”‚ Foundry LLM checks:                                          â”‚
â”‚ "Does response match these documents?"                      â”‚
â”‚ "Are these documents complete?"                             â”‚
â”‚ "Is all this relevant?"                                     â”‚
â”‚                                                              â”‚
â”‚ Results:                                                     â”‚
â”‚ â€¢ Faithfulness: 0.92 (matches KB)                           â”‚
â”‚ â€¢ Context Recall: 0.85 (KB has needed facts)                â”‚
â”‚ â€¢ Context Precision: 0.90 (KB is relevant)                  â”‚
â”‚ â€¢ Answer Relevance: 0.88 (addresses query)                  â”‚
â”‚ â€¢ Answer Correctness: 0.87 (factually accurate)             â”‚
â”‚                                                              â”‚
â”‚ âœ… Real RAG system evaluation                               â”‚
â”‚ âœ… Shows how good your KB is                                â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### Scenario C: Fetching KB from Foundry
```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Future Enhancement:                                          â”‚
â”‚                                                              â”‚
â”‚ Flow:                                                        â”‚
â”‚ 1. Query Foundry KB: project_client.search_kb(query)        â”‚
â”‚ 2. Get Results: [doc1, doc2, doc3]                          â”‚
â”‚ 3. Add to context: test_case["context"] = results           â”‚
â”‚ 4. Then evaluate: Same as Scenario B                        â”‚
â”‚                                                              â”‚
â”‚ "context": [Docs fetched from Foundry KB]                   â”‚
â”‚            â†“                                                 â”‚
â”‚ RAGAS + Foundry LLM evaluate = Full RAG validation          â”‚
â”‚                                                              â”‚
â”‚ âœ… Uses Foundry KB for context retrieval                    â”‚
â”‚ âœ… Uses Foundry LLM for evaluation                          â”‚
â”‚ âœ… Uses RAGAS for metrics                                   â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## â“ SINGLE PATH Clarification

**Question: Is it from single path?**

**Answer: YES âœ… - SINGLE LOCAL PATH**

```
SINGLE PATH:
data/processed/test_cases_formatted.json
    â†“
    Contains: query, response, context
    â†“
    "context" field = YOUR KNOWLEDGE BASE
    â†“
    Used by RAGAS metrics
    â†“
    Scored by Foundry LLM
    â†“
    Results exported to JSON + Excel

Everything flows from ONE LOCAL FILE
Everything uses the "context" field from that file
```

---

## ðŸ“‹ Summary

| Aspect | Answer | Source |
|--------|--------|--------|
| **KB Source** | LOCAL | data/processed/test_cases_formatted.json |
| **KB Field** | context | "context": [] in JSON |
| **KB User** | RAGAS | Metrics evaluate it |
| **KB Scorer** | Foundry LLM | Evaluates against KB |
| **Single Path** | YES | Everything through context field |
| **Current Status** | Empty | Mock testing mode |
| **Future Status** | Populated | Real RAG testing |

---

## âœ… KEY INSIGHT

**Your knowledge base is in ONE PLACE, flows through ONE PATH:**

```
Your KB (context field)
    â†“
RAGAS (uses it to evaluate)
    â†“
Foundry LLM (scores it)
    â†“
Results (show KB quality)
```

**It's a SINGLE UNIFIED PATH from LOCAL JSON through RAGAS to Foundry scoring.**


