from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.domain.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryResponse
from app.application.services.category_service import CategoryService
from app.infrastructure.repositories.category_repository import CategoryRepository

router = APIRouter()

# Dependency để tạo service với repository injection
def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    """
    Dependency injection: tạo CategoryService với CategoryRepository
    Tuân thủ Dependency Inversion Principle
    """
    category_repo = CategoryRepository(db)
    return CategoryService(category_repo)

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_in: CategoryCreate, 
    service: CategoryService = Depends(get_category_service)
):
    """
    Tạo category mới
    
    - **name**: Tên category (VD: Khái niệm, Tính chất, Bài tập...)
    - **slug**: Slug chuẩn hóa (VD: khai-niem, tinh-chat, bai-tap...)
    """
    return service.create_category(category_in)

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int, 
    service: CategoryService = Depends(get_category_service)
):
    """Lấy thông tin chi tiết một category"""
    category = service.get_category_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Category với ID {category_id} không tồn tại"
        )
    return category

@router.get("/", response_model=List[CategoryResponse])
def get_categories(
    skip: int = 0,
    limit: int = 100,
    service: CategoryService = Depends(get_category_service)
):
    """Lấy danh sách categories với phân trang"""
    return service.get_all_categories(skip=skip, limit=limit)

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_in: CategoryUpdate,
    service: CategoryService = Depends(get_category_service)
):
    """Cập nhật category"""
    category = service.update_category(category_id, category_in)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category với ID {category_id} không tồn tại"
        )
    return category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service)
):
    """Xóa category"""
    success = service.delete_category(category_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category với ID {category_id} không tồn tại"
        )
    return None
