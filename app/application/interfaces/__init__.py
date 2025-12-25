"""
Repository Interfaces
Định nghĩa các contracts cho repositories theo Dependency Inversion Principle.
"""

from .category_repository_interface import ICategoryRepository
from .related_topic_association_repository_interface import IRelatedTopicAssociationRepository
from .section_repository_interface import ISectionRepository
from .topic_repository_interface import ITopicRepository
from .tag_repository_interface import ITagRepository

__all__ = [
    "ICategoryRepository",
    "IRelatedTopicAssociationRepository",
    "ISectionRepository",
    "ITopicRepository",
    "ITagRepository",
]
