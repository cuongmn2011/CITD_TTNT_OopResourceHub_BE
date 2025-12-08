from fastapi import FastAPI
from app.core.database import engine, Base
from app.api.v1.endpoints import topic_api, category_api

# Tạo bảng trong DB (chỉ chạy dev, product nên dùng Alembic migration)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="OOP Resource Hub API")

# Đăng ký Router
app.include_router(topic_api.router, prefix="/api/v1/topics", tags=["Topics"])
app.include_router(category_api.router, prefix="/api/v1/categories", tags=["Categories"])

@app.get("/")
def root():
    return {"message": "Server is running..."}
