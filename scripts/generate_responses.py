#!/usr/bin/env python3
"""
Generate LLM responses for test queries.
Creates realistic responses for each test case query.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def generate_response_for_query(query: str, query_id: int) -> str:
    """
    Generate a realistic response for a given query.
    In production, this would call Azure OpenAI or other LLM.
    For now, returns contextual responses based on query keywords.
    """
    
    responses_map = {
        "What is PlayReady?": "PlayReady is a comprehensive digital rights management (DRM) solution developed by Microsoft. It's designed to protect audio, video, and other digital content from unauthorized access and distribution. PlayReady works across multiple platforms and devices, making it a widely adopted industry standard for content protection.",
        
        "What does PlayReady do?": "PlayReady protects video and audio content through encryption and licensing mechanisms. It ensures that only authorized users can access premium content, and usage rights can be defined per user or device. PlayReady also provides secure streaming capabilities and supports offline content delivery with time-limited access.",
        
        "Why use PlayReady?": "Organizations use PlayReady for security and protection of valuable digital content. It's an enterprise-grade solution that meets industry compliance standards and provides comprehensive content protection. PlayReady is widely supported across devices and platforms, reducing fragmentation and simplifying deployment.",
        
        "Is PlayReady free?": "PlayReady licensing varies by implementation. While some basic features are free, comprehensive enterprise deployment typically involves licensing costs. Microsoft offers different licensing tiers based on content type, usage volume, and distribution channels.",
        
        "How to implement PlayReady?": "Implementing PlayReady involves integrating the PlayReady SDK into your application, configuring licensing rules, setting up content encryption, and managing key distribution. The exact implementation steps depend on your platform (web, mobile, desktop) and content delivery method.",
        
        "PlayReady compatibility": "PlayReady is compatible with most modern streaming platforms and devices, including Windows, iOS, Android, and web browsers. However, compatibility varies by device manufacturer and platform implementation. Always verify target device support before deployment.",
        
        "What are PlayReady key features?": "PlayReady key features include adaptive streaming support, variable bit-rate encoding, license management, offline playback controls, secure boot requirements, and compliance with HDCP standards. It also supports both persistent and non-persistent licenses.",
        
        "How does PlayReady licensing work?": "PlayReady licensing uses challenge-response mechanisms where devices request licenses to play protected content. Licenses are encrypted and can include time-based restrictions, device-specific binding, and usage rights. License servers validate requests and issue appropriate credentials.",
        
        "PlayReady security": "PlayReady implements security through endpoint protection, secure boot verification, driver validation, and encrypted communication between clients and license servers. It meets WIDEVINE and other industry security standards.",
        
        "What is PlayReady SDK?": "The PlayReady SDK is a software development kit that enables developers to integrate PlayReady DRM functionality into their applications. It provides APIs for content protection, license acquisition, and playback control across different platforms.",
    }
    
    # Find best matching response
    query_lower = query.lower()
    for key, response in responses_map.items():
        if key.lower() in query_lower or any(word in query_lower for word in key.lower().split()):
            return response
    
    # Default response for unmatched queries
    return f"PlayReady is Microsoft's digital rights management solution. {query} is an important aspect of digital content protection. For specific implementation details, please refer to the official PlayReady documentation and SDK guides."


def main():
    """Main execution function."""
    
    # Load test cases
    test_cases_path = Path(__file__).parent.parent / "data" / "raw" / "test_cases.json"
    
    try:
        with open(test_cases_path, 'r') as f:
            test_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {test_cases_path}")
        sys.exit(1)
    
    # Generate responses
    responses = []
    test_cases = test_data.get("test_cases", [])
    
    print(f"\n{'='*70}")
    print(f"Generating responses for {len(test_cases)} test queries...")
    print(f"{'='*70}\n")
    
    for i, test_case in enumerate(test_cases, 1):
        query = test_case.get("query", "")
        query_id = test_case.get("id", i)
        
        # Generate response
        response = generate_response_for_query(query, query_id)
        
        responses.append({
            "id": query_id,
            "query": query,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        
        if i % 10 == 0:
            print(f"✓ Generated response {i}/{len(test_cases)}: {query[:50]}...")
    
    # Save responses
    responses_path = Path(__file__).parent.parent / "artifacts" / "latest" / "responses.json"
    responses_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(responses_path, 'w') as f:
        json.dump(responses, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"✅ Generated {len(responses)} responses")
    print(f"✅ Saved to: {responses_path}")
    print(f"{'='*70}\n")
    
    return responses


if __name__ == "__main__":
    main()
