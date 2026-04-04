#!/usr/bin/env python3
"""Extract knowledge base from PDF and populate test cases with context."""

import json
import logging
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple

try:
    from PyPDF2 import PdfReader  # type: ignore
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    PdfReader = None  # type: ignore
    print("Warning: PyPDF2 not available. Install: pip install PyPDF2")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PDFKnowledgeBaseLoader:
    """Load PDF and extract knowledge base for RAG evaluation."""
    
    def __init__(self, pdf_path: str) -> None:
        """Initialize loader with PDF path."""
        self.pdf_path = Path(pdf_path)
        self.content: str = ""
        self.chunks: List[str] = []
        
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    def extract_text(self) -> bool:
        """Extract text from PDF or text file."""
        try:
            if not self.pdf_path.exists():
                logger.error(f"File not found: {self.pdf_path}")
                return False
            
            # Handle .txt files (fallback)
            if self.pdf_path.suffix.lower() == '.txt':
                logger.info("Reading text file...")
                with open(self.pdf_path, 'r', encoding='utf-8') as f:
                    self.content = f.read()
                logger.info(f"Extracted {len(self.content)} characters from text file")
                return True
            
            # Handle PDF files
            if not PDF_AVAILABLE:
                logger.error("PyPDF2 not available. Install: pip install PyPDF2")
                return False
            
            reader = PdfReader(str(self.pdf_path))  # type: ignore
            text_parts: List[str] = []
            logger.info(f"Extracting from {len(reader.pages)} pages...")
            
            for page_num, page in enumerate(reader.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        text_parts.append(page_text)
                        logger.debug(f"Page {page_num}: {len(page_text)} chars")
                except Exception as err:
                    logger.warning(f"Error extracting page {page_num}: {err}")
            
            if not text_parts:
                logger.warning("No text extracted from PDF")
                return False
            
            self.content = "\n\n".join(text_parts)
            logger.info(f"Extracted {len(self.content)} total characters from PDF")
            return True
            
        except Exception as err:
            logger.error(f"Error extracting text: {err}")
            return False
    
    def chunk_content(self, chunk_size: int = 800, overlap: int = 400) -> bool:
        """Split content into overlapping chunks (Foundry standard: 800 tokens)."""
        if not self.content:
            logger.error("No content to chunk. Extract PDF first.")
            return False
        
        try:
            chunks: List[str] = []
            step = chunk_size - overlap
            
            # Approximate: 1 token ≈ 4 characters
            char_chunk_size = chunk_size * 4
            char_step = step * 4
            
            for i in range(0, len(self.content), char_step):
                chunk = self.content[i:i + char_chunk_size]
                if chunk.strip():
                    # Clean up whitespace
                    chunk = " ".join(chunk.split())
                    if len(chunk) > 50:  # Minimum meaningful chunk
                        chunks.append(chunk)
            
            self.chunks = chunks
            logger.info(f"Created {len(chunks)} chunks (avg ~800 tokens each)")
            return True
            
        except Exception as err:
            logger.error(f"Error chunking content: {err}")
            return False
    
    def get_context_for_query(self, query: str, num_chunks: int = 3) -> List[str]:
        """Get relevant context chunks for a query."""
        if not self.chunks:
            logger.warning("No chunks available")
            return []
        
        # Simple relevance: return first N chunks (can be enhanced with semantic search)
        num_chunks = min(num_chunks, len(self.chunks))
        context = self.chunks[:num_chunks]
        logger.debug(f"Retrieved {len(context)} chunks for query")
        return context


def load_test_cases(test_cases_path: str) -> List[Dict[str, Any]]:
    """Load test cases from JSON file."""
    try:
        with open(test_cases_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Handle both list and dict with 'test_cases' key
        if isinstance(data, dict):
            test_cases = data.get('test_cases', [])
        else:
            test_cases = data
        
        logger.info(f"Loaded {len(test_cases)} test cases")
        return test_cases
        
    except Exception as err:
        logger.error(f"Error loading test cases: {err}")
        return []


def populate_context(test_cases: List[Dict[str, Any]], loader: PDFKnowledgeBaseLoader) -> List[Dict[str, Any]]:
    """Add KB context to test cases."""
    try:
        updated_cases = []
        
        for i, case in enumerate(test_cases):
            # Get context for this query
            query = case.get('query', '')
            context = loader.get_context_for_query(query, num_chunks=3)
            
            # Update case with context
            case['context'] = context
            updated_cases.append(case)
            
            if (i + 1) % 20 == 0:
                logger.info(f"Populated context for {i + 1}/{len(test_cases)} cases")
        
        logger.info(f"Successfully populated context for {len(updated_cases)} test cases")
        return updated_cases
        
    except Exception as err:
        logger.error(f"Error populating context: {err}")
        return []


def save_test_cases(test_cases: List[Dict[str, Any]], output_path: str) -> bool:
    """Save updated test cases to JSON file."""
    try:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Save in same format as input
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(test_cases, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(test_cases)} test cases to {output_path}")
        return True
        
    except Exception as err:
        logger.error(f"Error saving test cases: {err}")
        return False


def main() -> int:
    """Main execution function."""
    try:
        # Paths
        base_path = Path(__file__).parent.parent
        
        # Prefer PDF when PyPDF2 is available, otherwise fall back to TXT
        pdf_path = base_path / "data" / "raw" / "playready_kb.pdf"
        txt_path = base_path / "data" / "raw" / "playready_kb.txt"
        if pdf_path.exists() and PDF_AVAILABLE:
            kb_path = pdf_path
        elif txt_path.exists():
            kb_path = txt_path
        else:
            kb_path = pdf_path if pdf_path.exists() else txt_path
        
        input_override = os.getenv("TEST_CASES_PATH")
        output_override = os.getenv("OUTPUT_TEST_CASES_PATH")

        input_test_cases = Path(input_override) if input_override else (base_path / "data" / "processed" / "test_cases_formatted.json")
        if output_override:
            output_test_cases = Path(output_override)
        elif input_test_cases.name == "test_cases_formatted.json":
            output_test_cases = base_path / "data" / "processed" / "test_cases_with_kb.json"
        else:
            output_test_cases = input_test_cases.with_name(f"{input_test_cases.stem}_with_kb.json")
        
        logger.info("=" * 80)
        logger.info("PDF Knowledge Base Loader")
        logger.info("=" * 80)
        
        # Check which file we're using
        if not kb_path.exists():
            logger.error(f"Knowledge base file not found: {pdf_path} or {txt_path}")
            return 1
        
        logger.info(f"Using KB file: {kb_path.name}")
        
        # Step 1: Load PDF/TXT and extract text
        logger.info("\n[Step 1/4] Loading and extracting knowledge base...")
        loader = PDFKnowledgeBaseLoader(str(kb_path))
        
        if not loader.extract_text():
            logger.error("Failed to extract text from knowledge base")
            return 1
        
        # Step 2: Chunk content
        logger.info("\n[Step 2/4] Chunking content (800 tokens, 400 overlap)...")
        if not loader.chunk_content(chunk_size=800, overlap=400):
            logger.error("Failed to chunk content")
            return 1
        
        # Step 3: Load test cases
        logger.info("\n[Step 3/4] Loading test cases...")
        test_cases = load_test_cases(str(input_test_cases))
        if not test_cases:
            logger.error("No test cases loaded")
            return 1
        
        # Step 4: Populate context and save
        logger.info("\n[Step 4/4] Populating KB context in test cases...")
        updated_cases = populate_context(test_cases, loader)
        
        if not save_test_cases(updated_cases, str(output_test_cases)):
            logger.error("Failed to save test cases")
            return 1
        
        # Summary
        logger.info("\n" + "=" * 80)
        logger.info("KB Integration Complete!")
        logger.info("=" * 80)
        logger.info(f"✓ KB extracted: {len(loader.content)} characters")
        logger.info(f"✓ Created {len(loader.chunks)} KB chunks (~800 tokens each)")
        logger.info(f"✓ Populated {len(updated_cases)} test cases with context")
        logger.info(f"✓ Output: {output_test_cases}")
        logger.info("\nNext: Run RAGAS evaluation with real KB context")
        logger.info("=" * 80)
        
        return 0
        
    except Exception as err:
        logger.error(f"Fatal error: {err}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
