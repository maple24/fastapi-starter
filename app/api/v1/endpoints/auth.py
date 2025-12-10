"""
Authentication endpoints
Handles user authentication, registration, and token management
"""

from datetime import timedelta

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import get_settings
from app.models.user import UserModel
from app.schemas.auth import Token, UserCreate, UserResponse
from app.schemas.user import User
from app.utils.ldap import (
    LDAPAuthenticationError,
    LDAPConnectionError,
    authenticate_ldap_user,
)
from app.utils.security import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_password_hash,
)

router = APIRouter()


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(user_data: UserCreate, settings=Depends(get_settings)):
    """
    Register a new user
    """
    # Check if user already exists (placeholder - implement with your database)
    # existing_user = await get_user_by_email(user_data.email)
    # if existing_user:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Email already registered"
    #     )

    # Hash password
    hashed_password = get_password_hash(user_data.password)

    # Create user (placeholder - implement with your database)
    user = UserModel(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        is_active=True,
    )

    # Save to database (placeholder)
    # user = await create_user(user)

    return UserResponse(
        id=1,  # placeholder
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        created_at="2024-01-01T00:00:00Z",  # placeholder
    )


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), settings=Depends(get_settings)
):
    """
    Login user and return access and refresh tokens
    Supports both LDAP authentication (if enabled) and local authentication
    """
    user_email = form_data.username

    # Try LDAP authentication if enabled
    if settings.LDAP_ENABLED:
        try:
            ldap_user = authenticate_ldap_user(
                form_data.username,
                form_data.password,
                settings
            )

            if ldap_user:
                # LDAP authentication successful
                user_email = ldap_user["email"]

                # Optionally, create or update user in local database here
                # user = await get_or_create_user_from_ldap(ldap_user)

                # Create tokens
                access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = create_access_token(
                    data={"sub": user_email}, expires_delta=access_token_expires
                )

                refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
                refresh_token = create_refresh_token(
                    data={"sub": user_email}, expires_delta=refresh_token_expires
                )

                return Token(
                    access_token=access_token,
                    refresh_token=refresh_token,
                    token_type="bearer"
                )
        except LDAPConnectionError:
            # Log LDAP connection error and fall back to local auth
            # logger.warning(f"LDAP connection error: {str(e)}")
            pass
        except LDAPAuthenticationError:
            # LDAP authentication failed, try local auth
            # logger.info(f"LDAP authentication failed: {str(e)}")
            pass

    # Fall back to local authentication
    # Authenticate user (placeholder - implement with your database)
    # user = await authenticate_user(form_data.username, form_data.password)
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect email or password",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )

    # Create tokens for local user
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        data={"sub": form_data.username}, expires_delta=refresh_token_expires
    )

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(current_user: User = Depends(get_current_user)):
    """
    Refresh access token using refresh token
    """
    # In a real application, you would validate the refresh token
    # and create a new access token
    settings = get_settings()

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.email}, expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        data={"sub": current_user.email}, expires_delta=refresh_token_expires
    )

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user information
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        created_at=current_user.created_at.isoformat() if current_user.created_at else "",
    )
