"""
Service xử lý tìm kiếm với fuzzy matching
"""
import re
import unicodedata
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.domain.models.topic import Topic
from app.domain.models.section import Section
from app.domain.models.category import Category
from app.domain.schemas.search_schema import (
    SearchResponse,
    TopicSearchResult,
    SectionSearchResult,
    CategorySearchResult,
)


class SearchService:
    """Service xử lý tìm kiếm với fuzzy matching và scoring"""

    def __init__(self, db: Session):
        self.db = db

    def remove_vietnamese_tones(self, text: str) -> str:
        """Loại bỏ dấu tiếng Việt để search linh hoạt hơn"""
        if not text:
            return ""
        # Normalize và loại bỏ dấu
        text = unicodedata.normalize('NFD', text)
        text = re.sub(r'[\u0300-\u036f]', '', text)
        # Xử lý đ/Đ
        text = text.replace('đ', 'd').replace('Đ', 'D')
        return text.lower()

    def extract_keywords(self, query: str) -> list[str]:
        """
        Trích xuất từ khóa quan trọng từ câu tìm kiếm.
        Loại bỏ stop words tiếng Việt và giữ lại từ có nghĩa.
        """
        # Stop words tiếng Việt phổ biến
        stop_words = {
            'là', 'của', 'và', 'có', 'được', 'trong', 'để', 'một', 'các',
            'này', 'cho', 'từ', 'với', 'những', 'thì', 'về', 'làm', 'sao',
            'như', 'nào', 'thế', 'gì', 'ai', 'đâu', 'khi', 'bao', 'giờ',
            'hiểu', 'học', 'tìm', 'biết', 'muốn', 'cần', 'the', 'a', 'an',
            'to', 'of', 'in', 'on', 'at', 'for', 'is', 'are', 'was', 'were'
        }
        
        # Loại bỏ dấu và chuyển thành chữ thường
        normalized = self.remove_vietnamese_tones(query)
        
        # Tách thành từng từ
        words = normalized.split()
        
        # Lọc bỏ stop words và giữ từ có độ dài >= 2
        keywords = [w for w in words if w not in stop_words and len(w) >= 2]
        
        # Nếu không có keyword nào sau khi lọc, giữ nguyên query gốc
        if not keywords:
            keywords = [normalized]
        
        return keywords

    def calculate_relevance_score(self, text: str, query: str) -> float:
        """
        Tính điểm relevance dựa trên nhiều tiêu chí:
        - Exact match: 1.0
        - Starts with query: 0.9
        - Contains query: 0.7
        - Any keyword match: 0.6
        - Fuzzy match: 0.5
        - Partial word match: 0.3
        """
        if not text or not query:
            return 0.0

        text_normalized = self.remove_vietnamese_tones(text)
        query_normalized = self.remove_vietnamese_tones(query)

        # Exact match
        if text_normalized == query_normalized:
            return 1.0

        # Starts with
        if text_normalized.startswith(query_normalized):
            return 0.9

        # Contains exact query
        if query_normalized in text_normalized:
            return 0.7

        # Extract keywords from query
        keywords = self.extract_keywords(query)
        
        # Check if any keyword appears in text (case insensitive)
        text_words = set(text_normalized.split())
        for keyword in keywords:
            # Exact keyword match trong text
            if keyword in text_normalized:
                # Nếu keyword match toàn bộ một từ trong text -> điểm cao nhất
                text_words_list = text_normalized.split()
                if keyword in text_words_list:
                    return 0.95  # Exact word match
                return 0.85  # Keyword contained in text
            
            # Check if keyword matches any word in text
            for word in text_words:
                if keyword in word or word in keyword:
                    return 0.65

        # Word-level matching
        query_words = set(query_normalized.split())
        
        if query_words.issubset(text_words):
            return 0.6

        # Partial word match
        matching_words = text_words.intersection(query_words)
        if matching_words:
            return 0.5 * (len(matching_words) / len(query_words))

        # Fuzzy sequential character matching
        query_index = 0
        for char in text_normalized:
            if query_index < len(query_normalized) and char == query_normalized[query_index]:
                query_index += 1

        if query_index == len(query_normalized):
            return 0.3

        return 0.0

    def search(self, query: str, limit: int = 20, tag_ids: list[int] = None) -> SearchResponse:
        """
        Tìm kiếm topics, sections, categories với fuzzy matching

        Args:
            query: Chuỗi tìm kiếm (ví dụ: "Làm sao để hiểu OOP")
            limit: Số lượng kết quả tối đa cho mỗi loại
            tag_ids: Danh sách tag IDs để filter topics (optional)

        Returns:
            SearchResponse chứa kết quả tìm kiếm được sắp xếp theo độ liên quan
        """
        if not query or not query.strip():
            return SearchResponse(query=query, total_results=0)

        query_normalized = self.remove_vietnamese_tones(query)
        query_words = query_normalized.split()

        # Search Topics
        topics_results = []
        topics_query = self.db.query(Topic)
        
        # Filter by tags if provided
        if tag_ids:
            from app.domain.models.tag import topic_tags
            topics_query = topics_query.join(topic_tags).filter(topic_tags.c.tag_id.in_(tag_ids))
        
        topics = topics_query.all()
        
        for topic in topics:
            # Calculate score based on title and definition
            title_score = self.calculate_relevance_score(topic.title, query)
            def_score = self.calculate_relevance_score(topic.short_definition or "", query)
            
            # Combined score: title có trọng số cao hơn (60%), definition (50%)
            # Nhưng nếu definition có điểm cao thì vẫn được ưu tiên
            combined_score = max(title_score, def_score * 0.95)
            max_score = combined_score
            
            if max_score > 0.15:  # Threshold - giảm xuống để dễ tìm hơn
                category_name = topic.category.name if topic.category else ""
                topics_results.append(
                    TopicSearchResult(
                        id=topic.id,
                        title=topic.title,
                        short_definition=topic.short_definition,
                        category_id=topic.category_id,
                        category_name=category_name,
                        created_at=topic.created_at,
                        score=max_score,
                    )
                )

        # Sort by score and limit
        topics_results.sort(key=lambda x: x.score, reverse=True)
        topics_results = topics_results[:limit]

        # Search Sections
        sections_results = []
        sections = self.db.query(Section).all()
        
        for section in sections:
            heading_score = self.calculate_relevance_score(section.heading or "", query)
            content_score = self.calculate_relevance_score(section.content or "", query) * 0.6
            
            max_score = max(heading_score, content_score)
            
            if max_score > 0.15:
                topic_title = section.topic.title if section.topic else ""
                content_preview = (section.content[:200] + "...") if section.content and len(section.content) > 200 else section.content
                
                sections_results.append(
                    SectionSearchResult(
                        id=section.id,
                        title=section.heading or "",
                        heading=section.heading or "",
                        topic_id=section.topic_id,
                        topic_title=topic_title,
                        content_preview=content_preview,
                        score=max_score,
                    )
                )

        sections_results.sort(key=lambda x: x.score, reverse=True)
        sections_results = sections_results[:limit]

        # Search Categories
        categories_results = []
        categories = self.db.query(Category).all()
        
        for category in categories:
            name_score = self.calculate_relevance_score(category.name, query)
            slug_score = self.calculate_relevance_score(category.slug or "", query) * 0.5
            
            max_score = max(name_score, slug_score)
            
            if max_score > 0.15:
                topic_count = len(category.topics) if category.topics else 0
                
                categories_results.append(
                    CategorySearchResult(
                        id=category.id,
                        title=category.name,
                        description=None,  # Category không có description field
                        topic_count=topic_count,
                        score=max_score,
                    )
                )

        categories_results.sort(key=lambda x: x.score, reverse=True)
        categories_results = categories_results[:limit]

        total = len(topics_results) + len(sections_results) + len(categories_results)

        return SearchResponse(
            query=query,
            total_results=total,
            topics=topics_results,
            sections=sections_results,
            categories=categories_results,
        )
