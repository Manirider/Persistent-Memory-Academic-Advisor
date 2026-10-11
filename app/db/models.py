from sqlalchemy import Column, String, Integer, DateTime, Text, JSON, UniqueConstraint, Index
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class ConversationModel(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    turn_id = Column(Integer, nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'turn_id', name='uq_conversation_user_turn'),
        Index('idx_conversations_user_timestamp', 'user_id', 'timestamp'),
        Index('idx_conversations_user_turn', 'user_id', 'turn_id'),
    )


class UserPreferencesModel(Base):
    __tablename__ = "user_preferences"
    
    user_id = Column(String, primary_key=True)
    preferences = Column(JSON, nullable=False)


class MilestoneModel(Base):
    __tablename__ = "milestones"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    milestone_id = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String, nullable=False)
    date_achieved = Column(DateTime, nullable=True)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'milestone_id', name='uq_milestone_user_id'),
        Index('idx_milestones_user', 'user_id'),
    )
