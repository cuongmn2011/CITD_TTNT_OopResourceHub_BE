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

class TopicResponse(TopicBase):
    id: int
    created_at: datetime
    sections: List[SectionResponse] = []

    class Config:
        from_attributes = True