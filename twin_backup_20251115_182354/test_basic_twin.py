#!/usr/bin/env python3
"""
Basic test script for the Digital Twin system
"""

import sys
import os

def test_basic_functionality():
    """Test basic digital twin functionality"""
    print("Testing Digital Twin System with Koya Initiative Integration")
    print("=" * 60)
    
    try:
        from complete_system import MyTwin
        
        # Initialize the twin
        twin = MyTwin()
        print(f"✓ Digital Twin initialized: {twin.name}")
        
        # Test status
        status = twin.get_status()
        print(f"✓ Status check passed: {status['status']}")
        print(f"  Primary Focus: {status['primary_focus']}")
        
        return twin
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return None
    except Exception as e:
        print(f"✗ Initialization error: {e}")
        return None

def test_koya_queries(twin):
    """Test Koya initiative queries"""
    if not twin:
        return
    
    print("\nTesting Koya Initiative Queries")
    print("=" * 40)
    
    queries = [
        "Tell me about the Koya initiative",
        "What compliance frameworks do you support?",
        "What grants are you pursuing?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. Query: {query}")
        print("-" * 50)
        try:
            response = twin.chat(query)
            print(response)
            print("✓ Query successful")
        except Exception as e:
            print(f"✗ Query failed: {e}")

def main():
    """Main test function"""
    print("Digital Twin System Test Suite")
    print("Starting tests...\n")
    
    # Test basic functionality
    twin = test_basic_functionality()
    
    # Test Koya queries
    test_koya_queries(twin)
    
    print("\n" + "=" * 60)
    print("Test suite completed!")
    
    if twin:
        print("\n🎉 Digital Twin system is ready!")
        print("You can now query about the Koya initiative!")
    else:
        print("\n❌ Digital Twin system has issues")

if __name__ == "__main__":
    main()
