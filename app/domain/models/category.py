from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base

class Category(Base):
    """
    Phân loại kiến thức (Tiêu chí tra cứu 2: Khái niệm, Tính chất, Bài tập...)
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)

    # Quan hệ 1-N: Một Category có nhiều Topics
    topics = relationship("Topic", back_populates="category")
