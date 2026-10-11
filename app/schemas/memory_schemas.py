from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any


def now_utc():
    return datetime.now(timezone.utc)


class Conversation(BaseModel):
    user_id: str = Field(..., min_length=1)
    turn_id: int = Field(..., ge=1)
    role: str
    content: str = Field(..., min_length=1)
    timestamp: datetime = Field(default_factory=now_utc)

    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        allowed = {"user", "assistant", "system"}
        if v not in allowed:
            raise ValueError(f"role must be one of {allowed}")
        return v


class UserPreferences(BaseModel):
    user_id: str = Field(..., min_length=1)
    preferences: Dict[str, Any]

    @field_validator('preferences')
    @classmethod
    def validate_preferences(cls, v):
        # Ensure JSON serializable
        try:
            import json
            json.dumps(v)
        except Exception as e:
            raise ValueError("preferences must be JSON serializable")
        return v


class Milestone(BaseModel):
    user_id: str = Field(..., min_length=1)
    milestone_id: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    status: str
    date_achieved: Optional[datetime] = None

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        allowed = {"planned", "in-progress", "completed"}
        if v not in allowed:
            raise ValueError(f"status must be one of {allowed}")
        return v


# API Schemas
class MemoryWriteRequest(BaseModel):
    memory_type: str
    data: Dict[str, Any]


class MemoryWriteResponse(BaseModel):
    status: str
    memory_id: str


class MemoryReadRequest(BaseModel):
    user_id: str
    query_type: str
    params: Dict[str, Any]


class MemoryReadResponse(BaseModel):
    results: list[Dict[str, Any]]


class MemoryRetrieveRequest(BaseModel):
    user_id: str
    query_text: str
    top_k: Optional[int] = None


class MemoryRetrieveResponse(BaseModel):
    results: list[Dict[str, Any]]


class HealthResponse(BaseModel):
    status: str


class ToolsResponse(BaseModel):
    tools: list[Dict[str, str]]
