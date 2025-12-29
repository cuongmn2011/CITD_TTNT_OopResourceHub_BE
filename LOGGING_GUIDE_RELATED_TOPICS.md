# Hướng dẫn đọc Logs cho API GET /api/v1/related-topics/{topic_id}

Tài liệu này hướng dẫn cách đọc và debug logs khi gọi API `GET /api/v1/related-topics/91`

## 📋 Cấu hình Logging

Logging đã được cấu hình trong `run.py` với level `DEBUG`:

```python
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
```

## 🔍 Các loại Logs

### 1. [API] Layer - Route Handler
**File:** `app/api/v1/endpoints/related_topic_association.py`

- `[API] GET /api/v1/related-topics/{id} - Starting request`
  - Log khi bắt đầu xử lý request

- `[API] GET /api/v1/related-topics/{id} - Success: Found {count} related topics`
  - Log khi thành công, kèm số lượng related topics

- `[API] GET /api/v1/related-topics/{id} - Response data: [...]`
  - Log chi tiết dữ liệu response (DEBUG level)

- `[API] GET /api/v1/related-topics/{id} - HTTPException: {code} - {detail}`
  - Log khi có HTTPException (WARNING level)

- `[API] GET /api/v1/related-topics/{id} - Unexpected error: {error}`
  - Log khi có lỗi không mong muốn (ERROR level)

### 2. [SERVICE] Layer - Business Logic
**File:** `app/application/services/related_topic_association_service.py`

- `[SERVICE] get_related_topics - START: topic_id={id}`
  - Bắt đầu xử lý trong service layer

- `[SERVICE] get_related_topics - Validating topic {id} exists...`
  - Bắt đầu validate topic

- `[SERVICE] get_related_topics - Topic {id} validated: title='{title}'`
  - Topic tồn tại và đã được validate

- `[SERVICE] get_related_topics - Topic {id} NOT FOUND in database`
  - Topic không tồn tại (WARNING level)

- `[SERVICE] get_related_topics - Querying related topics from repository...`
  - Bắt đầu query related topics

- `[SERVICE] get_related_topics - Repository returned {count} related topics`
  - Repository đã trả về kết quả

- `[SERVICE] get_related_topics - No related topics found for topic_id={id}`
  - Không tìm thấy related topics (WARNING level)

- `[SERVICE] get_related_topics - Related topic IDs: [...]`
  - Danh sách IDs của related topics

- `[SERVICE] get_related_topics - Converting to Pydantic schemas...`
  - Bắt đầu convert sang Pydantic

- `[SERVICE] get_related_topics - Successfully converted {count} topics to TopicResponse`
  - Convert thành công

### 3. [REPO] Layer - Database Repository
**File:** `app/infrastructure/repositories/related_topic_association_repository.py`

- `[REPO] list_related - START: topic_id={id}`
  - Bắt đầu query trong repository

- `[REPO] list_related - Querying topic with id={id} from database...`
  - Đang query topic từ database

- `[REPO] list_related - Topic found: id={id}, title='{title}', category_id={category_id}`
  - Topic đã được tìm thấy

- `[REPO] list_related - Topic with id={id} NOT FOUND in database`
  - Topic không tồn tại (WARNING level)

- `[REPO] list_related - Accessing related_topics relationship...`
  - Đang truy cập relationship related_topics

- `[REPO] list_related - Relationship returned {count} related topics`
  - Relationship đã trả về kết quả

- `[REPO] list_related - Related topic IDs: [...]`
  - Danh sách IDs của related topics từ relationship

- `[REPO] list_related - topic.related_topics relationship is EMPTY for topic_id={id}`
  - Relationship trống (WARNING level)

- `[REPO] list_related - Checking related_topics_association table directly...`
  - Kiểm tra trực tiếp bảng database

- `[REPO] list_related - Direct query to related_topics_association returned {count} rows`
  - Kết quả query trực tiếp từ bảng

- `[REPO] list_related - Direct query results: [...]`
  - Chi tiết kết quả query trực tiếp

- `[REPO] list_related - No records in related_topics_association table for topic_id={id}`
  - Không có records trong bảng (WARNING level)

**File:** `app/infrastructure/repositories/topic_repository.py`

- `[REPO] TopicRepository.get_by_id - Querying topic id={id}`
  - Đang query topic để validate (DEBUG level)

- `[REPO] TopicRepository.get_by_id - Topic found: id={id}, title='{title}'`
  - Topic được tìm thấy (DEBUG level)

- `[REPO] TopicRepository.get_by_id - Topic id={id} NOT FOUND`
  - Topic không tồn tại (DEBUG level)

## 📊 Ví dụ Log Output

### Trường hợp thành công (có related topics):

```
2024-01-15 10:30:45,123 [INFO] app.api.v1.endpoints.related_topic_association: [API] GET /api/v1/related-topics/91 - Starting request
2024-01-15 10:30:45,124 [INFO] app.application.services.related_topic_association_service: [SERVICE] get_related_topics - START: topic_id=91
2024-01-15 10:30:45,125 [INFO] app.application.services.related_topic_association_service: [SERVICE] get_related_topics - Validating topic 91 exists...
2024-01-15 10:30:45,126 [DEBUG] app.infrastructure.repositories.topic_repository: [REPO] TopicRepository.get_by_id - Querying topic id=91
2024-01-15 10:30:45,130 [DEBUG] app.infrastructure.repositories.topic_repository: [REPO] TopicRepository.get_by_id - Topic found: id=91, title='Encapsulation'
2024-01-15 10:30:45,131 [INFO] app.application.services.related_topic_association_service: [SERVICE] get_related_topics - Topic 91 validated: title='Encapsulation'
2024-01-15 10:30:45,132 [INFO] app.application.services.related_topic_association_service: [SERVICE] get_related_topics - Querying related topics from repository...
2024-01-15 10:30:45,133 [INFO] app.infrastructure.repositories.related_topic_association_repository: [REPO] list_related - START: topic_id=91
2024-01-15 10:30:45,134 [INFO] app.infrastructure.repositories.related_topic_association_repository: [REPO] list_related - Querying topic with id=91 from database...
2024-01-15 10:30:45,140 [INFO] app.infrastructure.repositories.related_topic_association_repository: [REPO] list_related - Topic found: id=91, title='Encapsulation', category_id=1
2024-01-15 10:30:45,141 [INFO] app.infrastructure.repositories.related_topic_association_repository: [REPO] list_related - Accessing related_topics relationship...
2024-01-15 10:30:45,145 [INFO] app.infrastructure.repositories.related_topic_association_repository: [REPO] list_related - Relationship returned 2 related topics
2024-01-15 10:30:45,146 [INFO] app.infrastructure.repositories.related_topic_association_repository: [REPO] list_related - Related topic IDs: [92, 93]
2024-01-15 10:30:45,147 [INFO] app.application.services.related_topic_association_service: [SERVICE] get_related_topics - Repository returned 2 related topics
2024-01-15 10:30:45,148 [INFO] app.application.services.related_topic_association_service: [SERVICE] get_related_topics - Related topic IDs: [92, 93]
2024-01-15 10:30:45,149 [INFO] app.application.services.related_topic_association_service: [SERVICE] get_related_topics - Converting to Pydantic schemas...
2024-01-15 10:30:45,150 [INFO] app.application.services.related_topic_association_service: [SERVICE] get_related_topics - Successfully converted 2 topics to TopicResponse
2024-01-15 10:30:45,151 [INFO] app.api.v1.endpoints.related_topic_association: [API] GET /api/v1/related-topics/91 - Success: Found 2 related topics
```

### Trường hợp không có related topics (topic tồn tại):

```
2024-01-15 10:31:00,123 [INFO] app.api.v1.endpoints.related_topic_association: [API] GET /api/v1/related-topics/91 - Starting request
2024-01-15 10:31:00,124 [INFO] app.application.services.related_topic_association_service: [SERVICE] get_related_topics - START: topic_id=91
2024-01-15 10:31:00,125 [INFO] app.application.services.related_topic_association_service: [SERVICE] get_related_topics - Validating topic 91 exists...
2024-01-15 10:31:00,126 [DEBUG] app.infrastructure.repositories.topic_repository: [REPO] TopicRepository.get_by_id - Querying topic id=91
2024-01-15 10:31:00,130 [DEBUG] app.infrastructure.repositories.topic_repository: [REPO] TopicRepository.get_by_id - Topic found: id=91, title='Encapsulation'
2024-01-15 10:31:00,131 [INFO] app.application.services.related_topic_association_service: [SERVICE] get_related_topics - Topic 91 validated: title='Encapsulation'
2024-01-15 10:31:00,132 [INFO] app.application.services.related_topic_association_service: [SERVICE] get_related_topics - Querying related topics from repository...
2024-01-15 10:31:00,133 [INFO] app.infrastructure.repositories.related_topic_association_repository: [REPO] list_related - START: topic_id=91
2024-01-15 10:31:00,134 [INFO] app.infrastructure.repositories.related_topic_association_repository: [REPO] list_related - Querying topic with id=91 from database...
2024-01-15 10:31:00,140 [INFO] app.infrastructure.repositories.related_topic_association_repository: [REPO] list_related - Topic found: id=91, title='Encapsulation', category_id=1
2024-01-15 10:31:00,141 [INFO] app.infrastructure.repositories.related_topic_association_repository: [REPO] list_related - Accessing related_topics relationship...
2024-01-15 10:31:00,145 [INFO] app.infrastructure.repositories.related_topic_association_repository: [REPO] list_related - Relationship returned 0 related topics
2024-01-15 10:31:00,146 [WARNING] app.infrastructure.repositories.related_topic_association_repository: [REPO] list_related - topic.related_topics relationship is EMPTY for topic_id=91
2024-01-15 10:31:00,147 [DEBUG] app.infrastructure.repositories.related_topic_association_repository: [REPO] list_related - Checking related_topics_association table directly...
2024-01-15 10:31:00,150 [INFO] app.infrastructure.repositories.related_topic_association_repository: [REPO] list_related - Direct query to related_topics_association returned 0 rows
2024-01-15 10:31:00,151 [WARNING] app.infrastructure.repositories.related_topic_association_repository: [REPO] list_related - No records in related_topics_association table for topic_id=91
2024-01-15 10:31:00,152 [INFO] app.application.services.related_topic_association_service: [SERVICE] get_related_topics - Repository returned 0 related topics
2024-01-15 10:31:00,153 [WARNING] app.application.services.related_topic_association_service: [SERVICE] get_related_topics - No related topics found for topic_id=91
2024-01-15 10:31:00,154 [INFO] app.application.services.related_topic_association_service: [SERVICE] get_related_topics - Converting to Pydantic schemas...
2024-01-15 10:31:00,155 [INFO] app.application.services.related_topic_association_service: [SERVICE] get_related_topics - Successfully converted 0 topics to TopicResponse
2024-01-15 10:31:00,156 [INFO] app.api.v1.endpoints.related_topic_association: [API] GET /api/v1/related-topics/91 - Success: Found 0 related topics
```

### Trường hợp topic không tồn tại:

```
2024-01-15 10:32:00,123 [INFO] app.api.v1.endpoints.related_topic_association: [API] GET /api/v1/related-topics/999 - Starting request
2024-01-15 10:32:00,124 [INFO] app.application.services.related_topic_association_service: [SERVICE] get_related_topics - START: topic_id=999
2024-01-15 10:32:00,125 [INFO] app.application.services.related_topic_association_service: [SERVICE] get_related_topics - Validating topic 999 exists...
2024-01-15 10:32:00,126 [DEBUG] app.infrastructure.repositories.topic_repository: [REPO] TopicRepository.get_by_id - Querying topic id=999
2024-01-15 10:32:00,130 [DEBUG] app.infrastructure.repositories.topic_repository: [REPO] TopicRepository.get_by_id - Topic id=999 NOT FOUND
2024-01-15 10:32:00,131 [WARNING] app.application.services.related_topic_association_service: [SERVICE] get_related_topics - Topic 999 NOT FOUND in database
2024-01-15 10:32:00,132 [WARNING] app.api.v1.endpoints.related_topic_association: [API] GET /api/v1/related-topics/999 - HTTPException: 404 - Topic 999 not found
```

## 🔧 Cách Debug

### 1. Kiểm tra Topic có tồn tại không
Tìm log: `[REPO] TopicRepository.get_by_id - Topic found/NOT FOUND`

### 2. Kiểm tra Related Topics trong Database
Tìm log: `[REPO] list_related - Direct query to related_topics_association returned {count} rows`

Nếu count = 0, có nghĩa là:
- Topic tồn tại nhưng chưa có related topics được tạo
- Cần tạo relationship bằng API `POST /api/v1/related-topics/` hoặc `POST /api/v1/related-topics/{topic_id}`

### 3. Kiểm tra Relationship SQLAlchemy
Tìm log: `[REPO] list_related - Relationship returned {count} related topics`

Nếu relationship trả về 0 nhưng direct query có data:
- Có thể là vấn đề với SQLAlchemy relationship configuration
- Cần kiểm tra lại relationship trong `Topic` model

### 4. Kiểm tra Data Conversion
Tìm log: `[SERVICE] get_related_topics - Successfully converted {count} topics to TopicResponse`

Nếu conversion fail, sẽ có ERROR log với exception details.

## 📝 Ghi chú

- Tất cả logs có prefix `[API]`, `[SERVICE]`, hoặc `[REPO]` để dễ filter
- Level `INFO` cho flow chính
- Level `DEBUG` cho chi tiết
- Level `WARNING` cho các trường hợp bất thường nhưng không phải lỗi
- Level `ERROR` cho các lỗi nghiêm trọng

## 🚀 Cách chạy với logging

```bash
python run.py
```

Hoặc nếu dùng uvicorn trực tiếp:

```bash
uvicorn app.main:app --reload --log-level debug
```

