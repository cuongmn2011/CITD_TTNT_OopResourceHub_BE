from pydantic import BaseModel, Field, field_validator
from typing import Optional

class SectionBase(BaseModel):
    """Base schema for Section with common fields"""
    heading: str = Field(..., min_length=1, max_length=200, description="Section heading")
    content: str = Field(..., min_length=1, description="Section content")
    image_url: Optional[str] = Field(None, description="Optional image URL")
    code_snippet: Optional[str] = Field(None, description="Optional code snippet")
    language: Optional[str] = Field(None, max_length=50, description="Programming language for code snippet")
    order_index: int = Field(..., ge=0, description="Display order of section within topic")

    @field_validator('language')
    @classmethod
    def validate_language(cls, v: Optional[str]) -> Optional[str]:
        """Validate programming language format"""
        if v is not None:
            # Normalize to lowercase
            v = v.strip().lower()
            # Common languages
            allowed_languages = {
                'python', 'java', 'javascript', 'typescript', 'c', 'cpp', 'c++',
                'csharp', 'c#', 'go', 'rust', 'ruby', 'php', 'swift', 'kotlin',
                'sql', 'html', 'css', 'bash', 'shell', 'json', 'xml', 'yaml'
            }
            if v not in allowed_languages:
                # Still allow it but normalize
                pass
        return v

class SectionCreate(SectionBase):
    """Schema for creating a new Section"""
    topic_id: int = Field(..., gt=0, description="ID of the topic this section belongs to")

class SectionUpdate(BaseModel):
    """Schema for updating an existing Section (all fields optional)"""
    heading: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    image_url: Optional[str] = None
    code_snippet: Optional[str] = None
    language: Optional[str] = Field(None, max_length=50)
    order_index: Optional[int] = Field(None, ge=0)
    topic_id: Optional[int] = Field(None, gt=0)

    @field_validator('language')
    @classmethod
    def validate_language(cls, v: Optional[str]) -> Optional[str]:
        """Validate programming language format"""
        if v is not None:
            v = v.strip().lower()
        return v

class SectionResponse(SectionBase):
    """Schema for Section response"""
    id: int
    topic_id: int

    class Config:
        from_attributes = True  # Pydantic v2 compatibility
