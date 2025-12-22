from abc import ABC, abstractmethod
from typing import List

from app.domain.models import Topic


class IRelatedTopicAssociationRepository(ABC):
    @abstractmethod
    def add_relation(self, topic_id: int, related_topic_id: int) -> None:
        pass

    @abstractmethod
    def remove_relation(self, topic_id: int, related_topic_id: int) -> bool:
        pass

    @abstractmethod
    def list_related(self, topic_id: int) -> List[Topic]:
        pass

    @abstractmethod
    def exists(self, topic_id: int, related_topic_id: int) -> bool:
        pass
