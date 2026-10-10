from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.core.config import settings

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from app.modules.auth.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
)
from app.modules.auth.models import User
from app.modules.auth.repository import AuthRepository



class AuthService:

    def __init__(
        self,
        db: AsyncSession,
        repository: AuthRepository,
    ) -> None:
        self.db = db
        self.repository = repository

    async def register(
        self,
        data: RegisterRequest,
    ) -> User:
        existing_user = await self.repository.get_user_by_email(
            data.email)
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        hashed_password = hash_password(data.password)

        try:
            user = await self.repository.create_user(
                email=data.email,
                password_hash=hashed_password,
            )

            await self.db.commit()
            await self.db.refresh(user)

            return user

        except IntegrityError as exc:
            await self.db.rollback()
            raise ValueError("Email already registered") from exc

        except Exception:
            await self.db.rollback()
            raise
        
        
        
    async def login(
        self,
        data: LoginRequest,
    ) -> tuple[str, str]:

        user = await self.repository.get_user_by_email(
            data.email
        )

        if not user or not verify_password(
            data.password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        access_token = create_access_token(
            user_id=user.id,
            role=user.role.value,
        )

        refresh_token = create_refresh_token(
            user_id=user.id,
            role=user.role.value,
        )

        return access_token, refresh_token
        
        
            
    async def refresh_tokens(
        self,
        refresh_token: str,
    ) -> TokenResponse:

        # 1. Validate the refresh token
        try:
            payload = jwt.decode(
                refresh_token,
                settings.SECRET_KEY.get_secret_value(),
                algorithms=["HS256"],
            )

            user_id = payload.get("sub")
            token_type = payload.get("type")

            if user_id is None or token_type != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token",
                )

            user_id = int(user_id)

        except (JWTError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
            )

        # 2. Get user from database
        user = await self.repository.get_user_by_id(user_id)

        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        # 3. Generate new tokens
        access_token = create_access_token(
            user_id=user.id,
            role=user.role.value,
        )

        new_refresh_token = create_refresh_token(
            user_id=user.id,
            role=user.role.value,
        )

        # 4. Return tokens
        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
        )