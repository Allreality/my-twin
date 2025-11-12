# FILE: working_memory.py

import redis
import json
from datetime import datetime

redis_client = redis.Redis(host='localhost', port=6379, db=0)

class WorkingMemory:
    """Manages short-term conversation context"""
    
    def store_conversation_turn(self, session_id, user_input, assistant_response):
        """Store a conversation turn"""
        key = f"conversation:{session_id}"
        
        turn = {
            'timestamp': datetime.now().isoformat(),
            'user': user_input,
            'assistant': assistant_response
        }
        
        # Append to conversation history
        redis_client.rpush(key, json.dumps(turn))
        
        # Keep last 50 turns only
        redis_client.ltrim(key, -50, -1)
        
        # Set expiry: 24 hours
        redis_client.expire(key, 86400)
    
    def get_recent_conversation(self, session_id, last_n=10):
        """Get recent conversation history"""
        key = f"conversation:{session_id}"
        turns = redis_client.lrange(key, -last_n, -1)
        return [json.loads(t) for t in turns]
    
    def get_conversation_summary(self, session_id):
        """Get summary of current conversation"""
        recent = self.get_recent_conversation(session_id, 5)
        
        summary = "Recent conversation:\n"
        for turn in recent:
            summary += f"User: {turn['user'][:50]}...\n"
            summary += f"You: {turn['assistant'][:50]}...\n\n"
        
        return summary

# Usage:
memory = WorkingMemory()

# After each interaction:
memory.store_conversation_turn(
    session_id="user123",
    user_input="How are you?",
    assistant_response="I'm doing well, thanks!"
)

# When building context:
recent_context = memory.get_conversation_summary("user123")