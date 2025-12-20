from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.application.interfaces.related_topic_association_repository_interface import (
    IRelatedTopicAssociationRepository,
)
from app.domain.models import Topic, related_topics_association


class RelatedTopicAssociationRepository(IRelatedTopicAssociationRepository):
    def __init__(self, db: Session):
        self.db = db

    def add_relation(self, topic_id: int, related_topic_id: int) -> None:
        topic = self.db.query(Topic).filter(Topic.id == topic_id).first()
        related = self.db.query(Topic).filter(Topic.id == related_topic_id).first()
        if not topic or not related:
            raise ValueError("Topic or related topic not found")
        if related in topic.related_topics:
            return
        topic.related_topics.append(related)
        self.db.commit()

    def remove_relation(self, topic_id: int, related_topic_id: int) -> bool:
        topic = self.db.query(Topic).filter(Topic.id == topic_id).first()
        related = self.db.query(Topic).filter(Topic.id == related_topic_id).first()
        if not topic or not related:
            return False
        if related in topic.related_topics:
            topic.related_topics.remove(related)
            self.db.commit()
            return True
        return False

    def list_related(self, topic_id: int) -> List[Topic]:
        topic = self.db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            return []
        # Access relationship collection
        return list(topic.related_topics)

    def exists(self, topic_id: int, related_topic_id: int) -> bool:
        q = self.db.query(related_topics_association).filter(
            and_(
                related_topics_association.c.topic_id == topic_id,
                related_topics_association.c.related_topic_id == related_topic_id,
            )
        )
        return self.db.query(q.exists()).scalar()
