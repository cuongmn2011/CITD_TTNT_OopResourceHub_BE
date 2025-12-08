from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models import Section

class ISectionRepository(ABC):
    """
    Interface cho Section Repository (Dependency Inversion Principle).
    Định nghĩa contract cho các thao tác CRUD với Section.
    """
    
    @abstractmethod
    def create(self, section: Section) -> Section:
        """
        Tạo mới một Section.
        
        Args:
            section: Section entity cần tạo
            
        Returns:
            Section đã được tạo với ID
        """
        pass
    
    @abstractmethod
    def get_by_id(self, section_id: int) -> Optional[Section]:
        """
        Lấy Section theo ID.
        
        Args:
            section_id: ID của Section cần tìm
            
        Returns:
            Section nếu tìm thấy, None nếu không tìm thấy
        """
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Section]:
        """
        Lấy danh sách tất cả Sections với phân trang.
        
        Args:
            skip: Số lượng bản ghi bỏ qua
            limit: Số lượng bản ghi tối đa trả về
            
        Returns:
            Danh sách Section
        """
        pass
    
    @abstractmethod
    def get_by_topic_id(self, topic_id: int) -> List[Section]:
        """
        Lấy tất cả Sections thuộc về một Topic, sắp xếp theo order_index.
        
        Args:
            topic_id: ID của Topic
            
        Returns:
            Danh sách Section của Topic, sắp xếp theo thứ tự
        """
        pass
    
    @abstractmethod
    def update(self, section_id: int, section_data: dict) -> Optional[Section]:
        """
        Cập nhật thông tin Section.
        
        Args:
            section_id: ID của Section cần cập nhật
            section_data: Dictionary chứa dữ liệu cần cập nhật
            
        Returns:
            Section sau khi cập nhật, None nếu không tìm thấy
        """
        pass
    
    @abstractmethod
    def delete(self, section_id: int) -> bool:
        """
        Xóa Section theo ID.
        
        Args:
            section_id: ID của Section cần xóa
            
        Returns:
            True nếu xóa thành công, False nếu không tìm thấy
        """
        pass
