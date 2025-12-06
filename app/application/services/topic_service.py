from typing import List, Optional
from app.application.interfaces.topic_repository_interface import ITopicRepository
from app.domain.models.document_model import Topic
from app.domain.schemas.topic_schema import TopicCreate, TopicResponse

class TopicService:
    """
    Service layer xử lý business logic cho Topic.
    Áp dụng Dependency Inversion: phụ thuộc vào ITopicRepository interface thay vì concrete class.
    """
    
    def __init__(self, topic_repo: ITopicRepository):
        """
        Constructor nhận interface thay vì Session để tuân thủ DIP
        
        Args:
            topic_repo: Implementation của ITopicRepository
        """
        self.topic_repo = topic_repo

    def create_new_topic(self, data: TopicCreate) -> TopicResponse:
        """
        Tạo topic mới
        
        Business logic có thể thêm ở đây:
        - Validate title không trùng
        - Kiểm tra category_id tồn tại
        - Log hoạt động
        """
        topic = self.topic_repo.create(data)
        return TopicResponse.model_validate(topic)
    
    def get_topic_by_id(self, topic_id: int) -> Optional[TopicResponse]:
        """Lấy topic theo ID"""
        topic = self.topic_repo.get_by_id(topic_id)
        if topic:
            return TopicResponse.model_validate(topic)
        return None
    
    def get_all_topics(self, skip: int = 0, limit: int = 100) -> List[TopicResponse]:
        """Lấy danh sách topics"""
        topics = self.topic_repo.get_all(skip, limit)
        return [TopicResponse.model_validate(topic) for topic in topics]
    
    def update_topic(self, topic_id: int, data: TopicCreate) -> Optional[TopicResponse]:
        """Cập nhật topic"""
        topic = self.topic_repo.update(topic_id, data)
        if topic:
            return TopicResponse.model_validate(topic)
        return None
    
    def delete_topic(self, topic_id: int) -> bool:
        """Xóa topic"""
        return self.topic_repo.delete(topic_id)