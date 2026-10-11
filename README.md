# 🎓 Persistent-Memory AI Academic Advisor

<p align="center">
  <strong>Production-grade, FAANG-caliber persistent memory backend and Model Context Protocol (MCP) server for personalized student advising.</strong>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/release/python-3110/"><img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white" alt="Python 3.11+"></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat&logo=fastapi&logoColor=white" alt="FastAPI"></a>
  <a href="https://modelcontextprotocol.io/"><img src="https://img.shields.io/badge/MCP-1.0+-4B32C3?style=flat&logo=anthropic&logoColor=white" alt="Model Context Protocol"></a>
  <a href="https://www.trychroma.com/"><img src="https://img.shields.io/badge/ChromaDB-Vector_Store-FF6F61?style=flat" alt="ChromaDB"></a>
  <a href="https://www.sqlite.org/"><img src="https://img.shields.io/badge/SQLite-SQLAlchemy_2.0-003B57?style=flat&logo=sqlite&logoColor=white" alt="SQLite"></a>
  <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker&logoColor=white" alt="Docker"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/badge/Code_Style-Ruff-black?style=flat" alt="Ruff"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat" alt="License: MIT"></a>
</p>

<p align="center">
  <a href="https://render.com/deploy?repo=https://github.com/Manirider/Persistent-Memory-Academic-Advisor">
    <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
  </a>
</p>

---

## 🌐 Live Demo & Deployment

Deploy this project with **1 click** to get a free, permanent HTTPS live link:

1. Click the **[Deploy to Render](https://render.com/deploy?repo=https://github.com/Manirider/Persistent-Memory-Academic-Advisor)** button above (or create a Web Service on [Render.com](https://render.com/) and select your GitHub repository `Persistent-Memory-Academic-Advisor`).
2. Render automatically detects [`render.yaml`](render.yaml) and builds the Docker container.
3. Once deployed, your live URL will be active with:
   - **Interactive Web Playground**: `https://<your-service-name>.onrender.com/`
   - **Swagger API Documentation**: `https://<your-service-name>.onrender.com/docs`
   - **Live Health Probe**: `https://<your-service-name>.onrender.com/health`

---

## 📌 Executive Overview

The **Persistent-Memory AI Academic Advisor** provides an intelligent, dual-tier memory engine built to bridge long-term student state across advising sessions. Conventional conversational AI systems suffer from stateless amnesia across context windows; this system guarantees persistent, cross-session continuity through:

1. **Deterministic Structured Memory**: Relational tracking of sequential conversations, customizable student preference models, and academic milestone progressions stored with strict relational integrity via **SQLAlchemy 2.x** and **SQLite**.
2. **Contextual Semantic Memory**: Sub-second approximate nearest neighbor (ANN) vector retrieval powered by **ChromaDB** and Hugging Face's `sentence-transformers` (`all-MiniLM-L6-v2`) embeddings.
3. **Dual Protocol Interoperability**: Exposes unified memory capabilities across standard **FastAPI REST endpoints** and an official **Model Context Protocol (MCP)** server for seamless native integration into LLM agents (Claude Desktop, Cursor, LangChain, etc.).

---

## 🏛️ System Architecture

```
                            ┌────────────────────────┐
                            │     Student Client     │
                            └───────────┬────────────┘
                                        │
                                        ▼
                            ┌────────────────────────┐
                            │ Academic Advisor Agent │
                            └───────────┬────────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    │                                       │
                    ▼                                       ▼
         ┌─────────────────────┐                 ┌─────────────────────┐
         │  FastAPI REST API   │                 │   Stdio MCP Server  │
         │  (/invoke/*, /tools)│                 │   (JSON-RPC 2.0)    │
         └──────────┬──────────┘                 └──────────┬──────────┘
                    │                                       │
                    └───────────────────┬───────────────────┘
                                        ▼
                            ┌────────────────────────┐
                            │     MemoryService      │
                            │ (Business Logic Layer) │
                            └───────────┬────────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    │                                       │
                    ▼                                       ▼
         ┌─────────────────────┐                 ┌─────────────────────┐
         │  Memory Repository  │                 │  Embedding Service  │
         │  (SQLAlchemy 2.x)   │                 │ (all-MiniLM-L6-v2)  │
         └──────────┬──────────┘                 └──────────┬──────────┘
                    │                                       │
                    ▼                                       ▼
         ┌─────────────────────┐                 ┌─────────────────────┐
         │    SQLite Store     │                 │      ChromaDB       │
         │ (Relational Tables) │                 │ (Vector Collection) │
         └─────────────────────┘                 └─────────────────────┘
```

### Flow Breakdown
- **Write Path**: Incoming memory payloads are validated via Pydantic v2 schemas, persisted into the relational store (SQLite), transformed into high-dimensional dense vector embeddings, and indexed into the ChromaDB vector collection.
- **Read Path (Structured)**: Direct relational queries filtered by `user_id` retrieve historical turns (chronological order), key-value student preferences, and milestone tracking.
- **Retrieve Path (Semantic)**: User-isolated similarity queries against ChromaDB match queries to past academic disclosures, returning content, distance scores, and rich metadata.

---

## ✨ Key Features

- **🧠 Dual-Tier Persistence**: Synchronous relational storage paired with an indexed vector space for exact records and fuzzy semantic lookups.
- **🔌 Model Context Protocol (MCP) Compliant**: Genuine MCP standard tools exposed for direct consumption by modern AI harnesses and agents.
- **🛡️ Strict User Isolation**: Multi-tenant memory boundaries guarantee student data cannot leak across semantic or relational queries.
- **⚡ High-Throughput REST API**: Fully typed FastAPI interface with automatic OpenAPI/Swagger documentation (`/docs`).
- **📦 Container-First Architecture**: One-command Docker Compose deployment mounting persistent storage volumes (`/app/data`).
- **✅ Comprehensive Quality Suite**: Unit, integration, and contract tests with strict linting via Ruff.

---

## 📁 Repository Structure

```
.
├── app/
│   ├── api/                    # FastAPI route controllers
│   │   ├── health.py           # Health check endpoint (/health)
│   │   ├── memory.py           # Memory write, read, and retrieve routes
│   │   └── tools.py            # Tool discovery endpoint (/tools)
│   ├── db/                     # Database engine & ORM models
│   │   ├── database.py         # SQLAlchemy engine & session factory
│   │   └── models.py           # SQLite tables (conversations, preferences, milestones)
│   ├── mcp/                    # Model Context Protocol implementation
│   │   └── server.py           # MCP server exposing stdio tools
│   ├── repositories/           # Data access layer
│   │   └── memory_repository.py# Relational CRUD operations
│   ├── schemas/                # Pydantic v2 data validation schemas
│   │   └── memory_schemas.py   # Request/response and domain contracts
│   ├── services/               # Core business services
│   │   ├── embedding_service.py# SentenceTransformers embedding generation
│   │   ├── memory_service.py   # Unified memory orchestrator
│   │   ├── retrieval_service.py# ChromaDB ANN query runner
│   │   └── vector_store.py     # Persistent ChromaDB client manager
│   ├── config.py               # Environment configuration via Pydantic Settings
│   └── main.py                 # FastAPI application root
├── docs/                       # Architectural specs & design diagrams
│   ├── architecture.md         # Detailed architectural documentation
│   ├── evaluation_report.md    # Requirement verification matrix
│   ├── memory_architecture.mmd # Mermaid diagram source
│   └── memory_architecture.png # Rendered architecture diagram
├── tests/                      # Automated test suite
│   ├── conftest.py             # Pytest fixtures and test environments
│   ├── contract/               # Schema and API contract validation
│   ├── integration/            # Multi-component workflow tests
│   └── unit/                   # Isolated unit tests
├── docker-compose.yml          # Container orchestration with volume mounts
├── Dockerfile                  # Multi-stage production container build
├── pyproject.toml              # Build configurations & package dependencies
├── submission.json             # Evaluation payload benchmark
└── .env.example                # Template environment variables
```

---

## 🚀 Quick Start Guide

### Option 1: One-Command Docker Setup (Recommended)

Ensure Docker and Docker Compose are installed on your machine:

```bash
# Clone the repository
git clone https://github.com/Manirider/Persistent-Memory-Academic-Advisor.git
cd Persistent-Memory-Academic-Advisor

# Build and start container
docker compose up --build
```

Verify service readiness:
```bash
curl http://localhost:8000/health
# Output: {"status":"ok"}
```

Access interactive Swagger documentation at **[http://localhost:8000/docs](http://localhost:8000/docs)**.

---

### Option 2: Local Python Development

#### 1. Prerequisites
- Python 3.11+
- Git

#### 2. Environment Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"
```

#### 3. Configuration
Copy the configuration template:
```bash
cp .env.example .env
```
Default parameters in `.env`:
```ini
DB_PATH=./data/advisor_memory.db
CHROMA_DB_PATH=./data/chroma_db
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
```

#### 4. Run the API Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 📡 API Reference & Contracts

### 1. Health Probe
- **Endpoint**: `GET /health`
- **Response**: `200 OK`
```json
{
  "status": "ok"
}
```

---

### 2. Tool Discovery
- **Endpoint**: `GET /tools`
- **Response**: `200 OK`
```json
{
  "tools": [
    {"name": "memory_write", "description": "Write a memory of type conversation, preference, or milestone"},
    {"name": "memory_read", "description": "Read memories for a user with query type and params"},
    {"name": "memory_retrieve_by_context", "description": "Retrieve semantically relevant memories by context query"}
  ]
}
```

---

### 3. Write Memory
- **Endpoint**: `POST /invoke/memory_write`
- **Response**: `201 Created`

#### Writing a Conversation Turn:
```bash
curl -X POST http://localhost:8000/invoke/memory_write \
  -H "Content-Type: application/json" \
  -d '{
    "memory_type": "conversation",
    "data": {
      "user_id": "student_402",
      "turn_id": 1,
      "role": "user",
      "content": "I am interested in taking advanced bioinformatics and data structures next semester."
    }
  }'
```
```json
{
  "status": "success",
  "memory_id": "conv:student_402:1"
}
```

#### Writing Preferences or Milestones:
```json
// Preferences Payload
{
  "memory_type": "preference",
  "data": {
    "user_id": "student_402",
    "preferences": { "max_credits": 16, "preferred_time": "morning", "target_major": "Bioinformatics" }
  }
}

// Milestone Payload
{
  "memory_type": "milestone",
  "data": {
    "user_id": "student_402",
    "milestone_id": "CS101_REQ",
    "description": "Completed Introduction to Programming",
    "status": "completed"
  }
}
```

---

### 4. Read Structured Memories
- **Endpoint**: `POST /invoke/memory_read`
- **Response**: `200 OK`

```bash
curl -X POST http://localhost:8000/invoke/memory_read \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "student_402",
    "query_type": "last_n_turns",
    "params": {"n": 5}
  }'
```
```json
{
  "results": [
    {
      "user_id": "student_402",
      "turn_id": 1,
      "role": "user",
      "content": "I am interested in taking advanced bioinformatics and data structures next semester.",
      "timestamp": "2026-10-11T08:15:30.000000Z"
    }
  ]
}
```
*Supported `query_type` options: `last_n_turns`, `preferences`, `milestones`.*

---

### 5. Semantic Context Retrieval
- **Endpoint**: `POST /invoke/memory_retrieve_by_context`
- **Response**: `200 OK`

```bash
curl -X POST http://localhost:8000/invoke/memory_retrieve_by_context \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "student_402",
    "query_text": "What computational fields did the student want to explore?",
    "top_k": 3
  }'
```
```json
{
  "results": [
    {
      "id": "conv:student_402:1",
      "content": "user: I am interested in taking advanced bioinformatics and data structures next semester.",
      "score": 0.312,
      "metadata": {
        "user_id": "student_402",
        "memory_type": "conversation",
        "role": "user",
        "turn_id": 1,
        "timestamp": "2026-10-11T08:15:30.000000Z"
      }
    }
  ]
}
```

---

## 🤖 Model Context Protocol (MCP) Integration

The server provides a standard stdio JSON-RPC transport interface compliant with Anthropic's Model Context Protocol.

### Running Standalone MCP Server
```bash
python -m app.mcp.server
```

### Client Integration (e.g., Claude Desktop / Cursor)
Add the server entry to your MCP configuration (e.g. `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "academic-advisor-memory": {
      "command": "python",
      "args": ["-m", "app.mcp.server"],
      "env": {
        "DB_PATH": "/path/to/data/advisor_memory.db",
        "CHROMA_DB_PATH": "/path/to/data/chroma_db",
        "EMBEDDING_MODEL_NAME": "all-MiniLM-L6-v2"
      }
    }
  }
}
```

---

## 🧪 Testing & Code Quality

### Running the Test Suite
Execute tests with pytest:
```bash
pytest tests/ -v
```

### Linting and Formatting
Check code style and enforce formatting rules:
```bash
# Check code style with Ruff
ruff check .

# Automatically apply format fixes
ruff format .
```

---

## 🔒 Security & Production Roadmap

- [x] **Relational Isolation**: User ID scoping on all SQL queries preventing horizontal privilege escalation.
- [x] **Metadata-Filtering in Vector Space**: Hard constraints on vector queries (`where={"user_id": user_id}`).
- [ ] **Authentication & Authorization**: Integrate OAuth2 / JWT bearer tokens for role-based academic advisor sessions.
- [ ] **Distributed Vector Scalability**: Seamless plug-in replacement for Qdrant or Milvus for horizontal clustering.
- [ ] **PostgreSQL + pgvector Integration**: Support for single-engine multi-model relational + vector storage.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for complete details.

---

<p align="center">
  Crafted by <a href="https://github.com/Manirider"><strong>Manirider</strong></a>
</p>
