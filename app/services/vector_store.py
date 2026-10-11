import os
import chromadb
from chromadb.config import Settings as ChromaSettings
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class VectorStore:
    def __init__(self):
        os.makedirs(settings.CHROMA_DB_PATH, exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_PATH,
            settings=ChromaSettings(allow_reset=True)
        )
        self.collection = self.client.get_or_create_collection(
            name="academic_memories",
            metadata={"hnsw:space": "cosine"}
        )

    def upsert_memory(self, memory_id: str, text: str, user_id: str, memory_type: str, metadata: dict):
        # Chroma expects metadata values to be primitive types
        safe_metadata = {
            "user_id": user_id,
            "memory_type": memory_type,
        }
        # Merge additional metadata, ensure serializable
        for k, v in metadata.items():
            if isinstance(v, (str, int, float, bool)) or v is None:
                safe_metadata[k] = v
            else:
                safe_metadata[k] = str(v)
        
        self.collection.upsert(
            ids=[memory_id],
            documents=[text],
            metadatas=[safe_metadata]
        )

    def search(self, query_text: str, user_id: str, top_k: int = 5):
        results = self.collection.query(
            query_texts=[query_text],
            where={"user_id": user_id},
            n_results=top_k
        )
        return results

    def count(self, user_id: str | None = None):
        # Chroma doesn't support direct count with filter easily, return total
        return self.collection.count()
