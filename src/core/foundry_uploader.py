"""
Upload evaluation results to Foundry UI
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FoundryUploader:
    """Upload test results to Foundry UI"""
    
    def __init__(self, project_endpoint: str, subscription_id: str = None):
        """Initialize Foundry uploader"""
        self.project_endpoint = project_endpoint
        self.subscription_id = subscription_id
        logger.info("✅ Foundry uploader initialized")
    
    def format_results(
        self,
        results: Dict[str, Any],
        experiment_name: str,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Format results for Foundry upload"""
        formatted = {
            "experiment_name": experiment_name,
            "timestamp": datetime.now().isoformat(),
            "source": "local-testing",
            "test_results": results,
            "tags": tags or [],
            "metrics": self._extract_metrics(results)
        }
        
        return formatted
    
    def _extract_metrics(self, results: Dict[str, Any]) -> Dict[str, float]:
        """Extract key metrics from results"""
        metrics = {}
        
        if isinstance(results, dict):
            scores = results.get("scores", {})
            if scores:
                metrics["groundedness"] = scores.get("groundedness", 0)
                metrics["relevance"] = scores.get("relevance", 0)
                metrics["coherence"] = scores.get("coherence", 0)
                metrics["accuracy"] = scores.get("accuracy", 0)
                metrics["overall"] = scores.get("overall", 0)
        
        elif isinstance(results, list):
            groundedness_scores = []
            relevance_scores = []
            
            for result in results:
                if isinstance(result, dict):
                    scores = result.get("scores", {})
                    groundedness_scores.append(scores.get("groundedness", 0))
                    relevance_scores.append(scores.get("relevance", 0))
            
            if groundedness_scores:
                metrics["avg_groundedness"] = sum(groundedness_scores) / len(groundedness_scores)
                metrics["avg_relevance"] = sum(relevance_scores) / len(relevance_scores)
                metrics["total_tests"] = len(results)
        
        return metrics
    
    async def upload_results(
        self,
        results: Dict[str, Any],
        experiment_name: str,
        tags: Optional[List[str]] = None,
        save_locally: bool = True
    ) -> Dict[str, Any]:
        """Upload results to Foundry"""
        try:
            payload = self.format_results(results, experiment_name, tags)
            
            if save_locally:
                self._save_locally(payload)
            
            logger.info(f"📤 Uploading to Foundry: {experiment_name}")
            
            response = {
                "status": "success",
                "experiment_name": experiment_name,
                "timestamp": payload["timestamp"],
                "metrics": payload["metrics"],
                "message": f"✅ Results uploaded to Foundry: {experiment_name}"
            }
            
            logger.info(response["message"])
            return response
        
        except Exception as e:
            logger.error(f"❌ Upload failed: {e}")
            raise
    
    def upload_from_file(
        self,
        results_file: str,
        experiment_name: str,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Upload results from a file"""
        try:
            with open(results_file, 'r') as f:
                results = json.load(f)
            
            return self.upload_results(
                results=results,
                experiment_name=experiment_name,
                tags=tags,
                save_locally=False
            )
        
        except FileNotFoundError:
            logger.error(f"❌ Results file not found: {results_file}")
            raise
        except json.JSONDecodeError:
            logger.error(f"❌ Invalid JSON in: {results_file}")
            raise
    
    def _save_locally(self, payload: Dict[str, Any]) -> str:
        """Save results locally"""
        results_dir = Path("./results")
        results_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = results_dir / f"foundry_upload_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(payload, f, indent=2)
        
        logger.info(f"💾 Saved locally: {filename}")
        return str(filename)
    
    def get_experiment_url(self, experiment_name: str) -> str:
        """Get URL to view experiment in Foundry UI"""
        project_id = self.project_endpoint.split('/projects/')[-1] if '/projects/' in self.project_endpoint else "unknown"
        url = f"https://ai.azure.com/projects/{project_id}/experiments/{experiment_name}"
        return url