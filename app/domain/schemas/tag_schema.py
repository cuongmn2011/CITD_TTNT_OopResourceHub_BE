from typing import Optional
from pydantic import BaseModel, Field


class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    slug: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    slug: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None


class TagResponse(TagBase):
    id: int
    topic_count: Optional[int] = 0  # Số lượng topics có tag này

    class Config:
        from_attributes = True


class TagWithTopics(TagResponse):
    """Tag kèm danh sách topic IDs"""
    topic_ids: list[int] = []
