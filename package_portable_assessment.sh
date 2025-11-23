#!/bin/bash

# Create portable compliance assessment package
PACKAGE_NAME="koya_compliance_assessment_$(date +%Y%m%d)"

echo "📦 Creating portable assessment package: $PACKAGE_NAME"

mkdir -p "$PACKAGE_NAME"

# Copy essential files
cp koya_initiative_knowledge.py "$PACKAGE_NAME/"
cp compliance_assessment_agent.py "$PACKAGE_NAME/"
cp deploy_compliance_assessment.py "$PACKAGE_NAME/"

# Create portable README
cat > "$PACKAGE_NAME/README.md" << 'PACKAGE_EOF'
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
PACKAGE_EOF

# Create requirements file
echo "# No external dependencies required - uses Python standard library" > "$PACKAGE_NAME/requirements.txt"

# Create compressed package
tar -czf "${PACKAGE_NAME}.tar.gz" "$PACKAGE_NAME"

echo "✅ Portable package created: ${PACKAGE_NAME}.tar.gz"
echo "📋 Package contents:"
ls -la "$PACKAGE_NAME/"

echo ""
echo "🎯 DEPLOYMENT INSTRUCTIONS:"
echo "1. Copy ${PACKAGE_NAME}.tar.gz to target system"
echo "2. Extract: tar -xzf ${PACKAGE_NAME}.tar.gz"
echo "3. Run: cd ${PACKAGE_NAME} && python deploy_compliance_assessment.py 'Institution Name'"
echo ""
echo "💼 Perfect for on-site compliance demonstrations!"
