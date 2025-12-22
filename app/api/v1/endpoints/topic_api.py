from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.application.services.topic_service import TopicService
from app.domain.schemas.topic_schema import TopicCreate, TopicResponse
from app.infrastructure.database import get_db
from app.infrastructure.repositories.topic_repository import TopicRepository

router = APIRouter()


class RelatedTopicResponse(BaseModel):
    topic: TopicResponse
    score: float


# Dependency để tạo service với repository injection
def get_topic_service(db: Session = Depends(get_db)) -> TopicService:
    """
    Dependency injection: tạo TopicService với TopicRepository
    Tuân thủ Dependency Inversion Principle
    """
    topic_repo = TopicRepository(db)
    return TopicService(topic_repo)


@router.get("/{topic_id}", response_model=TopicResponse)
def get_topic(topic_id: int, service: TopicService = Depends(get_topic_service)):
    """Lấy thông tin chi tiết một topic"""
    try:
        topic = service.get_topic_by_id(topic_id)
        if not topic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Topic với ID {topic_id} không tồn tại",
            )
        return topic
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi lấy topic: {str(e)}",
        )


@router.get("/", response_model=List[TopicResponse])
def get_topics(
    skip: int = 0, limit: int = 100, service: TopicService = Depends(get_topic_service)
):
    """Lấy danh sách topics với phân trang"""
    try:
        return service.get_all_topics(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi lấy danh sách topics: {str(e)}",
        )


@router.post("/", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
def create_topic(
    topic_in: TopicCreate, service: TopicService = Depends(get_topic_service)
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


@router.put("/{topic_id}", response_model=TopicResponse)
def update_topic(
    topic_id: int,
    topic_in: TopicCreate,
    service: TopicService = Depends(get_topic_service),
):
    """Cập nhật topic"""
    try:
        topic = service.update_topic(topic_id, topic_in)
        if not topic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Topic với ID {topic_id} không tồn tại",
            )
        return topic
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi cập nhật topic: {str(e)}",
        )


@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_topic(topic_id: int, service: TopicService = Depends(get_topic_service)):
    """Xóa topic"""
    try:
        success = service.delete_topic(topic_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Topic với ID {topic_id} không tồn tại",
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi xóa topic: {str(e)}",
        )


@router.get("/{topic_id}/related", response_model=List[RelatedTopicResponse])
async def get_related_topics(
    topic_id: int,
    top_n: int = Query(
        default=5, ge=1, le=20, description="Số lượng topics liên quan (1-20)"
    ),
    service: TopicService = Depends(get_topic_service),
):
    """
    Tìm các topics liên quan đến một topic cụ thể.

    Sử dụng thuật toán:
    - **TF-IDF**: Tính độ tương đồng nội dung giữa các topics
    - **Heuristic Scoring**: Áp dụng các quy tắc:
        - Cùng category: +0.3 điểm bonus
        - Từ khóa trùng khớp trong title: +0.2 điểm
        - Độ dài definition tương tự: +0.1 điểm

    **Combined Score**: TF-IDF (70%) + Heuristic (30%)

    Args:
    - topic_id: ID của topic cần tìm related topics
    - top_n: Số lượng topics liên quan cần trả về (1-20, mặc định 5)

    Returns:
        Danh sách topics liên quan kèm điểm số, sắp xếp theo độ liên quan giảm dần
    """
    try:
        # Tìm related topics
        related_topics = service.find_related_topics(topic_id, top_n)

        if not related_topics:
            # Kiểm tra xem topic có tồn tại không
            topic = service.get_topic_by_id(topic_id)
            if not topic:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Topic with id {topic_id} not found",
                )
            # Topic tồn tại nhưng không có related topics
            return []

        return related_topics

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error finding related topics: {str(e)}",
        )
