# Koya Compliance Assessment Tool
## Portable On-Site NIST SP 800-171 Assessment

### Quick Start
```bash
# Basic assessment
python deploy_compliance_assessment.py "Institution Name" --type hospital

# Research institution with multiple data types  
python deploy_compliance_assessment.py "Research Center" --type research --data-types clinical genomic research

# Quick assessment mode
python deploy_compliance_assessment.py "Hospital System" --quick
```

### What This Does
1. **Network Assessment** - Discovers basic system topology and security posture
2. **NIST SP 800-171 Evaluation** - Assesses compliance against 8 critical controls
3. **Gap Analysis** - Identifies specific non-compliance areas
4. **Koya Solution Mapping** - Shows how Koya addresses each gap
5. **Executive Report** - Generates business-ready compliance report

### Output
- Real-time compliance score
- Critical gap identification  
- Risk analysis and business impact
- Koya solution value proposition
- Detailed JSON report file

### Business Value
- Immediate compliance assessment (30 minutes)
- Professional compliance reports
- Clear demonstration of Koya solution value
- Foundation for solution sales discussion

### Requirements
- Python 3.6+
- Network access to target systems
- Admin/assessment permissions at institution
