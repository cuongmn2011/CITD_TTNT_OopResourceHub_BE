from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.models import Category
from app.domain.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.application.interfaces.category_repository_interface import ICategoryRepository

class CategoryRepository(ICategoryRepository):
    """
    Implementation của ICategoryRepository sử dụng SQLAlchemy ORM.
    Xử lý tất cả các thao tác database liên quan đến Category.
    """
    
    def __init__(self, db: Session):
        self.db = db

    def create(self, category_data: CategoryCreate) -> Category:
        """Tạo category mới"""
        new_category = Category(
            name=category_data.name,
            slug=category_data.slug
        )
        self.db.add(new_category)
        self.db.commit()
        self.db.refresh(new_category)
        return new_category
    
    def get_by_id(self, category_id: int) -> Optional[Category]:
        """Lấy category theo ID"""
        return self.db.query(Category).filter(Category.id == category_id).first()
    
    def get_by_slug(self, slug: str) -> Optional[Category]:
        """Lấy category theo slug"""
        return self.db.query(Category).filter(Category.slug == slug).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Category]:
        """Lấy danh sách categories với phân trang"""
        return self.db.query(Category).offset(skip).limit(limit).all()
    
    def update(self, category_id: int, category_data: CategoryUpdate) -> Optional[Category]:
        """Cập nhật category"""
        category = self.get_by_id(category_id)
        if not category:
            return None
        
        # Chỉ cập nhật các trường được cung cấp
        if category_data.name is not None:
            category.name = category_data.name
        if category_data.slug is not None:
            category.slug = category_data.slug
        
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def delete(self, category_id: int) -> bool:
        """Xóa category"""
        category = self.get_by_id(category_id)
        if not category:
            return False
        
        self.db.delete(category)
        self.db.commit()
        return True
