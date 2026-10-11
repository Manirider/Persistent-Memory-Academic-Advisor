from sqlalchemy.orm import Session
from app.repositories.memory_repository import MemoryRepository
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.schemas.memory_schemas import Conversation, UserPreferences, Milestone
import uuid
import logging

logger = logging.getLogger(__name__)


class MemoryService:
    def __init__(self, db: Session, embedding_service: EmbeddingService, vector_store: VectorStore):
        self.repo = MemoryRepository(db)
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def write_memory(self, memory_type: str, data: dict):
        if memory_type == "conversation":
            conv = Conversation(**data)
            model = self.repo.create_conversation(conv)
            memory_id = f"conv:{conv.user_id}:{conv.turn_id}"
            text = f"{conv.role}: {conv.content}"
            metadata = {
                "turn_id": conv.turn_id,
                "role": conv.role,
                "timestamp": conv.timestamp.isoformat()
            }
            self._index_memory(memory_id, text, conv.user_id, memory_type, metadata)
            return {"status": "success", "memory_id": memory_id}
        
        elif memory_type == "preference":
            prefs = UserPreferences(**data)
            self.repo.upsert_preferences(prefs)
            memory_id = f"pref:{prefs.user_id}"
            text = f"User preferences: {prefs.preferences}"
            metadata = {"preferences": str(prefs.preferences)}
            self._index_memory(memory_id, text, prefs.user_id, memory_type, metadata)
            return {"status": "success", "memory_id": memory_id}
        
        elif memory_type == "milestone":
            milestone = Milestone(**data)
            self.repo.upsert_milestone(milestone)
            memory_id = f"mile:{milestone.user_id}:{milestone.milestone_id}"
            text = f"Milestone {milestone.milestone_id}: {milestone.description} status {milestone.status}"
            metadata = {
                "milestone_id": milestone.milestone_id,
                "status": milestone.status
            }
            self._index_memory(memory_id, text, milestone.user_id, memory_type, metadata)
            return {"status": "success", "memory_id": memory_id}
        
        else:
            raise ValueError(f"Unsupported memory_type: {memory_type}")

    def _index_memory(self, memory_id: str, text: str, user_id: str, memory_type: str, metadata: dict):
        try:
            embedding = self.embedding_service.embed_text(text)
            self.vector_store.collection.upsert(
                ids=[memory_id],
                embeddings=[embedding],
                documents=[text],
                metadatas=[{"user_id": user_id, "memory_type": memory_type, **metadata}]
            )
        except Exception as e:
            logger.error(f"Vector indexing error for {memory_id}: {e}")
            raise

    def read_memories(self, user_id: str, query_type: str, params: dict):
        if query_type == "last_n_turns":
            n = int(params.get("n", 5))
            if n <= 0:
                raise ValueError("n must be positive")
            # enforce reasonable max
            max_n = 100
            if n > max_n:
                n = max_n
            models = self.repo.get_recent_conversations(user_id, n)
            # Return in chronological order
            results = []
            for m in reversed(models):
                results.append({
                    "user_id": m.user_id,
                    "turn_id": m.turn_id,
                    "role": m.role,
                    "content": m.content,
                    "timestamp": m.timestamp.isoformat()
                })
            return results
        elif query_type == "preferences":
            prefs = self.repo.get_preferences(user_id)
            if prefs:
                return [{"user_id": prefs.user_id, "preferences": prefs.preferences}]
            return []
        elif query_type == "milestones":
            milestones = self.repo.get_milestones(user_id)
            return [
                {
                    "user_id": m.user_id,
                    "milestone_id": m.milestone_id,
                    "description": m.description,
                    "status": m.status,
                    "date_achieved": m.date_achieved.isoformat() if m.date_achieved else None
                }
                for m in milestones
            ]
        else:
            raise ValueError(f"Unsupported query_type: {query_type}")

    def retrieve_by_context(self, user_id: str, query_text: str, top_k: int | None = None):
        from app.services.retrieval_service import RetrievalService
        retrieval = RetrievalService(self.vector_store)
        return retrieval.retrieve_by_context(user_id, query_text, top_k)
