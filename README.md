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

### 4. Configure environment

**Create `.env` file from example:**
```bash
cp .env.example .env
```

**Edit `.env` file:**
```bash
# Local development với SQLite (default)
ENVIRONMENT=development
# DATABASE_URL sẽ mặc định là sqlite:///./oop_resource.db

# Hoặc dùng PostgreSQL local
ENVIRONMENT=development
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

**Note:** 
- `ENVIRONMENT=development` tự động tạo bảng khi khởi động
- `ENVIRONMENT=production` bỏ qua việc tạo bảng tự động

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
├── api/                           # API endpoints
│   └── v1/endpoints/
│       ├── category_api.py        # Category CRUD APIs
│       ├── topic_api.py           # Topic CRUD APIs
│       └── section_api.py         # Section CRUD APIs
├── application/                   # Business logic layer
│   ├── interfaces/                # Repository interfaces (DIP)
│   │   ├── category_repository_interface.py
│   │   ├── topic_repository_interface.py
│   │   └── section_repository_interface.py
│   └── services/                  # Service layer
│       ├── category_service.py
│       ├── topic_service.py
│       └── section_service.py
├── domain/                        # Core business domain
│   ├── models/                    # SQLAlchemy ORM models
│   │   ├── category.py            # Category entity
│   │   ├── topic.py               # Topic entity + related_topics
│   │   ├── section.py             # Section entity
│   │   └── __init__.py
│   └── schemas/                   # Pydantic DTOs
│       ├── category_schema.py
│       ├── topic_schema.py
│       └── section_schema.py
├── infrastructure/                # External services
│   └── repositories/              # Data access layer (SQLAlchemy)
│       ├── category_repository.py
│       ├── topic_repository.py
│       └── section_repository.py
└── core/                          # Core configuration
    └── database.py                # Database setup
```

## 📡 API Endpoints

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/categories/` | Create new category |
| GET | `/api/v1/categories/` | Get all categories (paginated) |
| GET | `/api/v1/categories/{id}` | Get category by ID |
| GET | `/api/v1/categories/slug/{slug}` | Get category by slug |
| PUT | `/api/v1/categories/{id}` | Update category |
| DELETE | `/api/v1/categories/{id}` | Delete category |

### Topics

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/topics/` | Create new topic |
| GET | `/api/v1/topics/` | Get all topics (paginated) |
| GET | `/api/v1/topics/{id}` | Get topic by ID |
| PUT | `/api/v1/topics/{id}` | Update topic |
| DELETE | `/api/v1/topics/{id}` | Delete topic |

### Sections

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/sections/` | Create new section |
| GET | `/api/v1/sections/` | Get all sections (paginated) |
| GET | `/api/v1/sections/{id}` | Get section by ID |
| GET | `/api/v1/sections/topic/{topic_id}` | Get all sections of a topic |
| PUT | `/api/v1/sections/{id}` | Update section |
| DELETE | `/api/v1/sections/{id}` | Delete section |

## 🚢 Deployment

### Deploy to Vercel

1. **Create Vercel Postgres database:**
   - Go to Vercel Dashboard → Storage → Create Database
   - Choose Postgres
   - Copy `DATABASE_URL` environment variable

2. **Add environment variables:**
   - Go to Project Settings → Environment Variables
   - Add: `DATABASE_URL` = (your Postgres connection string)
   - Add: `ENVIRONMENT` = `production`

3. **Create database tables (first time only):**
   
   **Option A - Temporary development mode:**
   - Temporarily set `ENVIRONMENT=development` in Vercel
   - Deploy once to auto-create tables
   - Then change back to `ENVIRONMENT=production`
   
   **Option B - Manual SQL (recommended for production):**
   - Connect to Vercel Postgres using psql or GUI client
   - Run the following SQL:
   ```sql
   CREATE TABLE categories (
       id SERIAL PRIMARY KEY,
       name VARCHAR UNIQUE NOT NULL,
       slug VARCHAR UNIQUE NOT NULL
   );
   
   CREATE TABLE topics (
       id SERIAL PRIMARY KEY,
       title VARCHAR UNIQUE NOT NULL,
       short_definition TEXT NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       category_id INTEGER NOT NULL REFERENCES categories(id)
   );
   
   CREATE TABLE sections (
       id SERIAL PRIMARY KEY,
       topic_id INTEGER NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
       order_index INTEGER NOT NULL,
       heading VARCHAR NOT NULL,
       content TEXT NOT NULL,
       image_url VARCHAR,
       code_snippet TEXT,
       language VARCHAR
   );
   
   CREATE TABLE related_topics_association (
       topic_id INTEGER REFERENCES topics(id),
       related_topic_id INTEGER REFERENCES topics(id),
       PRIMARY KEY (topic_id, related_topic_id)
   );
   
   CREATE INDEX idx_categories_slug ON categories(slug);
   CREATE INDEX idx_topics_title ON topics(title);
   CREATE INDEX idx_topics_category ON topics(category_id);
   CREATE INDEX idx_sections_topic ON sections(topic_id);
   ```

4. **Deploy:**
   ```bash
   git push origin develop  # or main
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

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `ENVIRONMENT` | Runtime environment (`development`, `production`, `staging`) | `development` | No |
| `DATABASE_URL` | Database connection string | `sqlite:///./oop_resource.db` | No |

**Important Notes:**
- `ENVIRONMENT=development`: Auto-creates database tables on startup (for local dev)
- `ENVIRONMENT=production`: Skips auto table creation (requires manual schema setup or migrations)
- When deploying to Vercel, set `ENVIRONMENT=production` in environment variables

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is part of CITD coursework.
