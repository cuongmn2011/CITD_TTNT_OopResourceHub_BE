"""
Custom exception classes for the application.
Extends FastAPI's HTTPException with domain-specific errors.
"""
from fastapi import HTTPException, status

class ResourceNotFoundException(HTTPException):
    """Raised when a requested resource is not found"""
    def __init__(self, resource_name: str, resource_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource_name} với ID {resource_id} không tồn tại"
        )

class DuplicateResourceException(HTTPException):
    """Raised when trying to create a resource that already exists"""
    def __init__(self, resource_name: str, field: str, value: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{resource_name} với {field} '{value}' đã tồn tại"
        )

class ValidationException(HTTPException):
    """Raised when business validation fails"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )
