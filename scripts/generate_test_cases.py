"""
Generate 100+ test cases for PlayReady QA testing
Run: python scripts/generate_test_cases.py
"""

import json
from pathlib import Path

# Sample questions and keywords
PLAYREADY_QUESTIONS = [
    # General (10 cases)
    ("What is PlayReady?", ["DRM", "solution", "protect", "content"]),
    ("What does PlayReady do?", ["protect", "video", "content", "security"]),
    ("Why use PlayReady?", ["security", "protection", "enterprise", "standard"]),
    ("Is PlayReady free?", ["free", "cost", "licensing", "model"]),
    ("Who uses PlayReady?", ["companies", "enterprise", "streaming", "providers"]),
    ("How old is PlayReady?", ["technology", "Microsoft", "established", "years"]),
    ("What is PlayReady alternative?", ["competitor", "alternative", "similar", "option"]),
    ("Does Netflix use PlayReady?", ["Netflix", "streaming", "platform", "use"]),
    ("Is PlayReady open source?", ["open", "source", "proprietary", "Microsoft"]),
    ("What companies use PlayReady?", ["companies", "enterprise", "use", "adoption"]),
    
    # Technical (10 cases)
    ("How does PlayReady work?", ["encrypt", "decrypt", "protect", "technology"]),
    ("What encryption does PlayReady use?", ["encryption", "algorithm", "AES", "standard"]),
    ("How to implement PlayReady?", ["implement", "SDK", "API", "integration"]),
    ("What is PlayReady SDK?", ["SDK", "development", "kit", "tools"]),
    ("How to integrate PlayReady API?", ["integrate", "API", "connect", "endpoint"]),
    ("What programming languages support PlayReady?", ["language", "C#", "Java", "support"]),
    ("How to test PlayReady integration?", ["test", "debug", "verify", "integration"]),
    ("What are PlayReady error codes?", ["error", "code", "troubleshoot", "debug"]),
    ("How to debug PlayReady issues?", ["debug", "issue", "troubleshoot", "error"]),
    ("What is PlayReady certificate?", ["certificate", "public", "key", "security"]),
    
    # Licensing (10 cases)
    ("What are PlayReady licensing models?", ["license", "model", "option", "type"]),
    ("How does PlayReady licensing work?", ["license", "issue", "grant", "manage"]),
    ("What is PlayReady license server?", ["license", "server", "issue", "manage"]),
    ("How to setup PlayReady license server?", ["setup", "configure", "server", "license"]),
    ("How to issue PlayReady license?", ["issue", "grant", "license", "procedure"]),
    ("What is PlayReady license expiration?", ["expiration", "expire", "time", "period"]),
    ("Can PlayReady license be transferred?", ["transfer", "share", "move", "license"]),
    ("How to revoke PlayReady license?", ["revoke", "cancel", "remove", "license"]),
    ("What is subscription licensing?", ["subscription", "model", "recurring", "payment"]),
    ("How to manage multiple licenses?", ["manage", "multiple", "batch", "license"]),
    
    # Features (10 cases)
    ("What features does PlayReady have?", ["features", "capability", "support", "include"]),
    ("Does PlayReady support 4K?", ["4K", "resolution", "quality", "support"]),
    ("Does PlayReady support offline viewing?", ["offline", "download", "local", "view"]),
    ("What is persistent license?", ["persistent", "offline", "download", "cache"]),
    ("What is PlayReady Individualization?", ["individualization", "device", "unique", "identify"]),
    ("What is PlayReady Revocation?", ["revocation", "blacklist", "block", "prevent"]),
    ("Does PlayReady support multi-bitrate?", ["bitrate", "adaptive", "streaming", "quality"]),
    ("What is PlayReady Metering?", ["metering", "tracking", "usage", "monitor"]),
    ("Does PlayReady support DRM interoperability?", ["interop", "compatibility", "standard", "exchange"]),
    ("What is PlayReady output control?", ["output", "control", "display", "HDCP"]),
    
    # Compatibility (10 cases)
    ("What devices support PlayReady?", ["device", "support", "compatible", "platform"]),
    ("Does Windows support PlayReady?", ["Windows", "support", "OS", "platform"]),
    ("Does Xbox support PlayReady?", ["Xbox", "gaming", "console", "support"]),
    ("Does Android support PlayReady?", ["Android", "mobile", "device", "support"]),
    ("Does iOS support PlayReady?", ["iOS", "iPhone", "Apple", "support"]),
    ("Does Smart TV support PlayReady?", ["TV", "smart", "broadcast", "support"]),
    ("What browsers support PlayReady?", ["browser", "Chrome", "Firefox", "Edge"]),
    ("Does Roku support PlayReady?", ["Roku", "streaming", "device", "support"]),
    ("What about PlayReady on Linux?", ["Linux", "OS", "support", "compatible"]),
    ("What is PlayReady minimum requirement?", ["requirement", "minimum", "spec", "version"]),
    
    # Security (10 cases)
    ("How secure is PlayReady?", ["secure", "security", "protection", "level"]),
    ("What is PlayReady security level?", ["security", "level", "standard", "compliance"]),
    ("Is PlayReady resistant to hacking?", ["hack", "resist", "secure", "attack"]),
    ("How does PlayReady prevent piracy?", ["piracy", "prevent", "protect", "illegal"]),
    ("What encryption standard does PlayReady use?", ["standard", "encryption", "AES", "algorithm"]),
    ("Is PlayReady HDCP compatible?", ["HDCP", "display", "output", "protection"]),
    ("What is PlayReady compliance?", ["compliance", "standard", "certification", "requirement"]),
    ("Does PlayReady support DRM compliance?", ["compliance", "standard", "DRM", "requirement"]),
    ("How to verify PlayReady authenticity?", ["verify", "authentic", "genuine", "check"]),
    ("What are PlayReady security updates?", ["update", "security", "patch", "fix"]),
    
    # Streaming & Media (10 cases)
    ("Does PlayReady support live streaming?", ["live", "streaming", "broadcast", "support"]),
    ("Does PlayReady support VOD?", ["VOD", "on-demand", "streaming", "support"]),
    ("What video codecs does PlayReady support?", ["codec", "video", "format", "support"]),
    ("Does PlayReady support DASH?", ["DASH", "adaptive", "streaming", "protocol"]),
    ("Does PlayReady support HLS?", ["HLS", "streaming", "protocol", "support"]),
    ("What is PlayReady streaming requirements?", ["requirement", "streaming", "bandwidth", "spec"]),
    ("How to stream PlayReady protected content?", ["stream", "protected", "content", "procedure"]),
    ("What bitrates does PlayReady support?", ["bitrate", "quality", "resolution", "support"]),
    ("Does PlayReady support progressive download?", ["download", "progressive", "streaming", "support"]),
    ("What is PlayReady adaptive bitrate?", ["adaptive", "bitrate", "quality", "dynamic"]),
    
    # Business (10 cases)
    ("What is PlayReady business model?", ["business", "model", "licensing", "cost"]),
    ("How much does PlayReady cost?", ["cost", "price", "licensing", "fee"]),
    ("Is PlayReady suitable for startups?", ["startup", "cost", "suitable", "scale"]),
    ("What is PlayReady enterprise support?", ["enterprise", "support", "service", "SLA"]),
    ("How to get PlayReady support?", ["support", "help", "contact", "service"]),
    ("What is PlayReady training available?", ["training", "course", "learn", "education"]),
    ("Does PlayReady offer documentation?", ["documentation", "guide", "manual", "resource"]),
    ("What is PlayReady ROI?", ["ROI", "return", "investment", "benefit"]),
    ("How many customers use PlayReady?", ["customer", "adoption", "user", "market"]),
    ("What is PlayReady roadmap?", ["roadmap", "future", "plan", "feature"]),
]



def generate_test_cases(count=100):
    """Generate test cases"""
    test_cases = []
    
    for i, (question, keywords) in enumerate(PLAYREADY_QUESTIONS, 1):
        if i > count:
            break
        
        # Determine category
        if "license" in question.lower():
            category = "licensing"
        elif "implement" in question.lower() or "integrate" in question.lower():
            category = "implementation"
        elif "device" in question.lower() or "support" in question.lower():
            category = "compatibility"
        elif "secure" in question.lower() or "encrypt" in question.lower():
            category = "security"
        elif "stream" in question.lower():
            category = "streaming"
        elif "cost" in question.lower() or "business" in question.lower():
            category = "business"
        elif "feature" in question.lower():
            category = "features"
        else:
            category = "general"
        
        # Determine difficulty
        word_count = len(question.split())
        if word_count <= 4:
            difficulty = "easy"
        elif word_count <= 7:
            difficulty = "medium"
        else:
            difficulty = "hard"
        
        test_case = {
            "id": i,
            "query": question,
            "expected_keywords": keywords,
            "category": category,
            "difficulty": difficulty,
            "priority": "high" if i % 5 == 0 else "medium" if i % 3 == 0 else "low"
        }
        
        test_cases.append(test_case)
    
    # Generate remaining cases if needed
    while len(test_cases) < count:
        test_case = {
            "id": len(test_cases) + 1,
            "query": f"Custom test case {len(test_cases) + 1}",
            "expected_keywords": ["test", "case"],
            "category": "general",
            "difficulty": "medium",
            "priority": "low"
        }
        test_cases.append(test_case)
    
    return test_cases

def save_test_cases(test_cases, filename="data/raw/test_cases.json"):
    """Save test cases to JSON file"""
    data = {
        "test_suite": "PlayReady RAG QA Testing",
        "version": "1.0",
        "total_cases": len(test_cases),
        "test_cases": test_cases
    }
    
    Path("data").mkdir(exist_ok=True)
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Generated {len(test_cases)} test cases")
    print(f"📁 Saved to: {filename}")
    print(f"\n📊 Statistics:")
    
    # Count by category
    categories = {}
    for tc in test_cases:
        cat = tc.get("category", "general")
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\nBy Category:")
    for cat, count in sorted(categories.items()):
        print(f"  - {cat}: {count}")
    
    # Count by difficulty
    difficulties = {}
    for tc in test_cases:
        diff = tc.get("difficulty", "medium")
        difficulties[diff] = difficulties.get(diff, 0) + 1
    
    print(f"\nBy Difficulty:")
    for diff, count in sorted(difficulties.items()):
        print(f"  - {diff}: {count}")

if __name__ == "__main__":
    # Generate 100 test cases
    test_cases = generate_test_cases(100)
    save_test_cases(test_cases)