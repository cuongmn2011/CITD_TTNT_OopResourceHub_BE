from typing import List, Optional
from fastapi import HTTPException, status
from app.application.interfaces.category_repository_interface import ICategoryRepository
from app.domain.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryResponse

class CategoryService:
    """
    Service layer xử lý business logic cho Category.
    Áp dụng Dependency Inversion: phụ thuộc vào ICategoryRepository interface.
    """
    
    def __init__(self, category_repo: ICategoryRepository):
        """
        Constructor nhận interface thay vì Session để tuân thủ DIP
        
        Args:
            category_repo: Implementation của ICategoryRepository
        """
        self.category_repo = category_repo

    def create_category(self, data: CategoryCreate) -> CategoryResponse:
        """
        Tạo category mới
        
        Business logic:
        - Kiểm tra slug đã tồn tại chưa
        """
        # Kiểm tra slug đã tồn tại
        existing = self.category_repo.get_by_slug(data.slug)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category với slug '{data.slug}' đã tồn tại"
            )
        
        category = self.category_repo.create(data)
        return CategoryResponse.model_validate(category)
    
    def get_category_by_id(self, category_id: int) -> Optional[CategoryResponse]:
        """Lấy category theo ID"""
        category = self.category_repo.get_by_id(category_id)
        if category:
            return CategoryResponse.model_validate(category)
        return None
    
    def get_all_categories(self, skip: int = 0, limit: int = 100) -> List[CategoryResponse]:
        """Lấy danh sách categories"""
        categories = self.category_repo.get_all(skip, limit)
        return [CategoryResponse.model_validate(cat) for cat in categories]
    
    def update_category(self, category_id: int, data: CategoryUpdate) -> Optional[CategoryResponse]:
        """
        Cập nhật category
        
        Business logic:
        - Nếu update slug, kiểm tra slug mới có trùng không
        """
        # Nếu update slug, kiểm tra trùng
        if data.slug is not None:
            existing = self.category_repo.get_by_slug(data.slug)
            if existing and existing.id != category_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Category với slug '{data.slug}' đã tồn tại"
                )
        
        category = self.category_repo.update(category_id, data)
        if category:
            return CategoryResponse.model_validate(category)
        return None
    
    def delete_category(self, category_id: int) -> bool:
        """Xóa category"""
        return self.category_repo.delete(category_id)
