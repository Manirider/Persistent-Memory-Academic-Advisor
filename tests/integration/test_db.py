from app.repositories.memory_repository import MemoryRepository
from app.schemas.memory_schemas import Conversation, UserPreferences, Milestone


def test_conversation_upsert(temp_db):
    db, _ = temp_db
    repo = MemoryRepository(db)
    conv = Conversation(user_id="u1", turn_id=1, role="user", content="hello")
    model = repo.create_conversation(conv)
    assert model.content == "hello"
    # duplicate
    conv2 = Conversation(user_id="u1", turn_id=1, role="user", content="changed")
    model2 = repo.create_conversation(conv2)
    assert model2.content == "changed"
    assert model.id == model2.id


def test_preferences_upsert(temp_db):
    db, _ = temp_db
    repo = MemoryRepository(db)
    prefs = UserPreferences(user_id="u1", preferences={"a":1})
    repo.upsert_preferences(prefs)
    prefs2 = UserPreferences(user_id="u1", preferences={"b":2})
    repo.upsert_preferences(prefs2)
    fetched = repo.get_preferences("u1")
    assert fetched.preferences == {"b":2}


def test_milestone_upsert(temp_db):
    db, _ = temp_db
    repo = MemoryRepository(db)
    m = Milestone(user_id="u1", milestone_id="m1", description="d", status="planned")
    repo.upsert_milestone(m)
    ms = repo.get_milestones("u1")
    assert len(ms) == 1
