from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from core.database.base_model import MongoModel


class StickyType(str, Enum):
    PLAIN = "PLAIN"
    EMBED = "EMBED"

class StickyStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    REMOVED = "REMOVED"



class StickyMessage(MongoModel):
    guild_id : int
    channel_id: int
    message_id: int
    is_active: Optional[bool] = Field(default=True, description="Whether or not the message has been synced")
    speed_threshold: Optional[int] = Field(default=5, description="The speed threshold of the message")
    type: Optional[StickyType] = StickyType.PLAIN.value
    status: Optional[StickyStatus] = StickyStatus.ACTIVE.value
    last_message_id: Optional[int] = Field(default=None, description="The last message ID")