from typing import List

from fastapi import HTTPException, status

from app.application.interfaces.related_topic_association_repository_interface import (
    IRelatedTopicAssociationRepository,
)
from app.domain.schemas.related_topic_association_schema import RelatedTopicLinkResponse
from app.domain.schemas.topic_schema import TopicResponse


class RelatedTopicAssociationService:
    def __init__(self, repo: IRelatedTopicAssociationRepository, topic_repo=None):
        self.repo = repo
        self.topic_repo = topic_repo

    def create_relation(
        self, topic_id: int, related_topic_id: int
    ) -> RelatedTopicLinkResponse:
        if topic_id == related_topic_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A topic cannot be related to itself",
            )

        # Validate both topics exist
        if self.topic_repo:
            if not self.topic_repo.get_by_id(topic_id):
                raise HTTPException(
                    status_code=404, detail=f"Topic {topic_id} not found"
                )
            if not self.topic_repo.get_by_id(related_topic_id):
                raise HTTPException(
                    status_code=404, detail=f"Topic {related_topic_id} not found"
                )

        if self.repo.exists(topic_id, related_topic_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Relation already exists",
            )

        self.repo.add_relation(topic_id, related_topic_id)
        return RelatedTopicLinkResponse(
            topic_id=topic_id, related_topic_id=related_topic_id
        )

    def get_related_topics(self, topic_id: int) -> List[TopicResponse]:
        if self.topic_repo and not self.topic_repo.get_by_id(topic_id):
            raise HTTPException(status_code=404, detail=f"Topic {topic_id} not found")
        topics = self.repo.list_related(topic_id)
        return [TopicResponse.model_validate(t) for t in topics]

    def delete_relation(self, topic_id: int, related_topic_id: int) -> None:
        if not self.repo.remove_relation(topic_id, related_topic_id):
            raise HTTPException(status_code=404, detail="Relation not found")

    def update_relation(
        self, topic_id: int, related_topic_id: int, new_related_topic_id: int
    ) -> RelatedTopicLinkResponse:
        # Remove old relation if exists, then add new
        if topic_id == new_related_topic_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A topic cannot be related to itself",
            )
        if not self.repo.remove_relation(topic_id, related_topic_id):
            raise HTTPException(status_code=404, detail="Original relation not found")
        # Reuse create to validate and add
        return self.create_relation(topic_id, new_related_topic_id)
