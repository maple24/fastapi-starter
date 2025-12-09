# FastAPI Starter

A comprehensive FastAPI scaffolder with best practices, modern features, and production-ready configurations.

## 🚀 Features

- **Modern FastAPI Setup**: Latest FastAPI with async/await support
- **Authentication & Authorization**: JWT-based auth with refresh tokens and LDAP support
- **LDAP Integration**: Optional LDAP/Active Directory authentication with fallback to local auth
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
│       ├── database.py       # Database utilities
│       └── ldap.py           # LDAP authentication utilities
├── tests/                    # Test directory
├── main.py                   # Application entry point
├── pyproject.toml           # Project configuration
├── .env.example             # Environment variables template
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
   cp .env.example .env
   # Edit .env with your configuration
   ```

   **For LDAP authentication**, enable and configure LDAP settings in `.env`:
   ```bash
   LDAP_ENABLED=true
   LDAP_SERVER=ldap://your-ldap-server.com
   LDAP_BASE_DN=ou=users,dc=example,dc=com
   LDAP_USER_FILTER=(uid={username})
   # See .env.example for full LDAP configuration options
   ```

4. **Run the application**:
   ```bash
   # Development mode (recommended with UV)
   uv run python main.py

   # Or using uvicorn directly
   uv run uvicorn main:app --reload

   # Without UV
   python main.py
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
- `POST /api/v1/auth/login` - User login (supports LDAP if enabled)
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

## 🔐 LDAP Authentication

This starter supports LDAP/Active Directory authentication with automatic fallback to local authentication.

### Features

- **Flexible Authentication**: Try LDAP first, fall back to local database authentication
- **Multiple LDAP Servers**: Support for OpenLDAP, Active Directory, FreeIPA, and others
- **Secure Connection**: Optional SSL/TLS support
- **Customizable Mapping**: Configure LDAP attribute mapping for email and full name
- **Search Filters**: Flexible user search with customizable LDAP filters

### Configuration

All LDAP settings are configured via environment variables. See `.env.example` for detailed configuration options:

```bash
# Enable LDAP authentication
LDAP_ENABLED=true

# LDAP Server
LDAP_SERVER=ldap://ldap.example.com
LDAP_PORT=389
LDAP_USE_SSL=false

# Service account for user search
LDAP_BIND_DN=cn=admin,dc=example,dc=com
LDAP_BIND_PASSWORD=admin-password

# Search configuration
LDAP_BASE_DN=ou=users,dc=example,dc=com
LDAP_USER_FILTER=(uid={username})

# Attribute mapping
LDAP_ATTR_EMAIL=mail
LDAP_ATTR_FULLNAME=cn
```

### Common LDAP Filter Examples

```bash
# OpenLDAP (uid-based)
LDAP_USER_FILTER=(uid={username})

# Active Directory (sAMAccountName)
LDAP_USER_FILTER=(sAMAccountName={username})

# Email-based login
LDAP_USER_FILTER=(mail={username})

# Common name (cn)
LDAP_USER_FILTER=(cn={username})
```

### LDAP + Local Authentication Flow

1. User submits login credentials
2. If LDAP is enabled, attempt LDAP authentication first
3. If LDAP authentication succeeds, create JWT token
4. If LDAP fails or is disabled, try local database authentication
5. Return JWT token on successful authentication

### Testing LDAP Connection

You can test your LDAP configuration programmatically:

```python
from app.core.config import get_settings
from app.utils.ldap import test_ldap_connection

settings = get_settings()
if test_ldap_connection(settings):
    print("✅ LDAP connection successful")
else:
    print("❌ LDAP connection failed")
```

### LDAP Examples

The `.env.example` file includes complete configuration examples for:
- **OpenLDAP** with anonymous bind
- **Active Directory** with SSL
- **FreeIPA/Red Hat Directory Server**

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

# LDAP Configuration (if using LDAP authentication)
LDAP_ENABLED=true
LDAP_SERVER=ldaps://ldap.yourdomain.com
LDAP_PORT=636
LDAP_USE_SSL=true
LDAP_BIND_DN=cn=service_account,ou=service,dc=yourdomain,dc=com
LDAP_BIND_PASSWORD=your-ldap-bind-password
LDAP_BASE_DN=ou=users,dc=yourdomain,dc=com
LDAP_USER_FILTER=(uid={username})
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