"""
Upload local test results to Foundry UI
Run: python scripts/upload_to_foundry.py
"""

import asyncio
import argparse
import logging
from pathlib import Path
from dotenv import load_dotenv
import os
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

from src.core.foundry_uploader import FoundryUploader
from src.core.config import config

async def main():
    parser = argparse.ArgumentParser(
        description="Upload test results to Foundry UI"
    )
    parser.add_argument(
        "--results",
        default="./artifacts/latest/test_results.json",
        help="Path to results file"
    )
    parser.add_argument(
        "--experiment",
        default="playready-rag-qa-test",
        help="Experiment name"
    )
    parser.add_argument(
        "--tags",
        default="local-test,qa,playready",
        help="Comma-separated tags"
    )
    
    args = parser.parse_args()
    
    try:
        logger.info("🔌 Initializing Foundry uploader...")
        uploader = FoundryUploader(
            project_endpoint=config.azure.ai_project_endpoint,
            subscription_id=config.azure.subscription_id
        )
        
        tags = [t.strip() for t in args.tags.split(',')]
        
        results_path = Path(args.results)
        if not results_path.exists():
            logger.warning(f"⚠️  Results file not found: {args.results}")
            logger.info("💡 Make sure to run pytest first: pytest tests/ -v")
            return
        
        logger.info(f"📖 Reading results from: {args.results}")
        with open(results_path, 'r') as f:
            results = json.load(f)
        
        logger.info(f"📤 Uploading to Foundry...")
        response = await uploader.upload_results(
            results=results,
            experiment_name=args.experiment,
            tags=tags
        )
        
        logger.info("✅ Upload successful!")
        logger.info(f"   Experiment: {args.experiment}")
        logger.info(f"   Metrics:")
        for metric, value in response.get("metrics", {}).items():
            logger.info(f"      - {metric}: {value}")
        
        url = uploader.get_experiment_url(args.experiment)
        logger.info(f"\n🌐 View results in Foundry:")
        logger.info(f"   {url}")
        
    except Exception as e:
        logger.error(f"❌ Upload failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())