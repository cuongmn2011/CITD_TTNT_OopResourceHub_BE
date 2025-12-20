from pydantic import BaseModel, Field, field_validator


class RelatedTopicLinkBase(BaseModel):
    topic_id: int = Field(..., gt=0)
    related_topic_id: int = Field(..., gt=0)

    @field_validator("related_topic_id")
    @classmethod
    def not_self(cls, v, info):
        # topic_id only available post-validation, skip strict here; validate in service too
        return v


class RelatedTopicLinkCreate(RelatedTopicLinkBase):
    pass


class RelatedTopicLinkUpdate(BaseModel):
    topic_id: int = Field(..., gt=0)
    related_topic_id: int = Field(..., gt=0)
    new_related_topic_id: int = Field(..., gt=0)


class RelatedTopicLinkResponse(RelatedTopicLinkBase):
    class Config:
        from_attributes = True


class RelatedTopicIdPayload(BaseModel):
    related_topic_id: int = Field(..., gt=0)


class RelatedTopicReplacePayload(BaseModel):
    new_related_topic_id: int = Field(..., gt=0)
