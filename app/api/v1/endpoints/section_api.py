from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db
from app.domain.schemas.section_schema import SectionCreate, SectionUpdate, SectionResponse
from app.application.services.section_service import SectionService
from app.infrastructure.repositories.section_repository import SectionRepository
from app.infrastructure.repositories.topic_repository import TopicRepository

router = APIRouter()

def get_section_service(db: Session = Depends(get_db)) -> SectionService:
    """
    Dependency injection cho SectionService.
    Tạo instance của service với các dependencies cần thiết.
    """
    section_repository = SectionRepository(db)
    topic_repository = TopicRepository(db)
    return SectionService(section_repository, topic_repository)

@router.post("/", response_model=SectionResponse, status_code=status.HTTP_201_CREATED)
@router.post("", response_model=SectionResponse, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def create_section(
    section_data: SectionCreate,
    service: SectionService = Depends(get_section_service)
):
    """
    Tạo mới một Section.
    
    - **topic_id**: ID của Topic mà Section này thuộc về (required)
    - **heading**: Tiêu đề của Section (required)
    - **content**: Nội dung chi tiết (required)
    - **order_index**: Thứ tự hiển thị (required, >= 0)
    - **image_url**: URL hình minh họa (optional)
    - **code_snippet**: Đoạn code minh họa (optional)
    - **language**: Ngôn ngữ lập trình của code (optional)
    """
    try:
        return service.create_section(section_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi tạo section: {str(e)}"
        )

@router.get("/", response_model=List[SectionResponse])
def get_all_sections(
    skip: int = 0,
    limit: int = 100,
    service: SectionService = Depends(get_section_service)
):
    """
    Lấy danh sách tất cả Sections với phân trang.
    
    - **skip**: Số lượng bản ghi bỏ qua (default: 0)
    - **limit**: Số lượng bản ghi tối đa trả về (default: 100)
    """
    try:
        return service.get_all_sections(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi lấy danh sách sections: {str(e)}"
        )

@router.get("/topic/{topic_id}", response_model=List[SectionResponse])
def get_sections_by_topic(
    topic_id: int,
    service: SectionService = Depends(get_section_service)
):
    """
    Lấy tất cả Sections thuộc về một Topic, sắp xếp theo order_index.
    
    - **topic_id**: ID của Topic cần lấy sections
    """
    try:
        return service.get_sections_by_topic(topic_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi lấy sections của topic: {str(e)}"
        )

@router.get("/{section_id}", response_model=SectionResponse)
@router.get("/{section_id}/", response_model=SectionResponse, include_in_schema=False)
def get_section_by_id(
    section_id: int,
    service: SectionService = Depends(get_section_service)
):
    """
    Lấy thông tin chi tiết một Section theo ID.
    
    - **section_id**: ID của Section cần lấy
    """
    try:
        return service.get_section_by_id(section_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi lấy section: {str(e)}"
        )

@router.put("/{section_id}", response_model=SectionResponse)
@router.put("/{section_id}/", response_model=SectionResponse, include_in_schema=False)
def update_section(
    section_id: int,
    section_data: SectionUpdate,
    service: SectionService = Depends(get_section_service)
):
    """
    Cập nhật thông tin Section.
    Tất cả các field đều optional, chỉ cập nhật những field được cung cấp.
    
    - **section_id**: ID của Section cần cập nhật
    - **heading**: Tiêu đề mới (optional)
    - **content**: Nội dung mới (optional)
    - **order_index**: Thứ tự hiển thị mới (optional)
    - **topic_id**: Chuyển Section sang Topic khác (optional)
    - **image_url**: URL hình minh họa mới (optional)
    - **code_snippet**: Code snippet mới (optional)
    - **language**: Ngôn ngữ code mới (optional)
    """
    try:
        return service.update_section(section_id, section_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi cập nhật section: {str(e)}"
        )

@router.delete("/{section_id}", status_code=status.HTTP_200_OK)
@router.delete("/{section_id}/", status_code=status.HTTP_200_OK, include_in_schema=False)
def delete_section(
    section_id: int,
    service: SectionService = Depends(get_section_service)
):
    """
    Xóa một Section theo ID.
    
    - **section_id**: ID của Section cần xóa
    """
    try:
        return service.delete_section(section_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi xóa section: {str(e)}"
        )
