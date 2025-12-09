"""
Security utilities for authentication and authorization
"""

from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings
from app.schemas.auth import TokenData
from app.schemas.user import User

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token"""
    settings = get_settings()
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT refresh token"""
    settings = get_settings()
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> TokenData | None:
    """Verify and decode a JWT token"""
    try:
        settings = get_settings()
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        email = payload.get("sub")
        token_type_claim = payload.get("type")
        if not isinstance(email, str) or email is None or token_type_claim != token_type:
            return None
        return TokenData(email=email)
    except JWTError:
        return None


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get the current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(token)
    if token_data is None:
        raise credentials_exception

    # In a real application, you would get the user from the database
    # user = await get_user_by_email(token_data.email)
    # if user is None:
    #     raise credentials_exception

    # For now, return a mock user
    # Use a valid email for testing if token_data.email is invalid
    valid_email = token_data.email if "@" in str(token_data.email) else "test@example.com"
    return User(
        id=1,
        email=valid_email,
        full_name="Mock User",
        is_active=True,
        is_superuser=True,  # Grant superuser for testing
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get the current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get the current active superuser"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


async def authenticate_user(email: str, password: str) -> User | None:
    """Authenticate a user with email and password"""
    # In a real application, you would get the user from the database
    # and verify the password
    # user = await get_user_by_email(email)
    # if not user:
    #     return None
    # if not verify_password(password, user.hashed_password):
    #     return None
    # return user

    # For now, return a mock user for demonstration
    if email == "test@example.com" and password == "testpassword":
        return User(
            id=1,
            email=email,
            full_name="Test User",
            is_active=True,
            is_superuser=True,  # Grant superuser for testing
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
    return None
