from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.memory_service import MemoryService
from app.schemas.memory_schemas import MemoryWriteRequest, MemoryWriteResponse, MemoryReadRequest, MemoryReadResponse, MemoryRetrieveRequest, MemoryRetrieveResponse

router = APIRouter()


def get_memory_service(db: Session = Depends(get_db)):
    embedding_service = EmbeddingService()
    vector_store = VectorStore()
    return MemoryService(db, embedding_service, vector_store)


@router.post("/invoke/memory_write", response_model=MemoryWriteResponse, status_code=status.HTTP_201_CREATED)
def memory_write(req: MemoryWriteRequest, service: MemoryService = Depends(get_memory_service)):
    try:
        result = service.write_memory(req.memory_type, req.data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal error")


@router.post("/invoke/memory_read", response_model=MemoryReadResponse)
def memory_read(req: MemoryReadRequest, service: MemoryService = Depends(get_memory_service)):
    try:
        results = service.read_memories(req.user_id, req.query_type, req.params)
        return {"results": results}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal error")


@router.post("/invoke/memory_retrieve_by_context", response_model=MemoryRetrieveResponse)
def memory_retrieve(req: MemoryRetrieveRequest, service: MemoryService = Depends(get_memory_service)):
    try:
        results = service.retrieve_by_context(req.user_id, req.query_text, req.top_k)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal error")
