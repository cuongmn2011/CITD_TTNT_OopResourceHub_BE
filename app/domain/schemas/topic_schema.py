from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.domain.schemas.section_schema import SectionCreate, SectionResponse

# --- Topic Schemas ---
class TopicBase(BaseModel):
    title: str
    short_definition: Optional[str] = None
    category_id: Optional[int] = None

class TopicCreate(TopicBase):
    sections: List[SectionCreate] = [] # Cho phép tạo luôn section khi tạo topic
    tag_ids: List[int] = []  # Danh sách tag IDs khi tạo topic

class TopicListItem(TopicBase):
    """Lightweight schema for topic list - no sections/tags"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class TopicResponse(TopicBase):
    id: int
    created_at: datetime
    sections: List[SectionResponse] = []
    tags: List['TagResponse'] = []  # Danh sách tags của topic

    class Config:
        from_attributes = True

# Import để avoid circular dependency
from app.domain.schemas.tag_schema import TagResponse
TopicResponse.model_rebuild()