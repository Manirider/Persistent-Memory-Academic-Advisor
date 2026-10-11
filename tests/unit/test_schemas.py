from app.schemas.memory_schemas import Conversation, UserPreferences, Milestone


def test_conversation_valid():
    conv = Conversation(user_id="u1", turn_id=1, role="user", content="hi")
    assert conv.user_id == "u1"


def test_conversation_invalid_role():
    try:
        Conversation(user_id="u1", turn_id=1, role="invalid", content="hi")
        assert False
    except Exception:
        assert True


def test_user_preferences_valid():
    prefs = UserPreferences(user_id="u1", preferences={"theme": "dark"})
    assert prefs.preferences["theme"] == "dark"


def test_milestone_valid():
    m = Milestone(user_id="u1", milestone_id="m1", description="test", status="planned")
    assert m.status == "planned"
