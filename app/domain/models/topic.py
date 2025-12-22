from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from app.infrastructure.database import Base

# Bảng phụ N-N cho quan hệ self-referencing giữa các Topic (related topics)
related_topics_association = Table(
    "related_topics_association",
    Base.metadata,
    Column("topic_id", Integer, ForeignKey("topics.id"), primary_key=True),
    Column("related_topic_id", Integer, ForeignKey("topics.id"), primary_key=True),
)


class Topic(Base):
    """
    Chủ đề chính OOP (Tiêu chí tra cứu 1: Class, Object, Inheritance, Polymorphism...)
    """

    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    short_definition = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Khóa ngoại tham chiếu đến Category
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    # Quan hệ N-1: Nhiều Topics thuộc về 1 Category
    category = relationship("Category", back_populates="topics")

    # Quan hệ 1-N: Một Topic có nhiều Sections
    sections = relationship(
        "Section", back_populates="topic", cascade="all, delete-orphan"
    )

    # Quan hệ N-N tự tham chiếu: Các Topics liên quan
    related_topics = relationship(
        "Topic",
        secondary=related_topics_association,
        primaryjoin=id == related_topics_association.c.topic_id,
        secondaryjoin=id == related_topics_association.c.related_topic_id,
        backref="related_by",
    )
