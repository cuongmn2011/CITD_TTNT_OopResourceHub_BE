from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.models import Section
from app.domain.schemas.section_schema import SectionCreate
from app.application.interfaces.section_repository_interface import ISectionRepository

class SectionRepository(ISectionRepository):
    """
    Implementation của ISectionRepository sử dụng SQLAlchemy ORM.
    Xử lý tất cả các thao tác database liên quan đến Section.
    """
    
    def __init__(self, db: Session):
        """
        Khởi tạo repository với database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    def create(self, section: Section) -> Section:
        """Tạo mới Section trong database"""
        self.db.add(section)
        self.db.commit()
        self.db.refresh(section)
        return section
    
    def get_by_id(self, section_id: int) -> Optional[Section]:
        """Lấy Section theo ID"""
        return self.db.query(Section).filter(Section.id == section_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Section]:
        """Lấy danh sách tất cả Sections với phân trang"""
        return self.db.query(Section)\
            .order_by(Section.topic_id, Section.order_index)\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def get_by_topic_id(self, topic_id: int) -> List[Section]:
        """Lấy tất cả Sections thuộc về một Topic, sắp xếp theo order_index"""
        return self.db.query(Section)\
            .filter(Section.topic_id == topic_id)\
            .order_by(Section.order_index)\
            .all()
    
    def update(self, section_id: int, section_data: dict) -> Optional[Section]:
        """
        Cập nhật Section. Chỉ cập nhật các field được cung cấp trong section_data.
        """
        section = self.get_by_id(section_id)
        if not section:
            return None
        
        # Cập nhật từng field nếu có trong section_data
        for key, value in section_data.items():
            if hasattr(section, key) and value is not None:
                setattr(section, key, value)
        
        self.db.commit()
        self.db.refresh(section)
        return section
    
    def delete(self, section_id: int) -> bool:
        """Xóa Section theo ID"""
        section = self.get_by_id(section_id)
        if not section:
            return False
        
        self.db.delete(section)
        self.db.commit()
        return True
