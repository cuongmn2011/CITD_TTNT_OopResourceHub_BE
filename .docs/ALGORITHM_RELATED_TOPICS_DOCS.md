# Related Topics (TF-IDF + Heuristic)

Tài liệu hợp nhất hướng dẫn chạy, cách dùng API và mô tả chi tiết thuật toán tìm related topics cho OOP Resource Hub.

## Quick Start

- Cài đặt: `pip install -r requirements.txt`
- Chạy server: `python run.py` hoặc `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- Swagger: mở `http://localhost:8000/docs`

## API

- Endpoint: `GET /api/v1/topics/{topic_id}/related`
- Query: `top_n` (mặc định 5, min 1, max 20)
- Response: mảng `{ "topic": TopicResponse, "score": float }`

Ví dụ:
```bash
curl "http://localhost:8000/api/v1/topics/1/related?top_n=5"
```

```json
[
    {
        "topic": {
            "id": 3,
            "title": "Polymorphism",
            "short_definition": "Khả năng một đối tượng có thể có nhiều hình thái khác nhau...",
            "category_id": 1,
            "created_at": "2024-01-01T00:00:00.000Z",
            "sections": []
        },
        "score": 0.8543
    }
]
```

## Thuật toán

- Chuẩn bị văn bản: lặp lại `title` 3 lần + nối `short_definition`, lowercase.
- TF-IDF: `max_features=1000`, `ngram_range=(1, 3)`, `max_df=0.8`, `min_df=1`, `stop_words="english"`.
- Cosine similarity cho TF-IDF scores trong [0, 1].
- Heuristic rules (0–0.6):
    - +0.3 nếu cùng `category_id`.
    - +0.2 tối đa nếu có từ khóa chung trong title (loại bỏ stop words Anh + Việt cơ bản).
    - +0.1 nếu độ dài `short_definition` tương tự (≥80%).
- Điểm cuối: $score = 0.7 \times tfidf + 0.5 \times heuristic$ (chuẩn hóa về thang 0–1 theo sorting, không clamp).

## Luồng thực thi

1. API: [app/api/v1/endpoints/topic_api.py](app/api/v1/endpoints/topic_api.py) nhận `/{topic_id}/related`.
2. Service: [app/application/services/topic_service.py](app/application/services/topic_service.py) lấy topic nguồn, toàn bộ topics (không load sections) và gọi `RelatedTopicService`.
3. Thuật toán: [app/application/services/related_topic_service.py](app/application/services/related_topic_service.py) tính TF-IDF, heuristic, cộng điểm và sắp xếp.
4. Repository: [app/infrastructure/repositories/topic_repository.py](app/infrastructure/repositories/topic_repository.py) cung cấp `get_all_with_minimal_data()` để tránh eager load sections.

## Test nhanh với dữ liệu mẫu

```bash
# Category
curl -X POST http://localhost:8000/api/v1/categories \
    -H "Content-Type: application/json" \
    -d '{"name":"Core Concepts","slug":"core-concepts"}'

# Topics
curl -X POST http://localhost:8000/api/v1/topics \
    -H "Content-Type: application/json" \
    -d '{"title":"Inheritance","short_definition":"...","category_id":1,"sections":[]}'

curl -X POST http://localhost:8000/api/v1/topics \
    -H "Content-Type: application/json" \
    -d '{"title":"Polymorphism","short_definition":"...","category_id":1,"sections":[]}'

# Related
curl "http://localhost:8000/api/v1/topics/1/related?top_n=3"
```

## Troubleshooting

- Thiếu `sklearn` hoặc `numpy`: `pip install scikit-learn numpy`.
- `Topic not found`: kiểm tra `topic_id` tồn tại và DB kết nối tốt.
- Không có kết quả: cần tối thiểu 2 topics, dữ liệu phải có `title` và `short_definition` không rỗng.

## Performance và hướng phát triển

- Dataset nhỏ (<100): ~100–200ms; trung bình (100–1000): ~0.5–1s; lớn: cân nhắc cache TF-IDF và kết quả.
- Kế hoạch: thêm Vietnamese stop words, cache Redis, A/B test trọng số, cá nhân hóa theo hành vi người dùng.

## Phụ thuộc

- scikit-learn==1.5.2
- numpy==1.26.4
