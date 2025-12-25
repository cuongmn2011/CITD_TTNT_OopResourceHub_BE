from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.tag import Tag


class ITagRepository(ABC):
    """
    Interface cho Tag Repository.
    Định nghĩa contract cho việc tương tác với Tag data store.
    Áp dụng Dependency Inversion Principle.
    """

    @abstractmethod
    def create(self, tag_data) -> Tag:
        """
        Tạo tag mới
        
        Args:
            tag_data: Dữ liệu tag (TagCreate schema)
            
        Returns:
            Tag entity đã được tạo
        """
        pass

    @abstractmethod
    def get_by_id(self, tag_id: int) -> Optional[Tag]:
        """
        Lấy tag theo ID
        
        Args:
            tag_id: ID của tag
            
        Returns:
            Tag entity hoặc None nếu không tìm thấy
        """
        pass

    @abstractmethod
    def get_by_slug(self, slug: str) -> Optional[Tag]:
        """
        Lấy tag theo slug
        
        Args:
            slug: Slug của tag
            
        Returns:
            Tag entity hoặc None nếu không tìm thấy
        """
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Tag]:
        """
        Lấy tag theo tên chính xác
        
        Args:
            name: Tên của tag
            
        Returns:
            Tag entity hoặc None nếu không tìm thấy
        """
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Tag]:
        """
        Lấy danh sách tất cả tags với phân trang
        
        Args:
            skip: Số lượng records bỏ qua
            limit: Số lượng records tối đa trả về
            
        Returns:
            Danh sách Tag entities
        """
        pass

    @abstractmethod
    def update(self, tag_id: int, tag_data) -> Optional[Tag]:
        """
        Cập nhật tag
        
        Args:
            tag_id: ID của tag cần cập nhật
            tag_data: Dữ liệu cập nhật (TagUpdate schema)
            
        Returns:
            Tag entity đã được cập nhật hoặc None nếu không tìm thấy
        """
        pass

    @abstractmethod
    def delete(self, tag_id: int) -> bool:
        """
        Xóa tag
        
        Args:
            tag_id: ID của tag cần xóa
            
        Returns:
            True nếu xóa thành công, False nếu không tìm thấy
        """
        pass

    @abstractmethod
    def search_by_name(self, name: str) -> List[Tag]:
        """
        Tìm kiếm tags theo tên
        
        Args:
            name: Tên hoặc một phần tên của tag
            
        Returns:
            Danh sách Tag entities phù hợp
        """
        pass

    @abstractmethod
    def get_popular_tags(self, limit: int = 10) -> List[tuple]:
        """
        Lấy các tags phổ biến nhất (có nhiều topics nhất)
        
        Args:
            limit: Số lượng tags tối đa trả về
            
        Returns:
            Danh sách tuple (Tag, topic_count) được sắp xếp theo số lượng topics giảm dần
        """
        pass
