# FastAPI Starter

A comprehensive FastAPI scaffolder with best practices, modern features, and production-ready configurations.

## 🚀 Features

- **Modern FastAPI Setup**: Latest FastAPI with async/await support
- **Authentication & Authorization**: JWT-based auth with refresh tokens
- **Database Integration**: SQLModel with async PostgreSQL/SQLite support
- **API Documentation**: Auto-generated OpenAPI docs with Swagger UI
- **Security**: CORS, trusted hosts, rate limiting, and security headers
- **Validation**: Pydantic v2 schemas for request/response validation
- **Logging**: Structured logging with Loguru
- **Testing**: Pytest with async support and test utilities
- **Code Quality**: Ruff, Black, MyPy, and pre-commit hooks
- **Configuration**: Environment-based config with Pydantic Settings
- **Health Checks**: Comprehensive health monitoring endpoints
- **Middleware**: Custom middleware for logging, timing, and rate limiting

## 📁 Project Structure

```
fastapi-starter/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── health.py          # Health check endpoints
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py      # Main API router
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── auth.py    # Authentication endpoints
│   │           ├── users.py   # User management endpoints
│   │           └── items.py   # Sample CRUD endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── app.py            # FastAPI app factory
│   │   ├── config.py         # Configuration management
│   │   └── middleware.py     # Custom middleware
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py           # User database model
│   │   └── item.py           # Item database model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py           # Authentication schemas
│   │   ├── user.py           # User schemas
│   │   └── item.py           # Item schemas
│   └── utils/
│       ├── __init__.py
│       ├── security.py       # Security utilities
│       └── database.py       # Database utilities
├── tests/                    # Test directory
├── main.py                   # Application entry point
├── pyproject.toml           # Project configuration
├── .env.template            # Environment variables template
└── README.md
```

## 🛠️ Setup

### Prerequisites

- Python 3.13+
- UV package manager (recommended) or pip

### Installation

1. **Clone or use this template**:
   ```bash
   git clone <your-repo-url>
   cd fastapi-starter
   ```

2. **Install dependencies**:
   ```bash
   # Using UV (recommended)
   uv sync

   # Or using pip
   pip install -e .
   pip install -e ".[dev]"
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.template .env
   # Edit .env with your configuration
   ```

4. **Run the application**:
   ```bash
   # Development mode
   python main.py

   # Or using uvicorn directly
   uvicorn main:app --reload
   ```

5. **Visit the API documentation**:
   - Swagger UI: http://localhost:8000/api/v1/docs
   - ReDoc: http://localhost:8000/api/v1/redoc
   - Health Check: http://localhost:8000/health

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py
```

## 🔧 Development

### Code Quality

```bash
# Format code
black app tests

# Lint code
ruff check app tests

# Type checking
mypy app

# Run all quality checks
ruff check app tests && black --check app tests && mypy app
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

## 📊 API Endpoints

### Health & Status
- `GET /health` - Basic health check
- `GET /health/detailed` - Detailed system information
- `GET /ping` - Simple ping endpoint

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user info

### Users
- `GET /api/v1/users/` - List users (admin only)
- `POST /api/v1/users/` - Create user (admin only)
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user (admin only)

### Items (Sample CRUD)
- `GET /api/v1/items/` - List items with pagination and search
- `POST /api/v1/items/` - Create new item
- `GET /api/v1/items/{item_id}` - Get item by ID
- `PUT /api/v1/items/{item_id}` - Update item
- `DELETE /api/v1/items/{item_id}` - Delete item

## 🐳 Docker Support

### Quick Start with Docker

1. **Build and run with docker-compose**:
   ```bash
   # Development environment with live reload
   docker-compose -f docker-compose.dev.yml up --build

   # Production environment
   docker-compose up --build
   ```

2. **Or build and run manually**:
   ```bash
   # Build the image
   docker build -t fastapi-starter .

   # Run the container
   docker run -p 8000:8000 fastapi-starter
   ```

### Docker Configuration Files

- `Dockerfile` - Multi-stage production-ready image
- `docker-compose.yml` - Production setup with PostgreSQL, Redis, and Nginx
- `docker-compose.dev.yml` - Development setup with live reload
- `.dockerignore` - Files to exclude from Docker build context
- `nginx.conf` - Nginx reverse proxy configuration

### Environment-Specific Docker Commands

```bash
# Development with live reload
docker-compose -f docker-compose.dev.yml up --build

# Production with all services (app, db, redis, nginx)
docker-compose up --build

# Production without nginx (if you have external reverse proxy)
docker-compose up --build app db redis

# Run only the database for local development
docker-compose up db

# View logs
docker-compose logs -f app
```

### Docker Development Helper

Use the `docker-dev.py` script for easier Docker operations:

```bash
# Start development environment
python docker-dev.py dev --build --logs

# Start production environment
python docker-dev.py prod --build

# Database operations
python docker-dev.py db start
python docker-dev.py db shell
python docker-dev.py db reset

# View logs
python docker-dev.py logs app --follow

# Open shell in container
python docker-dev.py shell app

# Stop all services
python docker-dev.py stop

# Clean up
python docker-dev.py clean --all
```

### Docker Environment Variables

The Docker setup uses the following key environment variables:

- `ENVIRONMENT` - Set to `development` or `production`
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key (change in production!)
- `BACKEND_CORS_ORIGINS` - Allowed CORS origins
- `ALLOWED_HOSTS` - Allowed host headers

## 🚀 Deployment

### Environment Variables for Production

Make sure to set these environment variables in production:

```bash
ENVIRONMENT=production
SECRET_KEY=your-super-secret-key-min-32-chars
DATABASE_URL=postgresql://user:pass@host:5432/db
BACKEND_CORS_ORIGINS=https://yourdomain.com
ALLOWED_HOSTS=yourdomain.com
ENABLE_DOCS=false  # Disable docs in production
```

### Database Migration

```bash
# Create database tables
python -c "from app.utils.database import create_db_and_tables; create_db_and_tables()"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and quality checks
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Useful Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://pydantic.dev/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [UV Package Manager](https://github.com/astral-sh/uv)