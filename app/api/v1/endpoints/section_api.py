from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.core.database import get_db
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
    return service.create_section(section_data)

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
    return service.get_all_sections(skip=skip, limit=limit)

@router.get("/topic/{topic_id}", response_model=List[SectionResponse])
def get_sections_by_topic(
    topic_id: int,
    service: SectionService = Depends(get_section_service)
):
    """
    Lấy tất cả Sections thuộc về một Topic, sắp xếp theo order_index.
    
    - **topic_id**: ID của Topic cần lấy sections
    """
    return service.get_sections_by_topic(topic_id)

@router.get("/{section_id}", response_model=SectionResponse)
def get_section_by_id(
    section_id: int,
    service: SectionService = Depends(get_section_service)
):
    """
    Lấy thông tin chi tiết một Section theo ID.
    
    - **section_id**: ID của Section cần lấy
    """
    return service.get_section_by_id(section_id)

@router.put("/{section_id}", response_model=SectionResponse)
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
    return service.update_section(section_id, section_data)

@router.delete("/{section_id}", status_code=status.HTTP_200_OK)
def delete_section(
    section_id: int,
    service: SectionService = Depends(get_section_service)
):
    """
    Xóa một Section theo ID.
    
    - **section_id**: ID của Section cần xóa
    """
    return service.delete_section(section_id)
