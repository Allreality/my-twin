#!/usr/bin/env python3
"""Test basic Claude API connectivity"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('CLAUDE_API_KEY')

if not api_key or api_key == 'your_api_key_here':
    print("❌ Error: CLAUDE_API_KEY not set in .env file")
    print("Please edit .env and add your API key")
    exit(1)

print("🧪 Testing Claude API connection...\n")

try:
    # Initialize Claude client
    client = Anthropic(api_key=api_key)
    
    # Send test message
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        messages=[
            {"role": "user", "content": "Say hello and introduce yourself as a digital twin prototype!"}
        ]
    )
    
    # Display response
    print("✅ Claude API Connection Successful!\n")
    print("Claude's Response:")
    print("-" * 60)
    print(message.content[0].text)
    print("-" * 60)
    print("\n🎉 Your digital twin foundation is ready!")
    
except Exception as e:
    print(f"❌ Error connecting to Claude API: {e}")
    print("\nTroubleshooting:")
    print("1. Check your API key in .env")
    print("2. Verify you have API credits: https://console.anthropic.com/")
    print("3. Check your internet connection")

