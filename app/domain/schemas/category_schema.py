from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

# --- Category Schemas ---
class CategoryBase(BaseModel):
    name: str
    slug: str

class CategoryCreate(CategoryBase):
    """Schema để tạo category mới"""
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Tên category không được để trống')
        if len(v) > 100:
            raise ValueError('Tên category không được vượt quá 100 ký tự')
        return v.strip()
    
    @field_validator('slug')
    @classmethod
    def validate_slug(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Slug không được để trống')
        # Slug chỉ chứa chữ thường, số và dấu gạch ngang
        if not v.replace('-', '').replace('_', '').isalnum():
            raise ValueError('Slug chỉ được chứa chữ cái, số, gạch ngang và gạch dưới')
        return v.strip().lower()

class CategoryUpdate(BaseModel):
    """Schema để cập nhật category"""
    name: Optional[str] = None
    slug: Optional[str] = None
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError('Tên category không được để trống')
            if len(v) > 100:
                raise ValueError('Tên category không được vượt quá 100 ký tự')
            return v.strip()
        return v
    
    @field_validator('slug')
    @classmethod
    def validate_slug(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError('Slug không được để trống')
            if not v.replace('-', '').replace('_', '').isalnum():
                raise ValueError('Slug chỉ được chứa chữ cái, số, gạch ngang và gạch dưới')
            return v.strip().lower()
        return v

class CategoryResponse(CategoryBase):
    """Schema response trả về cho client"""
    id: int
    
    class Config:
        from_attributes = True
