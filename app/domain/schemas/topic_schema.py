from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- Section Schemas ---
class SectionBase(BaseModel):
    heading: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    code_snippet: Optional[str] = None
    language: str = "python"
    order_index: int = 0

class SectionCreate(SectionBase):
    pass

class SectionResponse(SectionBase):
    id: int
    
    class Config:
        from_attributes = True # Pydantic v2 (dùng orm_mode = True nếu v1)

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