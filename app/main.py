import os

from fastapi import FastAPI

from app.api.v1.endpoints import category_api, section_api, topic_api, related_topic_association
from app.infrastructure.database import Base, engine

# Chỉ tạo bảng tự động khi chạy local development
# Production nên dùng Alembic migration hoặc tạo schema thủ công
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
if ENVIRONMENT == "development":
    Base.metadata.create_all(bind=engine)
    print(f"[{ENVIRONMENT}] Database tables created/verified")
else:
    print(f"[{ENVIRONMENT}] Skipping auto table creation")

app = FastAPI(title="OOP Resource Hub API")

# Đăng ký Router
app.include_router(topic_api.router, prefix="/api/v1/topics", tags=["Topics"])
app.include_router(
    category_api.router, prefix="/api/v1/categories", tags=["Categories"]
)
app.include_router(section_api.router, prefix="/api/v1/sections", tags=["Sections"])
app.include_router(
    related_topic_association.router, prefix="/api/v1/related-topics", tags=["Related Topics"]
)


@app.get("/")
def root():
    return {
        "message": "OOP Resource Hub API is running successfully!",
        "version": "1.0.0",
        "docs": "/docs"
    }
