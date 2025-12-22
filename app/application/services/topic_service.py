from typing import List, Optional

from app.application.interfaces.topic_repository_interface import ITopicRepository
from app.application.services.related_topic_service import RelatedTopicService
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
        self.related_topic_service = RelatedTopicService()

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
        result = []
        for topic in topics:
            try:
                result.append(TopicResponse.model_validate(topic))
            except Exception as e:
                # Skip topics that fail validation (e.g., corrupted data)
                print(f"Warning: Failed to validate topic {topic.id}: {str(e)}")
                continue
        return result

    def update_topic(self, topic_id: int, data: TopicCreate) -> Optional[TopicResponse]:
        """Cập nhật topic"""
        topic = self.topic_repo.update(topic_id, data)
        if topic:
            return TopicResponse.model_validate(topic)
        return None

    def delete_topic(self, topic_id: int) -> bool:
        """Xóa topic"""
        return self.topic_repo.delete(topic_id)

    def find_related_topics(self, topic_id: int, top_n: int = 5) -> List[dict]:
        """
        Tìm các topics liên quan sử dụng TF-IDF + Heuristic Scoring.

        Args:
            topic_id: ID của topic cần tìm related topics
            top_n: Số lượng related topics cần trả về (mặc định 5)

        Returns:
            List[dict]: Danh sách topics liên quan kèm điểm số
                Format: [{"topic": TopicResponse, "score": float}, ...]
        """
        # Lấy topic nguồn
        source_topic = self.topic_repo.get_by_id(topic_id)
        if not source_topic:
            return []

        # Lấy tất cả topics (không load sections để tối ưu performance)
        all_topics = self.topic_repo.get_all_with_minimal_data()

        # Tìm related topics sử dụng thuật toán TF-IDF + Heuristic
        related_results = self.related_topic_service.find_related_topics(
            source_topic=source_topic, all_topics=all_topics, top_n=top_n
        )

        # Convert sang format response
        response_data = []
        for topic, score in related_results:
            response_data.append(
                {
                    "topic": TopicResponse.model_validate(topic),
                    "score": round(score, 4),  # Làm tròn điểm đến 4 chữ số thập phân
                }
            )

        return response_data
