#!/usr/bin/env python3
"""
Merge generated responses with test cases to create Foundry SDK format.
Foundry SDK requires: query, response, context fields for each test case.
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any


def merge_responses_into_testcases(
    test_cases_path: Path,
    responses_path: Path,
    output_path: Path
) -> List[Dict[str, Any]]:
    """
    Merge responses into test cases format compatible with Foundry SDK.
    
    Foundry SDK Requirements:
    - Each test case must have: query, response, context
    - context is typically array of relevant documents/passages
    - All three fields are mandatory
    """
    
    # Load test cases
    try:
        with open(test_cases_path, 'r') as f:
            test_data = json.load(f)
        test_cases = test_data.get("test_cases", [])
    except FileNotFoundError:
        print(f"Error: Could not find {test_cases_path}")
        sys.exit(1)
    
    # Load responses
    try:
        with open(responses_path, 'r') as f:
            responses_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {responses_path}")
        sys.exit(1)
    
    # Create lookup map for responses by ID
    responses_map = {r.get("id"): r.get("response", "") for r in responses_data}
    
    print(f"\n{'='*70}")
    print("Merging responses into Foundry SDK format...")
    print(f"Test Cases: {len(test_cases)}")
    print(f"Responses: {len(responses_data)}")
    print(f"{'='*70}\n")
    
    # Merge test cases with responses
    formatted_cases = []
    
    for test_case in test_cases:
        case_id = test_case.get("id")
        query = test_case.get("query", "")
        response = responses_map.get(case_id, "")
        
        # Foundry SDK format
        formatted_case = {
            "query": query,
            "response": response,
            "context": [],  # Empty context - can be populated with relevant documents
            "metadata": {
                "id": case_id,
                "category": test_case.get("category", ""),
                "difficulty": test_case.get("difficulty", ""),
                "priority": test_case.get("priority", ""),
                "expected_keywords": test_case.get("expected_keywords", [])
            }
        }
        
        formatted_cases.append(formatted_case)
    
    # Validate format
    validation_results = validate_foundry_format(formatted_cases)
    
    if not validation_results["all_valid"]:
        print("⚠️  Validation issues found:")
        if validation_results["missing_query"] > 0:
            print(f"  - {validation_results['missing_query']} cases missing 'query'")
        if validation_results["missing_response"] > 0:
            print(f"  - {validation_results['missing_response']} cases missing 'response'")
        if validation_results["missing_context"] > 0:
            print(f"  - {validation_results['missing_context']} cases missing 'context'")
    else:
        print("✅ All cases passed Foundry SDK format validation")
    
    # Save formatted test cases
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(formatted_cases, f, indent=2)
    
    print(f"\n✅ Formatted {len(formatted_cases)} test cases")
    print(f"✅ Saved to: {output_path}")
    
    # Print summary
    print(f"\n{'='*70}")
    print("Foundry SDK Format Summary:")
    print(f"  Total Cases: {len(formatted_cases)}")
    print(f"  With Query: {sum(1 for c in formatted_cases if c.get('query'))}")
    print(f"  With Response: {sum(1 for c in formatted_cases if c.get('response'))}")
    print(f"  With Context: {sum(1 for c in formatted_cases if 'context' in c)}")
    print(f"  Status: READY FOR FOUNDRY SDK ✓")
    print(f"{'='*70}\n")
    
    return formatted_cases


def validate_foundry_format(test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validate test cases against Foundry SDK requirements.
    
    Returns validation summary dict.
    """
    
    results = {
        "total": len(test_cases),
        "valid": 0,
        "missing_query": 0,
        "missing_response": 0,
        "missing_context": 0,
        "all_valid": True
    }
    
    for case in test_cases:
        is_valid = True
        
        if not case.get("query"):
            results["missing_query"] += 1
            is_valid = False
            
        if not case.get("response"):
            results["missing_response"] += 1
            is_valid = False
            
        if "context" not in case:
            results["missing_context"] += 1
            is_valid = False
        
        if is_valid:
            results["valid"] += 1
        else:
            results["all_valid"] = False
    
    return results


def main():
    """Main execution function."""
    
    base_path = Path(__file__).parent.parent
    
    test_cases_path = base_path / "data" / "raw" / "test_cases.json"
    responses_path = base_path / "artifacts" / "latest" / "responses.json"
    output_path = base_path / "data" / "processed" / "test_cases_formatted.json"
    
    formatted_cases = merge_responses_into_testcases(
        test_cases_path,
        responses_path,
        output_path
    )
    
    return formatted_cases


if __name__ == "__main__":
    main()
