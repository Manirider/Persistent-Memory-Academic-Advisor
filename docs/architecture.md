# Architecture

## Overview

The system provides a shared MemoryService used by both FastAPI REST endpoints and MCP tools.

## Components

- **app/main.py**: FastAPI app factory
- **app/api/**: HTTP routers for health, tools, memory
- **app/mcp/server.py**: MCP server exposing three tools
- **app/services/memory_service.py**: Business logic coordinating SQLAlchemy and vector store
- **app/db/**: SQLAlchemy models and session
- **app/services/embedding_service.py**: SentenceTransformer lifecycle
- **app/services/vector_store.py**: ChromaDB persistent client
- **app/schemas/memory_schemas.py**: Pydantic v2 models

## Data Flow

Write: Validate → Persist SQLite → Generate embedding → Upsert ChromaDB

Read structured: SQL query with user isolation

Retrieve semantic: ChromaDB query filtered by user_id, return content + metadata + score

## Persistence

SQLite tables: conversations, user_preferences, milestones

ChromaDB collection: academic_memories with metadata user_id, memory_type

## Diagram

See memory_architecture.png
