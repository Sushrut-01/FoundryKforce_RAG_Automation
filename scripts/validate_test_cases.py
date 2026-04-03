#!/usr/bin/env python3
"""
Validate test cases against Foundry SDK acceptance criteria.
Checks required fields and format compliance.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any


def validate_foundry_sdk_format(test_cases_path: Path) -> Dict[str, Any]:
    """
    Validate test cases against Foundry SDK requirements.
    
    Required fields:
    - query: str, non-empty
    - response: str, can be empty but field must exist
    - context: list, can be empty but field must exist
    
    Returns: validation report dict
    """
    
    try:
        with open(test_cases_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {test_cases_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {test_cases_path}")
        sys.exit(1)
    
    # Handle both array and object formats
    if isinstance(data, list):
        test_cases = data
    elif isinstance(data, dict) and "test_cases" in data:
        test_cases = data["test_cases"]
    else:
        test_cases = [data]
    
    print(f"\n{'='*70}")
    print("Foundry SDK Format Validation Report")
    print(f"{'='*70}\n")
    
    total = len(test_cases)
    errors = []
    warnings = []
    
    # Field validation
    with_query = 0
    with_response = 0
    with_context = 0
    valid_cases = 0
    
    for i, case in enumerate(test_cases, 1):
        case_errors = []
        
        # Check required fields
        if "query" not in case:
            case_errors.append("Missing 'query' field")
        elif not isinstance(case["query"], str):
            case_errors.append(f"'query' must be string, got {type(case['query']).__name__}")
        elif not case["query"].strip():
            case_errors.append("'query' is empty string")
        else:
            with_query += 1
        
        if "response" not in case:
            case_errors.append("Missing 'response' field")
        elif not isinstance(case["response"], str):
            case_errors.append(f"'response' must be string, got {type(case['response']).__name__}")
        else:
            with_response += 1
        
        if "context" not in case:
            case_errors.append("Missing 'context' field")
        elif not isinstance(case["context"], (list, str)):
            case_errors.append(f"'context' must be list or string, got {type(case['context']).__name__}")
        else:
            with_context += 1
        
        # Report errors
        if case_errors:
            errors.append({
                "case_id": case.get("id", i),
                "query": case.get("query", "N/A")[:50],
                "errors": case_errors
            })
        else:
            valid_cases += 1
    
    # Generate report
    print(f"Total test cases: {total}")
    print(f"With 'query' field: {with_query}/{total} ✓")
    print(f"With 'response' field: {with_response}/{total} ✓")
    print(f"With 'context' field: {with_context}/{total} ✓")
    print(f"Valid cases (all required fields): {valid_cases}/{total}")
    
    if valid_cases == total:
        print(f"\n✅ ALL {total} CASES PASS FOUNDRY SDK CRITERIA ✅")
        status = "READY"
    else:
        print(f"\n⚠️  {len(errors)} CASES HAVE ISSUES")
        status = "NEEDS FIXES"
        
        print(f"\nDetailed Errors:")
        for error_info in errors[:10]:  # Show first 10 errors
            print(f"\n  Case ID: {error_info['case_id']}")
            print(f"  Query: {error_info['query']}...")
            for err in error_info['errors']:
                print(f"    ✗ {err}")
        
        if len(errors) > 10:
            print(f"\n  ... and {len(errors) - 10} more errors")
    
    print(f"\n{'='*70}")
    print(f"Validation Status: {status}")
    print(f"{'='*70}\n")
    
    return {
        "total": total,
        "valid": valid_cases,
        "with_query": with_query,
        "with_response": with_response,
        "with_context": with_context,
        "errors": errors,
        "status": status
    }


def main():
    """Main execution function."""
    
    # Try to find test cases file
    base_path = Path(__file__).parent.parent
    
    # Check different possible locations
    possible_paths = [
        base_path / "data" / "test_cases_formatted.json",
        base_path / "data" / "test_cases.json",
    ]
    
    test_cases_path = None
    for path in possible_paths:
        if path.exists():
            test_cases_path = path
            print(f"Found test cases at: {path}")
            break
    
    if not test_cases_path:
        print("Error: Could not find test cases file")
        print("Expected locations:")
        for path in possible_paths:
            print(f"  - {path}")
        sys.exit(1)
    
    # Validate
    results = validate_foundry_sdk_format(test_cases_path)
    
    return results


if __name__ == "__main__":
    main()
