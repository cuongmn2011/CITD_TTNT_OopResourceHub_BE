from typing import List
from fastapi import HTTPException, status
from app.application.interfaces.tag_repository_interface import ITagRepository
from app.domain.schemas.tag_schema import TagCreate, TagUpdate, TagResponse, TagWithTopics


class TagService:
    """
    Service xử lý business logic cho Tags.
    Áp dụng Dependency Inversion: phụ thuộc vào ITagRepository interface.
    """

    def __init__(self, tag_repo: ITagRepository):
        self.tag_repo = tag_repo

    def get_all_tags(self, skip: int = 0, limit: int = 100) -> List[TagResponse]:
        """Lấy tất cả tags"""
        tags = self.tag_repo.get_all(skip, limit)
        return [
            TagResponse(
                id=tag.id,
                name=tag.name,
                slug=tag.slug,
                description=tag.description,
                topic_count=len(tag.topics) if tag.topics else 0
            )
            for tag in tags
        ]

    def get_tag_by_id(self, tag_id: int) -> TagWithTopics:
        """Lấy tag theo ID kèm topic IDs"""
        tag = self.tag_repo.get_by_id(tag_id)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tag với ID {tag_id} không tồn tại"
            )

        return TagWithTopics(
            id=tag.id,
            name=tag.name,
            slug=tag.slug,
            description=tag.description,
            topic_count=len(tag.topics) if tag.topics else 0,
            topic_ids=[t.id for t in tag.topics] if tag.topics else []
        )

    def create_tag(self, tag_data: TagCreate) -> TagResponse:
        """Tạo tag mới"""
        # Check duplicate
        existing = self.tag_repo.get_by_slug(tag_data.slug)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tag với slug '{tag_data.slug}' đã tồn tại"
            )

        tag = self.tag_repo.create(tag_data)
        return TagResponse(
            id=tag.id,
            name=tag.name,
            slug=tag.slug,
            description=tag.description,
            topic_count=0
        )

    def update_tag(self, tag_id: int, tag_data: TagUpdate) -> TagResponse:
        """Cập nhật tag"""
        tag = self.tag_repo.update(tag_id, tag_data)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tag với ID {tag_id} không tồn tại"
            )

        return TagResponse(
            id=tag.id,
            name=tag.name,
            slug=tag.slug,
            description=tag.description,
            topic_count=len(tag.topics) if tag.topics else 0
        )

    def delete_tag(self, tag_id: int) -> bool:
        """Xóa tag"""
        success = self.tag_repo.delete(tag_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tag với ID {tag_id} không tồn tại"
            )
        return True

    def get_popular_tags(self, limit: int = 10) -> List[TagResponse]:
        """Lấy các tags phổ biến nhất"""
        results = self.tag_repo.get_popular_tags(limit)
        return [
            TagResponse(
                id=tag.id,
                name=tag.name,
                slug=tag.slug,
                description=tag.description,
                topic_count=count
            )
            for tag, count in results
        ]
