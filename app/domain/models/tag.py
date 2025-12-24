from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base

# Bảng N-N giữa Topic và Tag
topic_tags = Table(
    "topic_tags",
    Base.metadata,
    Column("topic_id", Integer, ForeignKey("topics.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class Tag(Base):
    """
    Tags để phân loại và tìm kiếm topics dễ dàng hơn
    Ví dụ: "design-pattern", "solid", "oop-basics", "best-practices"
    """
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    # Quan hệ N-N: Tag có nhiều Topics, Topic có nhiều Tags
    topics = relationship(
        "Topic",
        secondary=topic_tags,
        back_populates="tags"
    )
