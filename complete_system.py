# FILE: complete_system.py

def process_interaction(user_input, session_id):
    """Complete interaction processing"""
    
    # 1. Get personality prompt
    personality = get_personality_prompt()
    
    # 2. Get emotional context
    emotional_context = emotion.get_context()
    
    # 3. Get recent conversation
    recent_conversation = memory.get_conversation_summary(session_id)
    
    # 4. Search for relevant memories
    memory_context = semantic_memory.get_memory_context(user_input)
    
    # 5. Assemble complete context
    full_context = f"""{personality}

{emotional_context}

{memory_context}

{recent_conversation}

Current user input: {user_input}
"""
    
    # 6. Call Claude with full context
    response = call_claude(full_context)
    
    # 7. Store this interaction
    memory.store_conversation_turn(session_id, user_input, response)
    
    # 8. Create memory if important
    if is_important(user_input, response):
        semantic_memory.store_memory(
            content=f"User: {user_input}\nTwin: {response}",
            memory_type="episodic",
            emotional_valence=extract_sentiment(user_input),
            importance=0.7
        )
    
    # 9. Update emotional state
    emotion.update(
        event_sentiment=extract_sentiment(user_input),
        trigger=f"conversation about {extract_topic(user_input)}"
    )
    
    return response