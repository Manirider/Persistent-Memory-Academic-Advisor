from app.services.vector_store import VectorStore
from app.config import settings


class RetrievalService:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def retrieve_by_context(self, user_id: str, query_text: str, top_k: int | None = None):
        k = top_k or settings.TOP_K_DEFAULT
        if k > settings.MAX_TOP_K:
            k = settings.MAX_TOP_K
        results = self.vector_store.search(query_text, user_id, top_k=k)
        
        documents = results.get('documents', [[]])[0]
        metadatas = results.get('metadatas', [[]])[0]
        distances = results.get('distances', [[]])[0]
        
        out = []
        for doc, meta, dist in zip(documents, metadatas, distances):
            # Convert cosine distance to similarity score (1 - distance)
            score = 1.0 - float(dist) if dist is not None else 0.0
            out.append({
                "content": doc,
                "metadata": meta,
                "score": round(score, 4)
            })
        return out
