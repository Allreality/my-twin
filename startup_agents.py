#!/usr/bin/env python3
"""
Total Reality Ecosystem - Agent System Startup
"""

import sys
import os
import time
import signal
from tan_agent_system_integration import update_agent_memory, update_personality_context
agent_memory.update(update_agent_memory())
personality_context.update(update_personality_context())
from tan_knowledge_base_update import get_tan_knowledge
knowledge_base.update(get_tan_knowledge())

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def signal_handler(signum, frame):
    print("\n🛑 Shutting down Agent System...")
    sys.exit(0)

def check_prerequisites():
    print("🔍 Checking prerequisites...")
    
    # Check digital twin
    try:
        from complete_system import MyTwin
        twin = MyTwin()
        response = twin.chat('Tell me about the Koya initiative')
        print("✅ Digital twin system available")
        return True
    except Exception as e:
        print(f"❌ Digital twin error: {e}")
        return False

def start_system():
    print("🚀 Starting Total Reality Agent Coordination System...")
    
    try:
        from service_integration import AgentServiceIntegration
        
        # Register signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Start service
        service = AgentServiceIntegration(port=5006)
        service.start()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Creating basic coordinator...")
        
        from agent_coordinator import AgentCoordinator
        coordinator = AgentCoordinator()
        coordinator.start()
        
        print(f"✅ Basic coordinator running on port {coordinator.port}")
        print("\n🎯 Basic Koya Strategy Test:")
        strategy_id = coordinator.execute_koya_strategy()
        print(f"Strategy ID: {strategy_id}")
        
        print("\nPress Ctrl+C to stop...")
        while True:
            time.sleep(1)
    
    except Exception as e:
        print(f"❌ System error: {e}")

def main():
    if not check_prerequisites():
        print("❌ Prerequisites not met. Please check your digital twin setup.")
        return
    
    start_system()

if __name__ == "__main__":
    main()
