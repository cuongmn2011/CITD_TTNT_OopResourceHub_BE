# CITD_TTNT_OopResourceHub_BE

OopResourceHub is a dedicated web application designed to help students and developers quickly search, discover, and organize learning materials related to Object-Oriented Programming (OOP) principles and practices.

## 🚀 Tech Stack

- **Framework**: FastAPI 0.123.8 (async, high-performance)
- **ORM**: SQLAlchemy 2.0.44 (with eager loading optimization)
- **Database**: PostgreSQL (Neon Database)
- **Validation**: Pydantic v2 (type-safe schemas)
- **Server**: Uvicorn (ASGI server)
- **Architecture**: Clean Architecture with DIP (Dependency Inversion Principle)
- **Deployment**: Google Cloud Run (containerized deployment)

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

**Create `.env` file:**
```bash
cp .env.example .env
```

**Edit `.env` file with your Neon PostgreSQL credentials:**
```bash
ENVIRONMENT=development
DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
```

**Get Neon Database URL:**
1. Sign up at [Neon](https://neon.tech)
2. Create a new project
3. Copy the connection string from dashboard
4. Paste it into your `.env` file

**Note:** 
- Database URL is **required** - the application will not start without it
- Both development and production use PostgreSQL (no SQLite support)

### 5. Run server

**Windows (PowerShell):**
```powershell
# Set environment variables and run
$env:DATABASE_URL="postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require"
$env:ENVIRONMENT="development"
python run.py
```

**Linux/Mac:**
```bash
# Option 1: Export then run
export DATABASE_URL="postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require"
export ENVIRONMENT="development"
python run.py

# Option 2: Use python-dotenv (automatically loads .env file)
python run.py
```

Server sẽ chạy tại: http://127.0.0.1:8000

- API Documentation: http://127.0.0.1:8000/docs
- Alternative docs: http://127.0.0.1:8000/redoc

**Note:** 
- Make sure your `.env` file exists and contains valid DATABASE_URL
- The app uses `python-dotenv` to automatically load `.env` file on startup
- If you see "DATABASE_URL environment variable is required!" error, check your `.env` file

## 🏗️ Project Structure

```
app/
├── api/                           # API endpoints layer
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
├── core/                          # Core application layer
│   ├── __init__.py                # Core exports
│   ├── settings.py                # App configuration & environment variables
│   ├── exceptions.py              # Custom exception classes
│   └── constants.py               # Application-wide constants
├── domain/                        # Core business domain
│   ├── models/                    # SQLAlchemy ORM models
│   │   ├── __init__.py            # Model exports
│   │   ├── category.py            # Category entity
│   │   ├── topic.py               # Topic entity + related_topics
│   │   └── section.py             # Section entity
│   └── schemas/                   # Pydantic DTOs
│       ├── category_schema.py     # Category request/response schemas
│       ├── topic_schema.py        # Topic request/response schemas
│       └── section_schema.py      # Section request/response schemas
└── infrastructure/                # External services & data access
    ├── database/                  # Database configuration
    │   ├── __init__.py            # Database exports
    │   └── connection.py          # SQLAlchemy engine, session & Base
    └── repositories/              # Data access layer (SQLAlchemy)
        ├── category_repository.py
        ├── topic_repository.py
        └── section_repository.py
```

### Architecture Principles

**Clean Architecture Layers:**
1. **API Layer** (`api/`) - HTTP endpoints, request/response handling
2. **Application Layer** (`application/`) - Business logic, use cases
3. **Domain Layer** (`domain/`) - Entities, value objects, business rules
4. **Infrastructure Layer** (`infrastructure/`) - External concerns (DB, APIs)
5. **Core Layer** (`core/`) - Cross-cutting concerns (config, exceptions)

**Key Design Patterns:**
- **Dependency Inversion Principle (DIP)**: Services depend on repository interfaces, not implementations
- **Dependency Injection**: Repositories injected into services via constructors
- **Repository Pattern**: Abstraction over data access
- **Service Layer Pattern**: Business logic separated from controllers

## ✨ Key Features

- **RESTful API** with full CRUD operations
- **Clean Architecture** with clear separation of concerns
- **Dependency Inversion** using repository interfaces
- **Comprehensive Error Handling** with detailed error messages
- **Eager Loading** for optimized database queries (joinedload)
- **Input Validation** using Pydantic v2 schemas
- **Auto-generated API Documentation** (Swagger UI & ReDoc)
- **Environment-based Configuration** (development/production)
- **PostgreSQL Database** with connection pooling for production workloads
- **Auto Database Schema Creation** on first startup

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

### Deploy to Google Cloud Run

**Prerequisites:**
- Google Cloud SDK installed
- Docker (optional - only needed for local Docker builds)
- Google Cloud project with billing enabled

**Quick Deploy:**

1. **Setup Google Cloud:**
   ```bash
   # Login to Google Cloud
   gcloud auth login
   
   # Set your project
   gcloud config set project YOUR_PROJECT_ID
   
   # Enable required APIs
   gcloud services enable run.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   ```

2. **Deploy using the deployment script:**
   
   **Windows (PowerShell):**
   ```powershell
   .\deploy.ps1
   ```
   
   **Linux/Mac:**
   ```bash
   bash deploy.sh
   ```
   
   Or deploy manually:
   ```bash
   gcloud run deploy oopresourcehub-api \
     --source . \
     --region asia-southeast1 \
     --allow-unauthenticated \
     --port 8000 \
     --set-env-vars ENVIRONMENT=production,DATABASE_URL="your_neon_database_url"
   ```

3. **Access your deployed API:**
   ```bash
   # Get service URL
   gcloud run services describe oopresourcehub-api \
     --region asia-southeast1 \
     --format='value(status.url)'
   ```

**Important Notes:**
- Database tables are automatically created on first startup
- Use Neon PostgreSQL for production database
- `deploy.ps1` and `deploy.sh` files contain your database credentials and are git-ignored
- See `DEPLOY_MANUAL.md` for detailed deployment instructions

### Database Setup

**Using Neon PostgreSQL (Recommended):**

1. Create account at [Neon](https://neon.tech)
2. Create a new project and database
3. Copy the connection string
4. Use it in your deployment command or `.env` file

Database tables are automatically created when the application starts for the first time.

## 🔧 Development

### Error Handling

All API endpoints include comprehensive error handling:

- **404 Not Found**: Resource không tồn tại
- **400 Bad Request**: Validation errors, duplicate resources
- **422 Unprocessable Entity**: Business logic validation failures
- **500 Internal Server Error**: Unexpected errors (with detailed messages in response)

Custom exceptions are defined in `app/core/exceptions.py`:
- `ResourceNotFoundException`
- `DuplicateResourceException`
- `ValidationException`

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
| `DATABASE_URL` | PostgreSQL connection string | None | **Yes** |

**Important Notes:**
- `DATABASE_URL` is **required** - application will fail to start without it
- Use Neon PostgreSQL for both development and production
- Database tables are automatically created on first startup
- Settings are centrally managed in `app/core/settings.py` using the Settings class
- Use `get_settings()` function to access configuration throughout the application

**Example DATABASE_URL formats:**
```bash
# Neon PostgreSQL (recommended)
DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require

# Local PostgreSQL
DATABASE_URL=postgresql://username:password@localhost:5432/database_name

# Google Cloud SQL
DATABASE_URL=postgresql://user:password@/dbname?host=/cloudsql/project:region:instance
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is part of CITD coursework.
