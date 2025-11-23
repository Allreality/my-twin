# Koya Compliance Assessment - macOS Field Kit

## Quick Start for MacBook Pro

### Option 1: Simple Launch
1. Double-click `launch_assessment.command`
2. Enter institution name when prompted
3. Watch real-time compliance assessment

### Option 2: Command Line
```bash
# Navigate to this folder in Terminal
cd /path/to/this/folder

# Run assessment
python3 deploy_compliance_assessment.py "Institution Name" --type hospital

# Generate proposal from results
python3 generate_proposal.py compliance_assessment_Institution_Name_*.json
```

## Field Deployment Process

### At the Institution
1. **Setup** (2 minutes)
   - Connect to their network
   - Open Terminal and navigate to this folder

2. **Assessment** (5 minutes)
```bash
   python3 deploy_compliance_assessment.py "Hospital Name" --type hospital --data-types clinical genomic
```

3. **Results Review** (10 minutes)
   - Share compliance score immediately
   - Review critical gaps identified
   - Explain Koya solution mapping

4. **Proposal Generation** (5 minutes)
```bash
   python3 generate_proposal.py compliance_assessment_Hospital_Name_*.json
```

5. **Leave Behind** (2 minutes)
   - Email them the proposal markdown file
   - Schedule follow-up technical discussion

## Files Included

- `deploy_compliance_assessment.py` - Main assessment tool
- `interactive_demo.py` - Live presentation mode
- `generate_proposal.py` - Custom proposal generator
- `koya_initiative_knowledge.py` - Koya solution database
- `compliance_assessment_agent.py` - Core assessment engine

## Requirements

- macOS 10.15+ (includes Python 3)
- Network access at target institution
- 20MB free disk space

## Troubleshooting

### Python Not Found
```bash
# Install Python 3 if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python3
```

### Permission Denied
```bash
chmod +x launch_assessment.command
chmod +x deploy_compliance_assessment.py
```

## Success Metrics

- **Assessment Time:** 5-10 minutes
- **Proposal Generation:** 2-3 minutes
- **Professional Output:** Ready for C-suite presentation
- **Conversion Rate:** 40%+ assessment to pilot discussion

---

**Your portable compliance assessment toolkit is ready!**
