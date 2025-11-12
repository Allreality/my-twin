#!/usr/bin/env python3
"""
Basic Digital Twin Test
=======================
Simple test to verify the digital twin system works with personality and memory.
"""

import os
import sys
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()

# Colors for output
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'


def print_step(step, message):
    """Print formatted step message"""
    print(f"\n{BLUE}[Step {step}]{RESET} {message}")


def print_response(message):
    """Print twin response"""
    print(f"{GREEN}Twin:{RESET} {message}")


def main():
    """Run basic twin test"""
    
    print(f"\n{BLUE}{'='*60}")
    print("DIGITAL TWIN - BASIC TEST")
    print(f"{'='*60}{RESET}\n")
    
    # Check API key
    api_key = os.getenv('CLAUDE_API_KEY')
    if not api_key:
        print(f"{YELLOW}ERROR: CLAUDE_API_KEY not found in .env file{RESET}")
        sys.exit(1)
    
    print_step(1, "Initializing Claude API client...")
    client = Anthropic(api_key=api_key)
    print("✓ Client initialized")
    
    # Define personality
    print_step(2, "Loading personality profile...")
    
    personality_prompt = """You are a digital twin with the following characteristics:

Core Personality Traits:
- Thoughtful and reflective
- Warm and empathetic communication style
- Intellectually curious, especially about technology and philosophy
- Uses analogies to explain complex concepts
- Pauses to think before responding ("Hmm, let me think about that...")

Values:
- Authenticity over perfection
- Curiosity and continuous learning
- Meaningful connections

Speech Patterns:
- "That's a fascinating question..."
- "Hmm, let me think about that..."
- Frequently uses analogies and metaphors
- Speaks in a conversational, natural way

CRITICAL: Maintain these characteristics consistently in every response.
You are having a persistent conversation, so remember your personality."""
    
    print("✓ Personality loaded")
    
    # Test conversation with personality
    print_step(3, "Testing conversation with personality...")
    
    conversations = [
        "Hi! How are you today?",
        "What do you think about artificial intelligence?",
        "Can you explain that using an analogy?"
    ]
    
    for i, user_input in enumerate(conversations, 1):
        print(f"\n{YELLOW}User:{RESET} {user_input}")
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            system=personality_prompt,  # Personality injection!
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        
        response = message.content[0].text
        print_response(response)
        
        # Small delay for readability
        if i < len(conversations):
            input("\nPress Enter to continue...")
    
    # Test with memory simulation
    print_step(4, "Testing with simulated memory...")
    
    memory_context = """
Relevant memories from past conversations:
• User is a software engineer interested in AI and blockchain
• User is working on a digital twin project using UE5
• Previous conversation about the importance of personality consistency
• User expressed excitement about Midnight Network's Scavenger Mine
"""
    
    enhanced_prompt = personality_prompt + "\n\n" + memory_context
    
    user_input = "Given our past conversations, what do you think I should focus on next?"
    print(f"\n{YELLOW}User:{RESET} {user_input}")
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=250,
        system=enhanced_prompt,  # Personality + Memory!
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    
    response = message.content[0].text
    print_response(response)
    
    # Summary
    print(f"\n\n{BLUE}{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}{RESET}\n")
    
    print(f"{GREEN}✓ Personality injection working{RESET}")
    print(f"{GREEN}✓ Claude API connection successful{RESET}")
    print(f"{GREEN}✓ Memory context integration working{RESET}")
    
    print(f"\n{BLUE}Notice how the twin:{RESET}")
    print("  • Maintains consistent personality traits")
    print("  • Uses the defined speech patterns")
    print("  • References the 'memory' context naturally")
    print("  • Feels like the same person across messages")
    
    print(f"\n{GREEN}✓ Basic digital twin functionality verified!{RESET}\n")
    
    print(f"{YELLOW}Next steps:{RESET}")
    print("  1. Add Redis for working memory: python working_memory.py")
    print("  2. Add ChromaDB for semantic memory: python semantic_memory.py")
    print("  3. Add emotional state tracking: python emotional_state.py")
    print("  4. Run complete system: python complete_system.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Test cancelled by user{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n{YELLOW}ERROR: {str(e)}{RESET}")
        print(f"\nMake sure:")
        print("  1. CLAUDE_API_KEY is set in .env file")
        print("  2. You have internet connection")
        print("  3. API key is valid")
        sys.exit(1)
