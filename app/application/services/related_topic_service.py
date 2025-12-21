"""
Service cho việc tìm kiếm các topics liên quan sử dụng TF-IDF và Heuristic Scoring
"""

from typing import Dict, List, Optional, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.domain.models import Topic


class RelatedTopicService:
    """
    Service sử dụng TF-IDF + Heuristic Scoring để tìm các topics liên quan.

    Thuật toán:
    1. TF-IDF: Tính độ tương đồng nội dung giữa các topics
    2. Heuristic Scoring: Áp dụng các quy tắc:
       - Cùng category: +0.3 điểm bonus
       - Từ khóa trùng khớp trong title: +0.2 điểm
       - Độ dài definition tương tự: +0.1 điểm
    """

    def __init__(self) -> None:
        """Khởi tạo TF-IDF vectorizer với cấu hình tối ưu cho tiếng Việt và tiếng Anh"""
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 3),  # Unigrams, bigrams và trigrams
            min_df=1,
            max_df=0.8,
            stop_words="english",  # Có thể thêm stop words tiếng Việt sau
            lowercase=True,
        )

    def _prepare_text(self, topic: Topic) -> str:
        """
        Chuẩn bị text từ topic để xử lý TF-IDF.
        Kết hợp title và short_definition với trọng số khác nhau.
        """
        # Title có trọng số cao hơn (lặp lại 3 lần)
        title_text: str = str(topic.title)
        title_repeated = " ".join([title_text] * 3)

        # Kiểm tra short_definition có None không
        short_def = topic.short_definition
        definition_text: str = str(short_def) if short_def is not None else ""

        combined_text = f"{title_repeated} {definition_text}"
        return combined_text.strip()

    def _calculate_tfidf_similarity(
        self, source_topic: Topic, all_topics: List[Topic]
    ) -> Dict[int, float]:
        """
        Tính độ tương đồng TF-IDF giữa source_topic và tất cả topics khác.

        Returns:
            Dict mapping topic_id -> similarity_score (0-1)
        """
        # Chuẩn bị corpus
        corpus = [self._prepare_text(topic) for topic in all_topics]

        # Tính TF-IDF matrix
        tfidf_matrix = self.vectorizer.fit_transform(corpus)

        # Tìm index của source topic
        source_topic_id: int = source_topic.id  # type: ignore
        source_idx: Optional[int] = next(
            (
                i
                for i, topic in enumerate(all_topics)
                if topic.id == source_topic_id  # type: ignore
            ),
            None,
        )

        if source_idx is None:
            return {}

        # Tính cosine similarity
        # type: ignore cho spmatrix indexing
        similarities = cosine_similarity(
            tfidf_matrix[source_idx : source_idx + 1],  # type: ignore
            tfidf_matrix,
        ).flatten()

        # Tạo dictionary mapping topic_id -> similarity_score
        similarity_dict: Dict[int, float] = {}
        for i, topic in enumerate(all_topics):
            topic_id: int = topic.id  # type: ignore
            if topic_id != source_topic_id:  # Loại trừ chính nó
                similarity_dict[topic_id] = float(similarities[i])

        return similarity_dict

    def _calculate_heuristic_score(
        self, source_topic: Topic, candidate_topic: Topic
    ) -> float:
        """
        Tính điểm heuristic dựa trên các quy tắc (rules-based).

        Quy tắc:
        1. Cùng category: +0.3
        2. Từ khóa trong title trùng khớp: +0.2
        3. Độ dài definition tương tự (±20%): +0.1

        Returns:
            Float score từ 0.0 đến 0.6
        """
        score = 0.0

        # Rule 1: Cùng category
        source_category_id: int = source_topic.category_id  # type: ignore
        candidate_category_id: int = candidate_topic.category_id  # type: ignore
        if source_category_id == candidate_category_id:
            score += 0.3

        # Rule 2: Từ khóa trong title trùng khớp
        source_title: str = str(source_topic.title)
        candidate_title: str = str(candidate_topic.title)
        source_keywords = set(source_title.lower().split())
        candidate_keywords = set(candidate_title.lower().split())

        # Loại bỏ stop words phổ biến
        common_stop_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "của",
            "và",
            "là",
            "có",
            "trong",
            "với",
            "các",
            "được",
            "từ",
        }
        source_keywords -= common_stop_words
        candidate_keywords -= common_stop_words

        if source_keywords & candidate_keywords:  # Có từ chung
            overlap_ratio = len(source_keywords & candidate_keywords) / len(
                source_keywords
            )
            score += min(0.2, overlap_ratio * 0.3)  # Max 0.2 điểm

        # Rule 3: Độ dài definition tương tự
        source_definition = source_topic.short_definition
        candidate_definition = candidate_topic.short_definition

        if source_definition is not None and candidate_definition is not None:
            source_def_str: str = str(source_definition)
            candidate_def_str: str = str(candidate_definition)
            source_len = len(source_def_str)
            candidate_len = len(candidate_def_str)

            if source_len > 0:
                ratio = min(source_len, candidate_len) / max(source_len, candidate_len)
                if ratio >= 0.8:  # Độ dài tương tự ±20%
                    score += 0.1

        return score

    def find_related_topics(
        self, source_topic: Topic, all_topics: List[Topic], top_n: int = 5
    ) -> List[Tuple[Topic, float]]:
        """
        Tìm top N topics liên quan nhất đến source_topic.

        Args:
            source_topic: Topic cần tìm các topics liên quan
            all_topics: Danh sách tất cả topics trong hệ thống
            top_n: Số lượng topics liên quan cần trả về

        Returns:
            List of tuples (topic, combined_score) được sắp xếp theo điểm giảm dần
        """
        if len(all_topics) <= 1:
            return []

        # Bước 1: Tính TF-IDF similarity
        tfidf_scores = self._calculate_tfidf_similarity(source_topic, all_topics)

        # Bước 2: Tính combined score cho mỗi candidate
        combined_scores: List[Tuple[Topic, float]] = []
        source_topic_id: int = source_topic.id  # type: ignore

        for topic in all_topics:
            topic_id: int = topic.id  # type: ignore
            if topic_id == source_topic_id:
                continue  # Skip chính nó

            # TF-IDF score (0-1)
            tfidf_score = tfidf_scores.get(topic_id, 0.0)

            # Heuristic score (0-0.6)
            heuristic_score = self._calculate_heuristic_score(source_topic, topic)

            # Combined score: TF-IDF (70%) + Heuristic (30%)
            # Normalize về scale 0-1
            combined_score = (tfidf_score * 0.7) + (heuristic_score * 0.5)

            combined_scores.append((topic, combined_score))

        # Bước 3: Sắp xếp và lấy top N
        combined_scores.sort(key=lambda x: x[1], reverse=True)

        return combined_scores[:top_n]

    def get_topic_similarity_matrix(self, topics: List[Topic]) -> np.ndarray:
        """
        Tính ma trận tương đồng cho tất cả các topics.
        Hữu ích cho việc phân tích và visualization.

        Returns:
            numpy array shape (n_topics, n_topics)
        """
        if not topics:
            return np.array([])

        corpus = [self._prepare_text(topic) for topic in topics]
        tfidf_matrix = self.vectorizer.fit_transform(corpus)
        similarity_matrix = cosine_similarity(tfidf_matrix)

        return similarity_matrix
