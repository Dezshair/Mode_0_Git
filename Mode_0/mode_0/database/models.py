"""
Database models for the Mode_0 bot.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Any

@dataclass
class User:
    """User model"""
    user_id: str
    username: str
    display_name: str
    first_seen: datetime
    last_seen: datetime
    message_count: int
    profile: Dict[str, Any]

@dataclass
class Message:
    """Message model"""
    id: Optional[int]
    user_id: str
    content: str
    channel: str
    timestamp: datetime

@dataclass
class Conversation:
    """Conversation model"""
    id: Optional[int]
    start_time: datetime
    end_time: Optional[datetime]
    user_id: str
    summary: Optional[str]
    messages: List[Message] = None
