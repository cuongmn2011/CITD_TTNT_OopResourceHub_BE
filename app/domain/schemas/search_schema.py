from typing import Literal, Optional
from pydantic import BaseModel
from datetime import datetime


class SearchResultBase(BaseModel):
    """Base schema for search results"""
    type: Literal["topic", "section", "category"]
    id: int
    title: str
    score: float  # Relevance score


class TopicSearchResult(SearchResultBase):
    """Search result for topics"""
    type: Literal["topic"] = "topic"
    short_definition: Optional[str] = None
    category_id: int
    category_name: str
    created_at: datetime

    class Config:
        from_attributes = True


class SectionSearchResult(SearchResultBase):
    """Search result for sections"""
    type: Literal["section"] = "section"
    heading: str
    topic_id: int
    topic_title: str
    content_preview: Optional[str] = None  # First 200 chars

    class Config:
        from_attributes = True


class CategorySearchResult(SearchResultBase):
    """Search result for categories"""
    type: Literal["category"] = "category"
    description: Optional[str] = None
    topic_count: int

    class Config:
        from_attributes = True


class SearchResponse(BaseModel):
    """Combined search response"""
    query: str
    total_results: int
    topics: list[TopicSearchResult] = []
    sections: list[SectionSearchResult] = []
    categories: list[CategorySearchResult] = []
