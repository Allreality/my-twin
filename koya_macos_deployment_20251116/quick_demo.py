#!/usr/bin/env python3
"""Quick demo for testing the system"""

def quick_test():
    print("🧪 Testing Koya Assessment System...")
    
    try:
        from compliance_assessment_agent import quick_assessment
        
        # Run quick test
        result = quick_assessment(
            institution_name="Demo Healthcare",
            institution_type="hospital",
            data_types=["clinical"]
        )
        
        print(f"✅ System test successful!")
        print(f"📄 Test report: {result}")
        
        # Test proposal generation
        from generate_proposal import ProposalGenerator
        generator = ProposalGenerator(result)
        proposal = generator.save_proposal("test_proposal.md")
        
        print(f"✅ Proposal generation successful!")
        print(f"📋 Test proposal: {proposal}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    quick_test()
