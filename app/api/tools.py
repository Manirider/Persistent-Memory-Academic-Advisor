from fastapi import APIRouter
from app.schemas.memory_schemas import ToolsResponse

router = APIRouter()


@router.get("/tools", response_model=ToolsResponse)
def list_tools():
    return {
        "tools": [
            {"name": "memory_write", "description": "Write a memory of type conversation, preference, or milestone"},
            {"name": "memory_read", "description": "Read memories for a user with query type and params"},
            {"name": "memory_retrieve_by_context", "description": "Retrieve semantically relevant memories by context query"},
        ]
    }
