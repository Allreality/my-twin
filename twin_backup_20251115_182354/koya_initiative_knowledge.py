"""
Koya Initiative Knowledge Base
"""

KOYA_INITIATIVE_KNOWLEDGE = {
    "overview": {
        "name": "Koya Initiative", 
        "description": "A comprehensive hardware-enforced compliance architecture combining AMD EPYC processors with SEV-SNP memory encryption, Midnight blockchain technology, and zero-knowledge proofs for NIST SP 800-171 compliance verification",
        "purpose": "Positioning as a ransomware prevention solution for healthcare and research institutions",
        "target_market": "Healthcare and research institutions requiring NIST SP 800-171 compliance",
        "compliance_focus": "NIST SP 800-171 compliance for controlled-access genomic data"
    },
    
    "technical_architecture": {
        "core_components": [
            "AMD EPYC processors with SEV-SNP memory encryption",
            "Midnight blockchain technology", 
            "Zero-knowledge proofs for compliance verification",
            "Hardware-enforced compliance architecture"
        ],
        "security_features": [
            "Memory encryption at hardware level",
            "Secure multi-institutional data collaboration",
            "Privacy-preserving compliance verification", 
            "Ransomware prevention through hardware isolation"
        ]
    },
    
    "business_strategy": {
        "grant_opportunities": [{
            "program": "NIH SBIR",
            "deadline": "January 2025 mandate", 
            "requirement": "NIST SP 800-171 compliance for controlled-access genomic data",
            "opportunity": "Federal funding for compliance solutions"
        }],
        "90_day_plan": [
            "Secure pilot customers",
            "Prepare grant applications",
            "Document cybersecurity innovation cost savings", 
            "Develop compliance proof demonstrations"
        ]
    },
    
    "regulatory_compliance": {
        "frameworks": ["NIST SP 800-171", "HIPAA compliance", "SOC 2 requirements"],
        "verification_methods": ["Zero-knowledge proofs", "Cryptographic attestation", "Blockchain audit trails"]
    }
}

def get_koya_info(query_type="overview"):
    return KOYA_INITIATIVE_KNOWLEDGE.get(query_type, KOYA_INITIATIVE_KNOWLEDGE)

def search_koya_knowledge(search_term):
    results = []
    search_term_lower = search_term.lower()
    
    def search_recursive(data, path=""):
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key
                if search_term_lower in key.lower():
                    results.append({"path": current_path, "content": value})
                search_recursive(value, current_path)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                search_recursive(item, f"{path}[{i}]")
        elif isinstance(data, str):
            if search_term_lower in data.lower():
                results.append({"path": path, "content": data})
    
    search_recursive(KOYA_INITIATIVE_KNOWLEDGE)
    return results
