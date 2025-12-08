from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models import Topic
from app.domain.schemas.topic_schema import TopicCreate

class ITopicRepository(ABC):
    """
    Interface định nghĩa các phương thức mà Topic Repository phải implement.
    Áp dụng Dependency Inversion Principle - phụ thuộc vào abstraction thay vì concrete class.
    """
    
    @abstractmethod
    def create(self, topic_data: TopicCreate) -> Topic:
        """
        Tạo topic mới trong database
        
        Args:
            topic_data: Dữ liệu topic cần tạo
            
        Returns:
            Topic: Topic object đã được tạo
        """
        pass
    
    @abstractmethod
    def get_by_id(self, topic_id: int) -> Optional[Topic]:
        """
        Lấy topic theo ID
        
        Args:
            topic_id: ID của topic
            
        Returns:
            Optional[Topic]: Topic object hoặc None nếu không tìm thấy
        """
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Topic]:
        """
        Lấy danh sách topics với phân trang
        
        Args:
            skip: Số bản ghi bỏ qua
            limit: Số bản ghi tối đa trả về
            
        Returns:
            List[Topic]: Danh sách topics
        """
        pass
    
    @abstractmethod
    def update(self, topic_id: int, topic_data: TopicCreate) -> Optional[Topic]:
        """
        Cập nhật topic
        
        Args:
            topic_id: ID của topic cần cập nhật
            topic_data: Dữ liệu mới
            
        Returns:
            Optional[Topic]: Topic đã cập nhật hoặc None nếu không tìm thấy
        """
        pass
    
    @abstractmethod
    def delete(self, topic_id: int) -> bool:
        """
        Xóa topic
        
        Args:
            topic_id: ID của topic cần xóa
            
        Returns:
            bool: True nếu xóa thành công, False nếu không tìm thấy
        """
        pass