from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.models import ConversationModel, UserPreferencesModel, MilestoneModel
from app.schemas.memory_schemas import Conversation, UserPreferences, Milestone
from datetime import datetime


class MemoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_conversation(self, conv: Conversation) -> ConversationModel:
        existing = self.db.query(ConversationModel).filter_by(
            user_id=conv.user_id, turn_id=conv.turn_id
        ).first()
        if existing:
            # Update existing
            existing.role = conv.role
            existing.content = conv.content
            existing.timestamp = conv.timestamp
            self.db.commit()
            self.db.refresh(existing)
            return existing
        
        model = ConversationModel(
            user_id=conv.user_id,
            turn_id=conv.turn_id,
            role=conv.role,
            content=conv.content,
            timestamp=conv.timestamp,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def get_recent_conversations(self, user_id: str, n: int) -> list[ConversationModel]:
        return (
            self.db.query(ConversationModel)
            .filter_by(user_id=user_id)
            .order_by(desc(ConversationModel.timestamp), desc(ConversationModel.turn_id))
            .limit(n)
            .all()
        )

    def upsert_preferences(self, prefs: UserPreferences) -> UserPreferencesModel:
        existing = self.db.query(UserPreferencesModel).filter_by(user_id=prefs.user_id).first()
        if existing:
            existing.preferences = prefs.preferences
            self.db.commit()
            self.db.refresh(existing)
            return existing
        
        model = UserPreferencesModel(user_id=prefs.user_id, preferences=prefs.preferences)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def get_preferences(self, user_id: str) -> UserPreferencesModel | None:
        return self.db.query(UserPreferencesModel).filter_by(user_id=user_id).first()

    def upsert_milestone(self, milestone: Milestone) -> MilestoneModel:
        existing = self.db.query(MilestoneModel).filter_by(
            user_id=milestone.user_id, milestone_id=milestone.milestone_id
        ).first()
        if existing:
            existing.description = milestone.description
            existing.status = milestone.status
            existing.date_achieved = milestone.date_achieved
            self.db.commit()
            self.db.refresh(existing)
            return existing
        
        model = MilestoneModel(
            user_id=milestone.user_id,
            milestone_id=milestone.milestone_id,
            description=milestone.description,
            status=milestone.status,
            date_achieved=milestone.date_achieved,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def get_milestones(self, user_id: str) -> list[MilestoneModel]:
        return self.db.query(MilestoneModel).filter_by(user_id=user_id).all()
