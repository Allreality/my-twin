#!/usr/bin/env python3
"""
Digital Twin System - Setup Verification & Testing
==================================================
This script verifies all components are properly installed and configured.
Run this FIRST to ensure everything is ready.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_status(message, status="info"):
    """Print colored status message"""
    colors = {
        "success": GREEN,
        "error": RED,
        "warning": YELLOW,
        "info": BLUE
    }
    color = colors.get(status, RESET)
    symbol = {
        "success": "✓",
        "error": "✗",
        "warning": "⚠",
        "info": "ℹ"
    }.get(status, "•")
    
    print(f"{color}{symbol} {message}{RESET}")


def check_python_version():
    """Check Python version"""
    print("\n" + "="*60)
    print("CHECKING PYTHON VERSION")
    print("="*60)
    
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} - OK", "success")
        return True
    else:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} - Need 3.8+", "error")
        return False


def check_env_file():
    """Check .env file exists and has required variables"""
    print("\n" + "="*60)
    print("CHECKING ENVIRONMENT VARIABLES")
    print("="*60)
    
    if not Path('.env').exists():
        print_status(".env file not found", "error")
        print_status("Create .env file with: CLAUDE_API_KEY=your_key_here", "info")
        return False
    
    load_dotenv()
    api_key = os.getenv('CLAUDE_API_KEY')
    
    if not api_key:
        print_status(".env file exists but CLAUDE_API_KEY not set", "error")
        return False
    
    if api_key.startswith('sk-ant-'):
        print_status(f"CLAUDE_API_KEY found (starts with: {api_key[:15]}...)", "success")
        return True
    else:
        print_status("CLAUDE_API_KEY doesn't look valid (should start with 'sk-ant-')", "warning")
        return False


def check_required_packages():
    """Check if required packages are installed"""
    print("\n" + "="*60)
    print("CHECKING REQUIRED PACKAGES")
    print("="*60)
    
    required = [
        ('anthropic', 'Claude API'),
        ('redis', 'Working Memory'),
        ('chromadb', 'Semantic Memory'),
        ('influxdb_client', 'Time-Series Memory'),
        ('dotenv', 'Environment Variables'),
    ]
    
    all_installed = True
    
    for package, description in required:
        try:
            __import__(package)
            print_status(f"{package:20} - {description} - Installed", "success")
        except ImportError:
            print_status(f"{package:20} - {description} - MISSING", "error")
            all_installed = False
    
    if not all_installed:
        print_status("\nInstall missing packages with:", "info")
        print(f"  pip install -r requirements.txt --break-system-packages")
    
    return all_installed


def check_redis_connection():
    """Check if Redis is accessible"""
    print("\n" + "="*60)
    print("CHECKING REDIS CONNECTION")
    print("="*60)
    
    try:
        import redis
        
        # Try to connect
        r = redis.Redis(host='localhost', port=6379, db=0, socket_timeout=2)
        r.ping()
        
        print_status("Redis server is running and accessible", "success")
        
        # Test basic operations
        r.set('test_key', 'test_value')
        value = r.get('test_key')
        r.delete('test_key')
        
        print_status("Redis read/write operations working", "success")
        return True
        
    except Exception as e:
        print_status(f"Redis connection failed: {str(e)}", "error")
        print_status("Redis is optional but recommended for working memory", "warning")
        print_status("Install Redis: https://redis.io/download", "info")
        return False


def check_chromadb():
    """Check if ChromaDB is working"""
    print("\n" + "="*60)
    print("CHECKING CHROMADB (Semantic Memory)")
    print("="*60)
    
    try:
        import chromadb
        
        # Create a test client
        client = chromadb.Client()
        
        # Test collection creation
        collection = client.create_collection(
            name="test_collection",
            metadata={"test": "true"}
        )
        
        # Test document storage
        collection.add(
            documents=["This is a test document"],
            ids=["test_id"]
        )
        
        # Test query
        results = collection.query(
            query_texts=["test"],
            n_results=1
        )
        
        # Cleanup
        client.delete_collection("test_collection")
        
        print_status("ChromaDB is working correctly", "success")
        return True
        
    except Exception as e:
        print_status(f"ChromaDB test failed: {str(e)}", "error")
        return False


def test_claude_api():
    """Test Claude API connection"""
    print("\n" + "="*60)
    print("TESTING CLAUDE API CONNECTION")
    print("="*60)
    
    try:
        from anthropic import Anthropic
        
        load_dotenv()
        api_key = os.getenv('CLAUDE_API_KEY')
        
        if not api_key:
            print_status("No API key found", "error")
            return False
        
        client = Anthropic(api_key=api_key)
        
        print_status("Sending test message to Claude...", "info")
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=50,
            messages=[
                {"role": "user", "content": "Say 'API connection successful' and nothing else."}
            ]
        )
        
        response = message.content[0].text
        print_status(f"Claude responded: {response}", "success")
        
        return True
        
    except Exception as e:
        print_status(f"Claude API test failed: {str(e)}", "error")
        print_status("Check your API key in .env file", "info")
        return False


def check_project_files():
    """Check if required project files exist"""
    print("\n" + "="*60)
    print("CHECKING PROJECT FILES")
    print("="*60)
    
    required_files = [
        ('personality.py', 'Personality Core Agent'),
        ('working_memory.py', 'Working Memory Agent'),
        ('semantic_memory.py', 'Semantic Memory Agent'),
        ('emotional_state.py', 'Emotional State Agent'),
        ('complete_system.py', 'Complete System Integration'),
    ]
    
    all_exist = True
    
    for filename, description in required_files:
        if Path(filename).exists():
            print_status(f"{filename:25} - {description} - Found", "success")
        else:
            print_status(f"{filename:25} - {description} - MISSING", "error")
            all_exist = False
    
    return all_exist


def run_all_checks():
    """Run all verification checks"""
    print(f"\n{BLUE}{'='*60}")
    print("DIGITAL TWIN SYSTEM - SETUP VERIFICATION")
    print(f"{'='*60}{RESET}\n")
    
    results = {
        "Python Version": check_python_version(),
        "Environment Variables": check_env_file(),
        "Required Packages": check_required_packages(),
        "Redis Connection": check_redis_connection(),
        "ChromaDB": check_chromadb(),
        "Claude API": test_claude_api(),
        "Project Files": check_project_files(),
    }
    
    # Summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60 + "\n")
    
    passed = sum(results.values())
    total = len(results)
    
    for check, status in results.items():
        print_status(f"{check:30} {'PASS' if status else 'FAIL'}", 
                    "success" if status else "error")
    
    print(f"\n{BLUE}Results: {passed}/{total} checks passed{RESET}\n")
    
    if passed == total:
        print_status("🎉 ALL CHECKS PASSED! System is ready to use.", "success")
        print_status("\nNext steps:", "info")
        print("  1. Run: python test_basic_twin.py")
        print("  2. Or: python complete_system.py")
    else:
        print_status("⚠️  Some checks failed. Fix issues above before proceeding.", "warning")
        
        if not results["Required Packages"]:
            print_status("\nTo install packages:", "info")
            print("  pip install -r requirements.txt --break-system-packages")
        
        if not results["Redis Connection"]:
            print_status("\nRedis is optional for now. You can continue without it.", "info")
    
    return passed == total


if __name__ == "__main__":
    try:
        success = run_all_checks()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print_status("\n\nVerification cancelled by user", "warning")
        sys.exit(1)
    except Exception as e:
        print_status(f"\n\nUnexpected error: {str(e)}", "error")
        sys.exit(1)
