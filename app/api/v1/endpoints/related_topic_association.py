from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.application.services.related_topic_association_service import (
    RelatedTopicAssociationService,
)
from app.domain.schemas.related_topic_association_schema import (
    RelatedTopicIdPayload,
    RelatedTopicLinkCreate,
    RelatedTopicLinkResponse,
    RelatedTopicLinkUpdate,
    RelatedTopicReplacePayload,
)
from app.domain.schemas.topic_schema import TopicResponse
from app.infrastructure.database import get_db
from app.infrastructure.repositories.related_topic_association_repository import (
    RelatedTopicAssociationRepository,
)
from app.infrastructure.repositories.topic_repository import TopicRepository

router = APIRouter()


def get_related_service(
    db: Session = Depends(get_db),
) -> RelatedTopicAssociationService:
    repo = RelatedTopicAssociationRepository(db)
    topic_repo = TopicRepository(db)
    return RelatedTopicAssociationService(repo, topic_repo)


@router.post(
    "/", response_model=RelatedTopicLinkResponse, status_code=status.HTTP_201_CREATED
)
def create_relation(
    payload: RelatedTopicLinkCreate,
    service: RelatedTopicAssociationService = Depends(get_related_service),
):
    try:
        return service.create_relation(payload.topic_id, payload.related_topic_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{topic_id}", response_model=List[TopicResponse])
def list_related_topics(
    topic_id: int,
    service: RelatedTopicAssociationService = Depends(get_related_service),
):
    try:
        return service.get_related_topics(topic_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Path-param variants for clearer REST style ---
@router.post(
    "/{topic_id}",
    response_model=RelatedTopicLinkResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_relation_for_topic(
    topic_id: int,
    payload: RelatedTopicIdPayload,
    service: RelatedTopicAssociationService = Depends(get_related_service),
):
    try:
        return service.create_relation(topic_id, payload.related_topic_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{topic_id}/{related_topic_id}", status_code=status.HTTP_200_OK)
def delete_relation_for_topic(
    topic_id: int,
    related_topic_id: int,
    service: RelatedTopicAssociationService = Depends(get_related_service),
):
    try:
        service.delete_relation(topic_id, related_topic_id)
        return {"message": "Relation deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/{topic_id}/{related_topic_id}",
    response_model=RelatedTopicLinkResponse,
)
def update_relation_for_topic(
    topic_id: int,
    related_topic_id: int,
    payload: RelatedTopicReplacePayload,
    service: RelatedTopicAssociationService = Depends(get_related_service),
):
    try:
        return service.update_relation(
            topic_id, related_topic_id, payload.new_related_topic_id
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/", status_code=status.HTTP_200_OK)
def delete_relation(
    payload: RelatedTopicLinkCreate,
    service: RelatedTopicAssociationService = Depends(get_related_service),
):
    try:
        service.delete_relation(payload.topic_id, payload.related_topic_id)
        return {"message": "Relation deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/", response_model=RelatedTopicLinkResponse)
def update_relation(
    payload: RelatedTopicLinkUpdate,
    service: RelatedTopicAssociationService = Depends(get_related_service),
):
    try:
        return service.update_relation(
            payload.topic_id, payload.related_topic_id, payload.new_related_topic_id
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
