from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.domain.models import Topic, Section, Tag
from app.domain.schemas.topic_schema import TopicCreate
from app.application.interfaces.topic_repository_interface import ITopicRepository

class TopicRepository(ITopicRepository):
    """
    Implementation của ITopicRepository sử dụng SQLAlchemy ORM.
    Xử lý tất cả các thao tác database liên quan đến Topic.
    """
    
    def __init__(self, db: Session):
        self.db = db

    def create(self, topic_data: TopicCreate) -> Topic:
        """Tạo topic mới kèm theo các sections và tags"""
        # 1. Tạo Topic
        new_topic = Topic(
            title=topic_data.title,
            short_definition=topic_data.short_definition,
            category_id=topic_data.category_id
        )
        self.db.add(new_topic)
        self.db.flush() # Flush để lấy new_topic.id trước khi commit

        # 2. Gắn tags (nếu có)
        if topic_data.tag_ids:
            tags = self.db.query(Tag).filter(Tag.id.in_(topic_data.tag_ids)).all()
            new_topic.tags = tags

        # 3. Tạo các Section con (nếu có)
        for section_data in topic_data.sections:
            new_section = Section(
                **section_data.model_dump(), # Convert pydantic model sang dict
                topic_id=new_topic.id
            )
            self.db.add(new_section)

        self.db.commit()
        self.db.refresh(new_topic)
        return new_topic
    
    def get_by_id(self, topic_id: int) -> Optional[Topic]:
        """Lấy topic theo ID với eager loading sections và tags"""
        return self.db.query(Topic)\
            .options(joinedload(Topic.sections), joinedload(Topic.tags))\
            .filter(Topic.id == topic_id)\
            .first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Topic]:
        """Lấy danh sách topics với phân trang và eager loading sections"""
        return self.db.query(Topic)\
            .options(joinedload(Topic.sections))\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def get_by_category(self, category_id: int, skip: int = 0, limit: int = 100) -> List[Topic]:
        """Lấy danh sách topics theo category (load tags cho filtering, không load sections)"""
        return self.db.query(Topic)\
            .options(joinedload(Topic.tags))\
            .filter(Topic.category_id == category_id)\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def update(self, topic_id: int, topic_data: TopicCreate) -> Optional[Topic]:
        """Cập nhật topic"""
        topic = self.get_by_id(topic_id)
        if not topic:
            return None
        
        # Cập nhật các trường cơ bản
        topic.title = topic_data.title
        topic.short_definition = topic_data.short_definition
        topic.category_id = topic_data.category_id
        
        # Cập nhật tags
        if topic_data.tag_ids:
            tags = self.db.query(Tag).filter(Tag.id.in_(topic_data.tag_ids)).all()
            topic.tags = tags
        else:
            topic.tags = []
        
        # Xóa sections cũ và tạo mới (simple approach)
        for section in topic.sections:
            self.db.delete(section)
        
        # Tạo sections mới
        for section_data in topic_data.sections:
            new_section = Section(
                **section_data.model_dump(),
                topic_id=topic.id
            )
            self.db.add(new_section)
        
        self.db.commit()
        self.db.refresh(topic)
        return topic
    
    def delete(self, topic_id: int) -> bool:
        """Xóa topic (cascade sẽ tự động xóa sections)"""
        topic = self.get_by_id(topic_id)
        if not topic:
            return False
        
        self.db.delete(topic)
        self.db.commit()
        return True    
    def get_all_with_minimal_data(self) -> List[Topic]:
        """Lấy tất cả topics không load sections (dùng cho việc tính toán related topics)"""
        return self.db.query(Topic).all()
