from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime
# Import Base từ file database.py nằm ở thư mục gốc
from core.database import Base

# Bảng trung gian cho quan hệ Many-to-Many (Self-referencing) của Topic
# Dùng để lưu trữ các bài học liên quan (Tiêu chí tra cứu 3)
related_topics_association = Table(
    'related_topics',
    Base.metadata,
    Column('source_id', Integer, ForeignKey('topics.id'), primary_key=True),
    Column('related_id', Integer, ForeignKey('topics.id'), primary_key=True)
)

class Category(Base):
    """
    Phân loại kiến thức (Tiêu chí tra cứu 2: Khái niệm, Tính chất, Bài tập...)
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True) # ID tự động
    name = Column(String, unique=True, index=True, nullable=False) # Tên danh mục
    slug = Column(String, unique=True, index=True, nullable=False)# Chuỗi đã chuẩn hóa: viết thường, không dấu, nối bằng gạch ngang.

    # Quan hệ 1-N: Một Category có nhiều Topics
    topics = relationship("Topic", back_populates="category")

class Topic(Base):
    """
    Bài học chính (Tiêu chí tra cứu 1)
    """
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    short_definition = Column(Text, nullable=True) # Định nghĩa ngắn gọn
    created_at = Column(DateTime, default=datetime.utcnow)
    
    category_id = Column(Integer, ForeignKey("categories.id"))

    # Quan hệ N-1: Topic thuộc về 1 Category
    category = relationship("Category", back_populates="topics")

    # Quan hệ 1-N: Topic chứa nhiều thành phần chi tiết (Sections)
    # cascade="all, delete-orphan": Xóa Topic sẽ xóa luôn các Section con
    sections = relationship("Section", back_populates="topic", cascade="all, delete-orphan")

    # Quan hệ N-N (Self-referencing): Các bài học liên quan
    related_topics = relationship(
        "Topic",
        secondary=related_topics_association,
        primaryjoin=id==related_topics_association.c.source_id,
        secondaryjoin=id==related_topics_association.c.related_id,
        backref="linked_by", # Giúp truy vấn ngược: Topic này được link bởi những bài nào
        lazy="select"
    )

class Section(Base):
    """
    Thành phần chi tiết để hiển thị (Heading, Code, Image...)
    """
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    
    order_index = Column(Integer, default=0)      # Thứ tự hiển thị
    heading = Column(String, nullable=True)       # Tên mục con
    content = Column(Text, nullable=True)         # Nội dung giải thích
    image_url = Column(String, nullable=True)     # Link ảnh minh họa
    code_snippet = Column(Text, nullable=True)    # Code mẫu
    language = Column(String, default="c#")       # Ngôn ngữ code (mặc định C#)

    # Quan hệ N-1: Section thuộc về Topic
    topic = relationship("Topic", back_populates="sections")