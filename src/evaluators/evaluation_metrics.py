"""
Evaluation metrics for RAG responses
Calculate groundedness, relevance, coherence, and accuracy
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import json
from datetime import datetime

@dataclass
class EvaluationScore:
    """Represents evaluation scores for a response"""
    query: str
    response: str
    retrieved_context: List[str]
    groundedness: float
    relevance: float
    coherence: float
    accuracy: float
    overall: float
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "query": self.query,
            "response": self.response,
            "context": self.retrieved_context,
            "scores": {
                "groundedness": round(self.groundedness, 4),
                "relevance": round(self.relevance, 4),
                "coherence": round(self.coherence, 4),
                "accuracy": round(self.accuracy, 4),
                "overall": round(self.overall, 4)
            },
            "timestamp": self.timestamp
        }

class EvaluationMetrics:
    """Calculate evaluation metrics for RAG responses"""
    
    def __init__(self, knowledge_base_path: str = "./knowledge_base"):
        """Initialize metrics calculator"""
        self.kb_path = Path(knowledge_base_path)
        self.kb_content = self._load_knowledge_base()
    
    def _load_knowledge_base(self) -> str:
        """Load all knowledge base content"""
        content = ""
        if self.kb_path.exists():
            for file in self.kb_path.glob("*.txt"):
                with open(file, 'r', encoding='utf-8') as f:
                    content += f.read() + "\n"
        return content.lower()
    
    def calculate_groundedness(self, response: str, context: List[str]) -> float:
        """Calculate groundedness score"""
        if not response or not context:
            return 0.0
        
        response_lower = response.lower()
        context_joined = " ".join(context).lower()
        
        response_words = response_lower.split()
        grounded_words = sum(1 for word in response_words 
                           if word in context_joined and len(word) > 3)
        
        score = min(1.0, grounded_words / len(response_words)) if response_words else 0.0
        return round(score, 4)
    
    def calculate_relevance(self, query: str, context: List[str]) -> float:
        """Calculate relevance score"""
        if not query or not context:
            return 0.0
        
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        relevance_scores = []
        for chunk in context:
            chunk_lower = chunk.lower()
            matching_words = sum(1 for word in query_words 
                               if word in chunk_lower and len(word) > 3)
            relevance_scores.append(min(1.0, matching_words / len(query_words)) 
                                  if query_words else 0.0)
        
        avg_relevance = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0.0
        return round(avg_relevance, 4)
    
    def calculate_coherence(self, response: str) -> float:
        """Calculate coherence score"""
        if not response:
            return 0.0
        
        checks = 0
        score = 0
        
        sentences = response.split('.')
        if len(sentences) > 1:
            score += 0.3
        checks += 0.3
        
        words = response.split()
        if 10 < len(words) < 1000:
            score += 0.3
        checks += 0.3
        
        words_lower = [w.lower() for w in words if len(w) > 3]
        if words_lower:
            unique_ratio = len(set(words_lower)) / len(words_lower)
            if unique_ratio > 0.5:
                score += 0.4
        checks += 0.4
        
        final_score = (score / checks) if checks > 0 else 0.0
        return round(final_score, 4)
    
    def calculate_accuracy(self, response: str, query: str) -> float:
        """Calculate accuracy score"""
        if not response or not query:
            return 0.0
        
        response_lower = response.lower()
        query_lower = query.lower()
        
        query_words = [w for w in query_lower.split() if len(w) > 3]
        matching = sum(1 for word in query_words if word in response_lower)
        
        accuracy = (matching / len(query_words)) if query_words else 0.0
        return round(min(1.0, accuracy), 4)
    
    def evaluate_response(
        self,
        query: str,
        response: str,
        context: List[str]
    ) -> EvaluationScore:
        """Evaluate a complete response"""
        groundedness = self.calculate_groundedness(response, context)
        relevance = self.calculate_relevance(query, context)
        coherence = self.calculate_coherence(response)
        accuracy = self.calculate_accuracy(response, query)
        
        overall = (groundedness + relevance + coherence + accuracy) / 4
        
        return EvaluationScore(
            query=query,
            response=response,
            retrieved_context=context,
            groundedness=groundedness,
            relevance=relevance,
            coherence=coherence,
            accuracy=accuracy,
            overall=overall
        )
    
    def batch_evaluate(
        self,
        test_cases: List[Dict[str, Any]]
    ) -> List[EvaluationScore]:
        """Evaluate multiple test cases"""
        results = []
        for test_case in test_cases:
            score = self.evaluate_response(
                query=test_case["query"],
                response=test_case["response"],
                context=test_case["context"]
            )
            results.append(score)
        
        return results