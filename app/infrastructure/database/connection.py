from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.core.settings import get_settings

# Load environment variables từ file .env (cho local development)
load_dotenv()

# Get settings
settings = get_settings()
DATABASE_URL = settings.DATABASE_URL

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
