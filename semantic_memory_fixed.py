import chromadb
from datetime import datetime
import os

# Use persistent storage
MEMORY_DIR = "/mnt/c/projects/twin/memory_db"
os.makedirs(MEMORY_DIR, exist_ok=True)

client = chromadb.PersistentClient(path=MEMORY_DIR)

# Get or create collection
try:
    collection = client.get_collection(name="twin_memories")
    print(f"✅ Loaded existing collection with {collection.count()} memories")
except:
    collection = client.create_collection(
        name="twin_memories",
        metadata={"description": "Digital twin's episodic and semantic memories"}
    )
    print("✅ Created new persistent collection")

class SemanticMemory:
    """Manages long-term semantic memory with persistence"""

    def store_memory(self, content, memory_type, emotional_valence, importance):
        """Store a memory with semantic embedding"""
        memory_id = f"mem_{datetime.now().timestamp()}"

        collection.add(
            documents=[content],
            metadatas=[{
                'type': memory_type,
                'emotional_valence': emotional_valence,
                'importance': importance,
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
            if memory_type and metadata['type'] != memory_type:
                continue
            memories.append({
                'content': doc,
                'metadata': metadata
            })
        return memories

    def clear_all_memories(self):
        """Clear all memories (use with caution!)"""
        client.delete_collection("twin_memories")
        return True

semantic_memory = SemanticMemory()
