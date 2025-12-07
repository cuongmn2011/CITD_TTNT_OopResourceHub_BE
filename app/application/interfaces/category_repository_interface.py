from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.document_model import Category
from app.domain.schemas.category_schema import CategoryCreate, CategoryUpdate

class ICategoryRepository(ABC):
    """
    Interface định nghĩa các phương thức mà Category Repository phải implement.
    Áp dụng Dependency Inversion Principle.
    """
    
    @abstractmethod
    def create(self, category_data: CategoryCreate) -> Category:
        """
        Tạo category mới
        
        Args:
            category_data: Dữ liệu category cần tạo
            
        Returns:
            Category: Category object đã được tạo
        """
        pass
    
    @abstractmethod
    def get_by_id(self, category_id: int) -> Optional[Category]:
        """
        Lấy category theo ID
        
        Args:
            category_id: ID của category
            
        Returns:
            Optional[Category]: Category object hoặc None
        """
        pass
    
    @abstractmethod
    def get_by_slug(self, slug: str) -> Optional[Category]:
        """
        Lấy category theo slug (để check trùng)
        
        Args:
            slug: Slug của category
            
        Returns:
            Optional[Category]: Category object hoặc None
        """
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Category]:
        """
        Lấy danh sách categories với phân trang
        
        Args:
            skip: Số bản ghi bỏ qua
            limit: Số bản ghi tối đa trả về
            
        Returns:
            List[Category]: Danh sách categories
        """
        pass
    
    @abstractmethod
    def update(self, category_id: int, category_data: CategoryUpdate) -> Optional[Category]:
        """
        Cập nhật category
        
        Args:
            category_id: ID của category cần cập nhật
            category_data: Dữ liệu cập nhật
            
        Returns:
            Optional[Category]: Category đã cập nhật hoặc None
        """
        pass
    
    @abstractmethod
    def delete(self, category_id: int) -> bool:
        """
        Xóa category
        
        Args:
            category_id: ID của category cần xóa
            
        Returns:
            bool: True nếu xóa thành công, False nếu không tìm thấy
        """
        pass
