from pydantic import BaseModel
from typing import Optional, List


class TopProduct(BaseModel):
    term: str
    frequency: int


class ChannelActivity(BaseModel):
    channel_name: str
    date: str
    message_count: int


class MessageSearchResult(BaseModel):
    message_id: int
    channel_name: str
    message_text: str
    message_date: str


class VisualContentStat(BaseModel):
    channel_name: str
    total_images: int
    avg_confidence: Optional[float]
