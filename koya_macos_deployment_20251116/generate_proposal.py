#!/usr/bin/env python3
"""
Proposal Generator from Compliance Assessment Results
Creates custom proposals based on institution assessment data
"""

import json
import sys
import os
from datetime import datetime
from typing import Dict, Any

class ProposalGenerator:
    def __init__(self, assessment_file: str):
        self.assessment_file = assessment_file
        self.assessment_data = self._load_assessment()
        
    def _load_assessment(self) -> Dict[str, Any]:
        """Load assessment results from JSON file"""
        try:
            with open(self.assessment_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading assessment: {e}")
            return {}
    
    def generate_executive_proposal(self) -> str:
        """Generate executive proposal document"""
        if not self.assessment_data:
            return "❌ No assessment data available"
        
        institution = self.assessment_data.get('institution_profile', {})
        executive_summary = self.assessment_data.get('executive_summary', {})
        findings = self.assessment_data.get('detailed_findings', [])
        
        proposal = f"""
# KOYA COMPLIANCE SOLUTION PROPOSAL
## {institution.get('name', 'Institution')}

**Prepared by:** Total Reality Global  
**Date:** {datetime.now().strftime('%B %d, %Y')}  
**Assessment Reference:** {self.assessment_file}

---

## EXECUTIVE SUMMARY

### Current Compliance Posture
- **Institution Type:** {institution.get('type', '').title()}
- **Data Types:** {', '.join(institution.get('data_types', []))}
- **Overall Compliance Score:** {executive_summary.get('overall_compliance_score', 'N/A')}
- **Critical Gaps:** {executive_summary.get('critical_gaps', 0)} out of {executive_summary.get('total_controls_assessed', 0)} controls

### Business Risk Assessment
- **Compliance Status:** {executive_summary.get('compliance_status', 'Unknown')}
- **Regulatory Risk:** High - Multiple NIST SP 800-171 violations
- **Data Breach Risk:** Elevated due to insufficient access controls
- **Financial Impact:** Potential penalties and audit costs

---

## KOYA SOLUTION OVERVIEW

### Hardware-Enforced Compliance Architecture
The Koya initiative delivers comprehensive NIST SP 800-171 compliance through:

**Core Technology Stack:**
- AMD EPYC processors with SEV-SNP memory encryption
- Midnight blockchain technology for verification
- Zero-knowledge proofs for compliance attestation
- Real-time continuous monitoring

### Specific Gap Resolution
"""
        
        # Add specific gap resolutions
        critical_gaps = [f for f in findings if f.get('risk_level') == 'critical' and f.get('status') == 'non_compliant']
        
        for gap in critical_gaps:
            proposal += f"""
**{gap.get('control_id')} - {gap.get('title')}**
- Current Status: {gap.get('status').replace('_', ' ').title()}
- Koya Solution: {gap.get('koya_solution')}
"""
        
        proposal += f"""

---

## IMPLEMENTATION ROADMAP

### Phase 1: Pilot Deployment (30 days)
1. Install Koya compliance infrastructure
2. Configure AMD EPYC security features
3. Integrate with existing systems
4. Initial compliance verification

### Phase 2: Full Deployment (60 days)
1. Scale across all critical systems
2. Implement continuous monitoring
3. Staff training and certification
4. Compliance documentation

### Phase 3: Optimization (90 days)
1. Performance tuning
2. Advanced threat detection
3. Regulatory reporting automation
4. ROI measurement

---

## BUSINESS VALUE PROPOSITION

### Cost-Benefit Analysis
- **Current Compliance Costs:** Estimated $500K annually
- **Koya Solution Cost:** $200K implementation + $100K annually
- **Net Savings:** $200K annually (60% reduction)
- **ROI:** 200% within first year

### Risk Mitigation
- **Regulatory Penalties:** Avoided potential $1M+ in fines
- **Data Breach Prevention:** $4M average breach cost mitigation
- **Audit Efficiency:** 75% reduction in audit preparation time

---

## NEXT STEPS

### Immediate Actions
1. **Technical Deep Dive:** Detailed system architecture review
2. **Pilot Agreement:** 90-day proof-of-concept deployment
3. **Stakeholder Alignment:** CIO, CISO, and Compliance Officer buy-in
4. **Timeline Establishment:** Project milestones and deliverables

### Pilot Program Terms
- **Duration:** 90 days
- **Scope:** Critical patient data systems
- **Success Metrics:** Achieve 95% NIST SP 800-171 compliance
- **Investment:** $50K pilot cost (credited toward full deployment)

---

**Contact Information:**
Akil (Pa Santige Koroma)  
Systems Analyst, Total Reality Global  
GitHub: Allreality  
Email: [Your Email]  
Phone: [Your Phone]

*This proposal is valid for 30 days from the date of assessment.*
"""
        
        return proposal
    
    def save_proposal(self, filename: str = None) -> str:
        """Save proposal to markdown file"""
        if not filename:
            institution_name = self.assessment_data.get('institution_profile', {}).get('name', 'Institution')
            safe_name = institution_name.replace(' ', '_').replace('/', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"proposal_{safe_name}_{timestamp}.md"
        
        proposal_content = self.generate_executive_proposal()
        
        with open(filename, 'w') as f:
            f.write(proposal_content)
        
        print(f"📄 Proposal saved: {filename}")
        return filename

def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_proposal.py <assessment_file.json>")
        print("\nAvailable assessment files:")
        for file in os.listdir('.'):
            if file.startswith('compliance_assessment_') and file.endswith('.json'):
                print(f"  {file}")
        return
    
    assessment_file = sys.argv[1]
    
    if not os.path.exists(assessment_file):
        print(f"❌ Assessment file not found: {assessment_file}")
        return
    
    print(f"📋 Generating proposal from: {assessment_file}")
    
    generator = ProposalGenerator(assessment_file)
    proposal_file = generator.save_proposal()
    
    print(f"✅ Custom proposal generated: {proposal_file}")
    print(f"💼 Ready for client presentation!")

if __name__ == "__main__":
    main()
