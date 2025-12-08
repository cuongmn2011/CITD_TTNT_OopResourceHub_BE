from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Section(Base):
    """
    Phần nội dung chi tiết của một Topic (Tiêu chí tra cứu 3: Giải thích, Ví dụ, Lưu ý...)
    """
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    order_index = Column(Integer, nullable=False)  # Thứ tự hiển thị section
    heading = Column(String, nullable=False)  # Tiêu đề nhỏ (e.g., "Định nghĩa", "Ví dụ", "Ưu điểm")
    content = Column(Text, nullable=False)  # Nội dung chi tiết
    image_url = Column(String, nullable=True)  # Đường dẫn hình minh họa
    code_snippet = Column(Text, nullable=True)  # Đoạn code minh họa
    language = Column(String, nullable=True)  # Ngôn ngữ code (Python, C#, Java...)

    # Quan hệ N-1: Nhiều Sections thuộc về 1 Topic
    topic = relationship("Topic", back_populates="sections")
