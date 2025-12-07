# CITD_TTNT_OopResourceHub_BE

OopResourceHub is a dedicated web application designed to help students and developers quickly search, discover, and organize learning materials related to Object-Oriented Programming (OOP) principles and practices.

## 🚀 Tech Stack

- **Framework**: FastAPI 0.123.8
- **ORM**: SQLAlchemy 2.0.44
- **Database**: SQLite (local) / PostgreSQL (production)
- **Validation**: Pydantic v2
- **Server**: Uvicorn

## 📦 Installation

### 1. Clone repository

```bash
git clone https://github.com/cuongmn2011/CITD_TTNT_OopResourceHub_BE.git
cd CITD_TTNT_OopResourceHub_BE
```

### 2. Create virtual environment

```bash
python -m venv venv
```

**Windows:**
```powershell
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure database

**Local development (SQLite):**
- Database tự động tạo file `oop_resource.db`
- Không cần cấu hình gì thêm

**Production (PostgreSQL):**
- Copy file `.env.example` thành `.env`
- Cập nhật `DATABASE_URL` với connection string của bạn:

```bash
cp .env.example .env
# Edit .env file
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

### 5. Run server

```bash
python -m run
```

Server sẽ chạy tại: http://127.0.0.1:8000

- API Documentation: http://127.0.0.1:8000/docs
- Alternative docs: http://127.0.0.1:8000/redoc

## 🏗️ Project Structure

```
app/
├── api/                    # API endpoints
│   └── v1/endpoints/
│       └── topic_api.py    # Topic CRUD APIs
├── application/            # Business logic layer
│   ├── interfaces/         # Repository interfaces
│   └── services/           # Service layer
├── domain/                 # Core business domain
│   ├── models/             # Database models
│   └── schemas/            # Pydantic schemas
├── infrastructure/         # External services
│   └── repositories/       # Data access layer
└── core/                   # Core configuration
    └── database.py         # Database setup
```

## 📡 API Endpoints

### Topics

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/topics/` | Create new topic |
| GET | `/api/v1/topics/` | Get all topics (paginated) |
| GET | `/api/v1/topics/{id}` | Get topic by ID |
| PUT | `/api/v1/topics/{id}` | Update topic |
| DELETE | `/api/v1/topics/{id}` | Delete topic |

## 🚢 Deployment

### Deploy to Vercel

1. **Create Vercel Postgres database:**
   - Go to Vercel Dashboard → Storage → Create Database
   - Choose Postgres
   - Copy `DATABASE_URL` environment variable

2. **Add environment variable:**
   - Go to Project Settings → Environment Variables
   - Add: `DATABASE_URL` = (your Postgres connection string)

3. **Deploy:**
   ```bash
   git push origin main
   ```

Vercel will automatically deploy your app!

### Alternative Platforms

- **Render.com**: Great for Python backends, free tier available
- **Railway.app**: Easy setup with automatic PostgreSQL
- **Heroku**: Classic choice with managed Postgres

## 🔧 Development

### Database Migrations (Future)

Consider using Alembic for production migrations:

```bash
pip install alembic
alembic init migrations
```

### Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./oop_resource.db` |

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is part of CITD coursework.
