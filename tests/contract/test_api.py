from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_tools():
    r = client.get("/tools")
    assert r.status_code == 200
    tools = r.json()["tools"]
    names = [t["name"] for t in tools]
    assert "memory_write" in names
    assert "memory_read" in names
    assert "memory_retrieve_by_context" in names


def test_memory_write():
    payload = {
        "memory_type": "conversation",
        "data": {"user_id": "u1", "turn_id": 1, "role": "user", "content": "hi"}
    }
    r = client.post("/invoke/memory_write", json=payload)
    assert r.status_code == 201
    assert r.json()["status"] == "success"


def test_memory_read():
    # first write
    client.post("/invoke/memory_write", json={
        "memory_type": "conversation",
        "data": {"user_id": "u2", "turn_id": 1, "role": "user", "content": "test"}
    })
    r = client.post("/invoke/memory_read", json={
        "user_id": "u2",
        "query_type": "last_n_turns",
        "params": {"n": 1}
    })
    assert r.status_code == 200
    results = r.json()["results"]
    assert len(results) == 1
    assert results[0]["content"] == "test"
