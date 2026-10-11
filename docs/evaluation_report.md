# Evaluation Report – Persistent-Memory AI Academic Advisor

## Requirement Verification Matrix

| Requirement | Status | Evidence |
|---|---|---|
| Docker startup | Blocked | Docker CLI not available in environment |
| Health endpoint | Blocked | Requires running container |
| Required SQLite tables | Passed | `conversations`, `user_preferences`, `milestones` defined in `app/db/models.py` |
| Conversation persistence | Passed | Unit/integration tests pass for upsert |
| Vector indexing | Blocked | Requires `sentence-transformers`/`chromadb` runtime |
| Semantic retrieval | Blocked | Requires model download and runtime |
| MCP protocol | Blocked | Requires MCP SDK runtime |
| Restart persistence | Blocked | Requires Docker runtime |
| Submission artifacts | Passed | `docker-compose.yml`, `Dockerfile`, `.env.example`, `README.md`, `submission.json`, `docs/memory_architecture.png` exist |
| Automated tests | Partial | Schema & DB tests pass; API/MCP tests blocked by missing dependencies |

## Mandatory Artifacts
- `docker-compose.yml` exists, service named `mcp_server`
- `Dockerfile` exists
- `.env.example` contains `DB_PATH`, `CHROMA_DB_PATH`, `EMBEDDING_MODEL_NAME`
- `README.md` present
- `submission.json` valid JSON with `testUserId` and `testConversation`
- `docs/memory_architecture.png` valid 4KB image

## Pydantic Schemas
Importable models: `Conversation`, `UserPreferences`, `Milestone` with required fields validated.

## SQLite Contracts
Tables defined with correct names, PKs, unique constraints, indexes. `DB_PATH` configurable.

## REST API Contract
Endpoints implemented in code. Runtime verification blocked.

## Vector Persistence
Implementation present. Runtime verification blocked by offline dependencies.

## MCP Server
Implementation present using official SDK. Runtime verification blocked.

## Remaining Issues
- Docker not available → deployment verification blocked
- `sentence-transformers`/`chromadb` not installable offline → semantic retrieval tests blocked
- MCP handshake tests blocked

All fixable code defects addressed. No secrets committed. Documentation accurate.
