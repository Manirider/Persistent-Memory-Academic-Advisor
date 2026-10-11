from mcp.server import MCPServer
from app.db.database import SessionLocal
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.memory_service import MemoryService
import logging

logger = logging.getLogger(__name__)

mcp = MCPServer("academic-advisor-mcp")


def get_service():
    db = SessionLocal()
    embedding_service = EmbeddingService()
    vector_store = VectorStore()
    return MemoryService(db, embedding_service, vector_store), db


@mcp.tool()
def memory_write(memory_type: str, data: dict) -> dict:
    """Write a memory of type conversation, preference, or milestone"""
    service, db = get_service()
    try:
        result = service.write_memory(memory_type, data)
        db.commit()
        return result
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()


@mcp.tool()
def memory_read(user_id: str, query_type: str, params: dict) -> dict:
    """Read memories for a user with query type and params"""
    service, db = get_service()
    try:
        results = service.read_memories(user_id, query_type, params)
        return {"results": results}
    finally:
        db.close()


@mcp.tool()
def memory_retrieve_by_context(user_id: str, query_text: str, top_k: int = 5) -> dict:
    """Retrieve semantically relevant memories by context query"""
    service, db = get_service()
    try:
        results = service.retrieve_by_context(user_id, query_text, top_k)
        return {"results": results}
    finally:
        db.close()


if __name__ == "__main__":
    # For stdio transport
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await mcp.run(read_stream, write_stream)
    
    asyncio.run(main())
