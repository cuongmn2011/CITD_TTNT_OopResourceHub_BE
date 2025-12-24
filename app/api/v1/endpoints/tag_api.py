from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.application.services.tag_service import TagService
from app.domain.schemas.tag_schema import TagCreate, TagUpdate, TagResponse, TagWithTopics
from app.infrastructure.database import get_db
from app.infrastructure.repositories.tag_repository import TagRepository

router = APIRouter()


def get_tag_service(db: Session = Depends(get_db)) -> TagService:
    """Dependency injection cho TagService"""
    tag_repo = TagRepository(db)
    return TagService(tag_repo)


@router.get("/", response_model=List[TagResponse])
def get_all_tags(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: TagService = Depends(get_tag_service)
):
    """
    Lấy tất cả tags với phân trang.
    
    - **skip**: Số lượng tags bỏ qua
    - **limit**: Số lượng tags tối đa trả về
    """
    return service.get_all_tags(skip, limit)


@router.get("/popular", response_model=List[TagResponse])
def get_popular_tags(
    limit: int = Query(10, ge=1, le=50, description="Số lượng tags phổ biến"),
    service: TagService = Depends(get_tag_service)
):
    """
    Lấy các tags phổ biến nhất (có nhiều topics nhất).
    
    Hữu ích cho:
    - Hiển thị tag cloud
    - Gợi ý tags khi tạo topic mới
    - Trending topics
    """
    return service.get_popular_tags(limit)


@router.get("/{tag_id}", response_model=TagWithTopics)
def get_tag_by_id(
    tag_id: int,
    service: TagService = Depends(get_tag_service)
):
    """
    Lấy thông tin chi tiết một tag kèm danh sách topic IDs.
    """
    return service.get_tag_by_id(tag_id)


@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag_data: TagCreate,
    service: TagService = Depends(get_tag_service)
):
    """
    Tạo tag mới.
    
    - **name**: Tên hiển thị (VD: "Design Patterns")
    - **slug**: URL-friendly identifier (VD: "design-patterns")
    - **description**: Mô tả ngắn về tag (optional)
    """
    return service.create_tag(tag_data)


@router.put("/{tag_id}", response_model=TagResponse)
def update_tag(
    tag_id: int,
    tag_data: TagUpdate,
    service: TagService = Depends(get_tag_service)
):
    """Cập nhật thông tin tag"""
    return service.update_tag(tag_id, tag_data)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: int,
    service: TagService = Depends(get_tag_service)
):
    """
    Xóa tag.
    
    Note: Topics liên kết với tag này sẽ không bị xóa,
    chỉ mối quan hệ N-N bị remove.
    """
    service.delete_tag(tag_id)
    return None
