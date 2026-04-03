"""
Integration tests for PlayReady QA with Foundry upload
Run: pytest tests/integration/test_playready_qa.py -v
"""

import pytest
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

from src.evaluators.evaluation_metrics import EvaluationMetrics, EvaluationScore
from src.core.config import config


class TestPlayReadyQA:
    """Test PlayReady Q&A accuracy"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment"""
        self.metrics = EvaluationMetrics(
            knowledge_base_path=config.rag.knowledge_base_path
        )
        self.results_dir = Path(config.local_storage.results_path)
        self.results_dir.mkdir(exist_ok=True)
    
    def test_knowledge_base_loaded(self):
        """Verify knowledge base is loaded"""
        assert self.metrics.kb_content, "Knowledge base is empty"
        print(f"✅ KB loaded: {len(self.metrics.kb_content)} characters")
    
    def test_groundedness_score(self):
        """Test groundedness calculation"""
        response = "PlayReady is a DRM solution that protects video content"
        context = [
            "PlayReady is a DRM solution",
            "It protects video content using encryption"
        ]
        
        score = self.metrics.calculate_groundedness(response, context)
        
        assert 0 <= score <= 1
        print(f"✅ Groundedness score: {score}")
    
    def test_relevance_score(self):
        """Test relevance calculation"""
        query = "What is PlayReady?"
        context = [
            "PlayReady is a DRM solution",
            "DRM protection uses encryption",
            "PlayReady supports video protection"
        ]
        
        score = self.metrics.calculate_relevance(query, context)
        
        assert 0 <= score <= 1
        print(f"✅ Relevance score: {score}")
    
    def test_coherence_score(self):
        """Test coherence calculation"""
        response = (
            "PlayReady is a DRM solution. It protects video content. "
            "It uses encryption and licensing. "
            "This ensures secure content delivery."
        )
        
        score = self.metrics.calculate_coherence(response)
        
        assert 0 <= score <= 1
        print(f"✅ Coherence score: {score}")
    
    def test_accuracy_score(self):
        """Test accuracy calculation"""
        query = "What is PlayReady?"
        response = "PlayReady is a DRM solution that protects video"
        
        score = self.metrics.calculate_accuracy(response, query)
        
        assert 0 <= score <= 1
        print(f"✅ Accuracy score: {score}")
    
    def test_complete_evaluation(self):
        """Test complete evaluation"""
        test_cases = [
            {
                "query": "What is PlayReady?",
                "response": "PlayReady is a DRM solution that protects video content using encryption and licensing mechanisms.",
                "context": [
                    "PlayReady is a DRM solution",
                    "It protects video content",
                    "Uses encryption and licensing"
                ]
            },
            {
                "query": "How does DRM work?",
                "response": "DRM works by encrypting content and controlling access through licensing agreements.",
                "context": [
                    "DRM uses encryption",
                    "Licensing controls access",
                    "Content is protected during delivery"
                ]
            }
        ]
        
        results = self.metrics.batch_evaluate(test_cases)
        
        assert len(results) == 2
        
        results_data = [r.to_dict() for r in results]
        
        results_file = self.results_dir / "test_results.json"
        with open(results_file, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        print(f"✅ Saved {len(results)} evaluation results")
        
        for i, result in enumerate(results):
            print(f"\nTest {i+1}:")
            print(f"  Query: {result.query}")
            print(f"  Groundedness: {result.groundedness}")
            print(f"  Relevance: {result.relevance}")
            print(f"  Coherence: {result.coherence}")
            print(f"  Accuracy: {result.accuracy}")
            print(f"  Overall: {result.overall}")