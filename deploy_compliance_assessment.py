#!/usr/bin/env python3
"""
Portable Compliance Assessment Deployment Script
Use this for on-site institution visits
"""

import sys
import os
import argparse
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    parser = argparse.ArgumentParser(description="Koya Compliance Assessment Tool")
    parser.add_argument('institution', help='Institution name')
    parser.add_argument('--type', choices=['hospital', 'research', 'pharmaceutical', 'university'], 
                       default='hospital', help='Institution type')
    parser.add_argument('--data-types', nargs='+', 
                       choices=['clinical', 'genomic', 'research', 'financial'],
                       default=['clinical'], help='Data types handled')
    parser.add_argument('--quick', action='store_true', help='Run quick assessment')
    
    args = parser.parse_args()
    
    print("🎯 KOYA COMPLIANCE ASSESSMENT TOOL")
    print("=" * 50)
    print(f"Institution: {args.institution}")
    print(f"Type: {args.type}")
    print(f"Data Types: {', '.join(args.data_types)}")
    print(f"Assessment Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    try:
        from compliance_assessment_agent import quick_assessment
        
        # Run the assessment
        report_file = quick_assessment(
            institution_name=args.institution,
            institution_type=args.type,
            data_types=args.data_types
        )
        
        print(f"\n✅ Assessment completed successfully!")
        print(f"📄 Report file: {report_file}")
        print("\n💼 Ready for compliance solution discussion!")
        
    except Exception as e:
        print(f"❌ Assessment failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
