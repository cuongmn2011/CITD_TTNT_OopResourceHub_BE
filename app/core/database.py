from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Tên file database sẽ là oop_resource.db nằm ngay thư mục gốc
SQLALCHEMY_DATABASE_URL = "sqlite:///./oop_resource.db"

# connect_args={"check_same_thread": False} là BẮT BUỘC với SQLite trong FastAPI
# vì SQLite mặc định chỉ cho phép 1 luồng truy cập tại 1 thời điểm
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
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