from typing import List, Optional
from sqlalchemy.orm import Session
from app.application.interfaces.tag_repository_interface import ITagRepository
from app.domain.models.tag import Tag
from app.domain.schemas.tag_schema import TagCreate, TagUpdate


class TagRepository(ITagRepository):
    """
    Repository cho Tag operations.
    Implements ITagRepository interface.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Tag]:
        """Lấy tất cả tags"""
        return self.db.query(Tag).offset(skip).limit(limit).all()

    def get_by_id(self, tag_id: int) -> Optional[Tag]:
        """Lấy tag theo ID"""
        return self.db.query(Tag).filter(Tag.id == tag_id).first()

    def get_by_slug(self, slug: str) -> Optional[Tag]:
        """Lấy tag theo slug"""
        return self.db.query(Tag).filter(Tag.slug == slug).first()

    def get_by_name(self, name: str) -> Optional[Tag]:
        """Lấy tag theo name"""
        return self.db.query(Tag).filter(Tag.name == name).first()
    def search_by_name(self, name: str) -> List[Tag]:
        """
        Tìm kiếm tags theo tên (có chứa chuỗi name, không phân biệt hoa thường)
        Implement phương thức abstract từ ITagRepository
        """
        # Sử dụng ilike để tìm kiếm gần đúng và không phân biệt hoa thường
        return self.db.query(Tag).filter(Tag.name.ilike(f"%{name}%")).all()
    def create(self, tag_data: TagCreate) -> Tag:
        """Tạo tag mới"""
        tag = Tag(**tag_data.model_dump())
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag

    def update(self, tag_id: int, tag_data: TagUpdate) -> Optional[Tag]:
        """Cập nhật tag"""
        tag = self.get_by_id(tag_id)
        if not tag:
            return None

        update_data = tag_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(tag, key, value)

        self.db.commit()
        self.db.refresh(tag)
        return tag

    def delete(self, tag_id: int) -> bool:
        """Xóa tag"""
        tag = self.get_by_id(tag_id)
        if not tag:
            return False

        self.db.delete(tag)
        self.db.commit()
        return True

    def get_popular_tags(self, limit: int = 10) -> List[tuple[Tag, int]]:
        """Lấy các tags phổ biến nhất (có nhiều topics nhất)"""
        from app.domain.models.topic import Topic
        from app.domain.models.tag import topic_tags
        from sqlalchemy import func

        results = (
            self.db.query(Tag, func.count(topic_tags.c.topic_id).label('topic_count'))
            .join(topic_tags, Tag.id == topic_tags.c.tag_id)
            .group_by(Tag.id)
            .order_by(func.count(topic_tags.c.topic_id).desc())
            .limit(limit)
            .all()
        )
        return results
