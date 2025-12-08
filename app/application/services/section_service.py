from typing import List, Optional
from fastapi import HTTPException, status
from app.domain.models import Section, Topic
from app.domain.schemas.section_schema import SectionCreate, SectionUpdate, SectionResponse
from app.application.interfaces.section_repository_interface import ISectionRepository

class SectionService:
    """
    Service layer xử lý business logic cho Section.
    Áp dụng Dependency Inversion: phụ thuộc vào ISectionRepository interface thay vì concrete class.
    """
    
    def __init__(self, section_repository: ISectionRepository, topic_repository=None):
        """
        Khởi tạo service với repository dependency.
        
        Args:
            section_repository: Implementation của ISectionRepository
            topic_repository: Optional - để validate topic_id
        """
        self.section_repository = section_repository
        self.topic_repository = topic_repository
    
    def create_section(self, section_data: SectionCreate) -> SectionResponse:
        """
        Tạo mới Section với validation.
        
        Args:
            section_data: Dữ liệu Section cần tạo
            
        Returns:
            SectionResponse đã được tạo
            
        Raises:
            HTTPException: Nếu topic_id không tồn tại
        """
        # Validate topic exists nếu có topic_repository
        if self.topic_repository:
            topic = self.topic_repository.get_by_id(section_data.topic_id)
            if not topic:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Topic with id {section_data.topic_id} not found"
                )
        
        # Tạo Section entity từ schema
        section = Section(
            topic_id=section_data.topic_id,
            heading=section_data.heading,
            content=section_data.content,
            image_url=section_data.image_url,
            code_snippet=section_data.code_snippet,
            language=section_data.language,
            order_index=section_data.order_index
        )
        
        # Lưu vào database
        created_section = self.section_repository.create(section)
        
        # Convert sang response schema
        return SectionResponse.model_validate(created_section)
    
    def get_section_by_id(self, section_id: int) -> SectionResponse:
        """
        Lấy Section theo ID.
        
        Args:
            section_id: ID của Section cần tìm
            
        Returns:
            SectionResponse
            
        Raises:
            HTTPException: Nếu Section không tồn tại
        """
        section = self.section_repository.get_by_id(section_id)
        if not section:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Section with id {section_id} not found"
            )
        
        return SectionResponse.model_validate(section)
    
    def get_all_sections(self, skip: int = 0, limit: int = 100) -> List[SectionResponse]:
        """
        Lấy danh sách tất cả Sections với phân trang.
        
        Args:
            skip: Số lượng bản ghi bỏ qua
            limit: Số lượng bản ghi tối đa
            
        Returns:
            Danh sách SectionResponse
        """
        sections = self.section_repository.get_all(skip=skip, limit=limit)
        return [SectionResponse.model_validate(section) for section in sections]
    
    def get_sections_by_topic(self, topic_id: int) -> List[SectionResponse]:
        """
        Lấy tất cả Sections thuộc về một Topic.
        
        Args:
            topic_id: ID của Topic
            
        Returns:
            Danh sách SectionResponse sắp xếp theo order_index
        """
        sections = self.section_repository.get_by_topic_id(topic_id)
        return [SectionResponse.model_validate(section) for section in sections]
    
    def update_section(self, section_id: int, section_data: SectionUpdate) -> SectionResponse:
        """
        Cập nhật Section.
        
        Args:
            section_id: ID của Section cần cập nhật
            section_data: Dữ liệu cập nhật
            
        Returns:
            SectionResponse sau khi cập nhật
            
        Raises:
            HTTPException: Nếu Section không tồn tại hoặc topic_id không hợp lệ
        """
        # Kiểm tra section tồn tại
        existing_section = self.section_repository.get_by_id(section_id)
        if not existing_section:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Section with id {section_id} not found"
            )
        
        # Validate topic_id nếu có thay đổi
        if section_data.topic_id and self.topic_repository:
            topic = self.topic_repository.get_by_id(section_data.topic_id)
            if not topic:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Topic with id {section_data.topic_id} not found"
                )
        
        # Chỉ lấy các field không None để cập nhật
        update_data = section_data.model_dump(exclude_unset=True)
        
        # Cập nhật trong database
        updated_section = self.section_repository.update(section_id, update_data)
        
        return SectionResponse.model_validate(updated_section)
    
    def delete_section(self, section_id: int) -> dict:
        """
        Xóa Section.
        
        Args:
            section_id: ID của Section cần xóa
            
        Returns:
            Dictionary thông báo kết quả
            
        Raises:
            HTTPException: Nếu Section không tồn tại
        """
        success = self.section_repository.delete(section_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Section with id {section_id} not found"
            )
        
        return {"message": f"Section with id {section_id} deleted successfully"}
