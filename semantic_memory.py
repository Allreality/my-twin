# FILE: semantic_memory.py

import chromadb
from datetime import datetime

client = chromadb.Client()
collection = client.create_collection(
    name="twin_memories",
    metadata={"description": "Digital twin's episodic and semantic memories"}
)

class SemanticMemory:
    """Manages long-term semantic memory"""
    
    def store_memory(self, content, memory_type, emotional_valence, importance):
        """Store a memory with semantic embedding"""
        memory_id = f"mem_{datetime.now().timestamp()}"
        
        collection.add(
            documents=[content],
            metadatas=[{
                'type': memory_type,  # 'episodic' or 'semantic'
                'emotional_valence': emotional_valence,  # -1 to 1
                'importance': importance,  # 0 to 1
                'timestamp': datetime.now().isoformat()
            }],
            ids=[memory_id]
        )
        
        return memory_id
    
    def search_memories(self, query, memory_type=None, limit=5):
        """Search for relevant memories"""
        results = collection.query(
            query_texts=[query],
            n_results=limit
        )
        
        memories = []
        for i, doc in enumerate(results['documents'][0]):
            metadata = results['metadatas'][0][i]
            
            # Filter by type if specified
            if memory_type and metadata['type'] != memory_type:
                continue
            
            memories.append({
                'content': doc,
                'metadata': metadata
            })
        
        return memories
    
    def get_memory_context(self, query):
        """Get formatted memory context for Claude"""
        memories = self.search_memories(query, limit=5)
        
        if not memories:
            return "No relevant memories found."
        
        context = "Relevant memories:\n\n"
        for mem in memories:
            context += f"• {mem['content']}\n"
            context += f"  (From: {mem['metadata']['timestamp'][:10]})\n\n"
        
        return context

# Usage:
semantic_memory = SemanticMemory()

# Store a memory:
semantic_memory.store_memory(
    content="User mentioned they're a software engineer at Google, working on AI projects",
    memory_type="semantic",
    emotional_valence=0.0,
    importance=0.8
)

# Later, retrieve:
memories = semantic_memory.search_memories("what does the user do for work?")
# ✅ Finds the Google/AI memory even though words don't exactly match!