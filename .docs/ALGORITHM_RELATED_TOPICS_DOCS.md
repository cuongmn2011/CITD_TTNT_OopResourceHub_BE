# Related Topics (TF-IDF + Heuristic)

Tài liệu hướng dẫn cách dùng API và mô tả chi tiết thuật toán tìm related topics cho OOP Resource Hub.

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

## Thuật toán chi tiết

### 1) Chuẩn bị dữ liệu văn bản
- Ghép văn bản: `text = title * 3 + " " + short_definition` (lặp title 3 lần để tăng trọng số).
- Tiền xử lý: lowercase, bỏ trống, dùng stop words tiếng Anh (có sẵn trong scikit-learn) và danh sách stop words Việt cơ bản tại [app/application/services/related_topic_service.py](app/application/services/related_topic_service.py).

### 2) Tính TF-IDF
- Cấu hình vectorizer: `max_features=1000`, `ngram_range=(1, 3)`, `max_df=0.8`, `min_df=1`, `stop_words="english"`, `lowercase=True`.
- Công thức: với từ $t$, document $d$, tổng documents $N$, số document chứa $t$ là $df(t)$:
    - $TF(t, d) = \frac{f_{t,d}}{\sum_{t'} f_{t',d}}$
    - $IDF(t) = \ln\left(\frac{N + 1}{df(t) + 1}\right) + 1$
    - $TFIDF(t, d) = TF(t, d) \times IDF(t)$

### 3) Độ tương đồng TF-IDF bằng Cosine Similarity
- Với vector TF-IDF của source $v_s$ và candidate $v_c$:
    $$\text{cosine}(s, c) = \frac{v_s \cdot v_c}{\lVert v_s \rVert_2\, \lVert v_c \rVert_2} \in [0, 1]$$

### 4) Heuristic Scoring (rule-based)
- Biến nhị phân và tỷ lệ:
    - $same\_cat = \mathbb{1}[category_s = category_c]$ (0 hoặc 1)
    - $overlap = \frac{|K_s \cap K_c|}{|K_s|}$ với $K$ là tập từ khóa title đã bỏ stop words; nếu $|K_s| = 0$ thì 0.
    - $len\_ratio = \frac{\min(len_s, len_c)}{\max(len_s, len_c)}$ với $len$ là độ dài `short_definition` (0 nếu thiếu dữ liệu).
- Điểm heuristic:
    $$H = 0.3 \times same\_cat + \min(0.2, 0.3 \times overlap) + 0.1 \times \mathbb{1}[len\_ratio \ge 0.8]$$

### 5) Kết hợp điểm
- Điểm cuối:
    $$score = 0.7 \times \text{cosine} + 0.5 \times H$$
- Phạm vi trước sorting ~[0, 1.2]; không clamp mà chỉ sắp xếp giảm dần và lấy top N.

### 6) Quy trình thực thi
1. API nhận request ở [app/api/v1/endpoints/topic_api.py](app/api/v1/endpoints/topic_api.py): validate `top_n`, gọi service.
2. [app/application/services/topic_service.py](app/application/services/topic_service.py) lấy topic nguồn, toàn bộ topics (không load sections) qua repo, gọi `RelatedTopicService`.
3. [app/application/services/related_topic_service.py](app/application/services/related_topic_service.py):
     - Chuẩn bị corpus, fit TF-IDF, tính cosine giữa source và tất cả topics.
     - Tính heuristic cho từng cặp source-candidate.
     - Tính `score`, sort, trả về top N.
4. Repo [app/infrastructure/repositories/topic_repository.py](app/infrastructure/repositories/topic_repository.py) dùng `get_all_with_minimal_data()` để giảm tải (không eager load sections).

## Vì sao chọn TF-IDF + heuristic

- **Nhanh và không cần GPU**: TF-IDF + cosine chạy tốt trên CPU, phù hợp service nhỏ/medium mà không cần model lớn.
- **Ít dữ liệu vẫn hiệu quả**: Không cần tập huấn luyện; tận dụng dữ liệu text sẵn có.
- **Giải thích được**: Heuristic nêu rõ lý do tăng điểm (cùng category, trùng từ khóa, độ dài tương tự), dễ debug.
- **Chi phí thấp**: Bộ nhớ gọn (`max_features=1000`, n-gram tới 3), phù hợp khi số topic vài trăm–vài nghìn.
- **Dễ mở rộng**: Có thể thêm stop words tiếng Việt, đổi trọng số, hoặc thay TF-IDF bằng embeddings khi cần mà vẫn giữ khung logic combine.

## Lưu ý triển khai

- Để ra kết quả, corpus cần ≥2 topic và `title`/`short_definition` không rỗng.
- Với dữ liệu lớn, cân nhắc cache TF-IDF matrix hoặc kết quả top N; hoặc chuyển sang vector DB/embeddings.
- Nếu title ngắn, lặp 3 lần giúp cân bằng với `short_definition`; có thể điều chỉnh khi title dài hơn.

## Luồng thực thi

1. API: [app/api/v1/endpoints/topic_api.py](app/api/v1/endpoints/topic_api.py) nhận `/{topic_id}/related`.
2. Service: [app/application/services/topic_service.py](app/application/services/topic_service.py) lấy topic nguồn, toàn bộ topics (không load sections) và gọi `RelatedTopicService`.
3. Thuật toán: [app/application/services/related_topic_service.py](app/application/services/related_topic_service.py) tính TF-IDF, heuristic, cộng điểm và sắp xếp.
4. Repository: [app/infrastructure/repositories/topic_repository.py](app/infrastructure/repositories/topic_repository.py) cung cấp `get_all_with_minimal_data()` để tránh eager load sections.

## Troubleshooting

- Thiếu `sklearn` hoặc `numpy`: `pip install scikit-learn numpy`.
- `Topic not found`: kiểm tra `topic_id` tồn tại và DB kết nối tốt.
- Không có kết quả: cần tối thiểu 2 topics, dữ liệu phải có `title` và `short_definition` không rỗng.

## Performance và hướng phát triển

- Dataset nhỏ (<100): ~100–200ms; trung bình (100–1000): ~0.5–1s; lớn: cân nhắc cache TF-IDF và kết quả.
- Kế hoạch: thêm Vietnamese stop words, cache Redis, A/B test trọng số.

## Phụ thuộc

- scikit-learn==1.5.2
- numpy==1.26.4
