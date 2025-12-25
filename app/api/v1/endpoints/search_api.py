from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.application.services.search_service import SearchService
from app.domain.schemas.search_schema import SearchResponse
from app.infrastructure.database import get_db

router = APIRouter()


def get_search_service(db: Session = Depends(get_db)) -> SearchService:
    """Dependency injection cho SearchService"""
    return SearchService(db)


@router.get("/", response_model=SearchResponse)
@router.get("", response_model=SearchResponse, include_in_schema=False)
def search(
    q: str = Query(..., min_length=1, description="Từ khóa tìm kiếm"),
    limit: int = Query(20, ge=1, le=50, description="Số lượng kết quả tối đa cho mỗi loại"),
    tags: str = Query(None, description="Danh sách tag IDs ngăn cách bởi dấu phẩy (VD: '1,2,3')"),
    service: SearchService = Depends(get_search_service),
):
    """
    Tìm kiếm topics, sections, categories với fuzzy matching.
    
    **Fuzzy Matching**: Hỗ trợ tìm kiếm gần đúng, bỏ qua dấu tiếng Việt.
    
    **Ví dụ**:
    - Query: "Làm sao để hiểu OOP" → Tìm topics có chứa "OOP"
    - Query: "ke thua" → Tìm "Kế thừa", "Inheritance"
    - Query: "class object" → Tìm topics liên quan đến class và object
    - Tags: "1,2" → Chỉ tìm topics có tag ID 1 hoặc 2
    
    **Scoring**: Kết quả được xếp hạng theo độ liên quan:
    - Exact match: 1.0
    - Starts with: 0.9
    - Contains: 0.7
    - Fuzzy match: 0.3-0.6
    
    Args:
        q: Từ khóa tìm kiếm (bắt buộc)
        limit: Số lượng kết quả tối đa cho mỗi loại (1-50, mặc định 20)
        tags: Filter theo tags (optional, VD: "1,2,3")
    
    Returns:
        SearchResponse chứa topics, sections, categories phù hợp
    """
    # Parse tag IDs
    tag_ids = None
    if tags:
        try:
            tag_ids = [int(tid.strip()) for tid in tags.split(',') if tid.strip()]
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Tag IDs phải là số nguyên, ngăn cách bởi dấu phẩy"
            )
    
    return service.search(query=q, limit=limit, tag_ids=tag_ids)
