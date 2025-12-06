from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.domain.schemas.topic_schema import TopicCreate, TopicResponse
from app.application.services.topic_service import TopicService
from app.infrastructure.repositories.topic_repository import TopicRepository

router = APIRouter()

# Dependency để tạo service với repository injection
def get_topic_service(db: Session = Depends(get_db)) -> TopicService:
    """
    Dependency injection: tạo TopicService với TopicRepository
    Tuân thủ Dependency Inversion Principle
    """
    topic_repo = TopicRepository(db)
    return TopicService(topic_repo)

@router.post("/", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
def create_topic(
    topic_in: TopicCreate, 
    service: TopicService = Depends(get_topic_service)
):
    """
    Tạo bài học mới (kèm theo các section chi tiết)
    
    - **title**: Tên bài học
    - **short_definition**: Định nghĩa ngắn gọn
    - **category_id**: ID của danh mục (Category)
    - **sections**: Danh sách các phần chi tiết
    """
    try:
        return service.create_new_topic(topic_in)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{topic_id}", response_model=TopicResponse)
def get_topic(
    topic_id: int, 
    service: TopicService = Depends(get_topic_service)
):
    """Lấy thông tin chi tiết một topic"""
    topic = service.get_topic_by_id(topic_id)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Topic với ID {topic_id} không tồn tại"
        )
    return topic

@router.get("/", response_model=List[TopicResponse])
def get_topics(
    skip: int = 0,
    limit: int = 100,
    service: TopicService = Depends(get_topic_service)
):
    """Lấy danh sách topics với phân trang"""
    return service.get_all_topics(skip=skip, limit=limit)

@router.put("/{topic_id}", response_model=TopicResponse)
def update_topic(
    topic_id: int,
    topic_in: TopicCreate,
    service: TopicService = Depends(get_topic_service)
):
    """Cập nhật topic"""
    topic = service.update_topic(topic_id, topic_in)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic với ID {topic_id} không tồn tại"
        )
    return topic

@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_topic(
    topic_id: int,
    service: TopicService = Depends(get_topic_service)
):
    """Xóa topic"""
    success = service.delete_topic(topic_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic với ID {topic_id} không tồn tại"
        )
    return None