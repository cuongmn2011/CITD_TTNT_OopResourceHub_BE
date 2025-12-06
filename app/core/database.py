import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables từ file .env (cho local development)
load_dotenv()

# Lấy DATABASE_URL từ environment variable (ưu tiên)
# Nếu không có, sử dụng SQLite local (cho development)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./oop_resource.db")

# Vercel Postgres cung cấp DATABASE_URL với prefix postgres://
# SQLAlchemy 2.0+ yêu cầu postgresql:// thay vì postgres://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Cấu hình engine dựa trên loại database
if DATABASE_URL.startswith("sqlite"):
    # SQLite: connect_args cần thiết cho multi-threading trong FastAPI
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL: không cần connect_args đặc biệt
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Kiểm tra connection trước khi sử dụng
        pool_size=5,         # Số lượng connection trong pool
        max_overflow=10      # Số connection tối đa có thể tạo thêm
    )

# Tạo SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class để các Model kế thừa
Base = declarative_base()

# Dependency để lấy DB session (dùng trong Controller/API)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()