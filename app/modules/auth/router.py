from app.db.session import DB
from app.modules.auth.dependencies import CurrentUser
from fastapi import APIRouter, HTTPException,  status,  Request, Response


from app.modules.auth.repository import AuthRepository
from app.modules.auth.service import AuthService
from app.modules.auth.schemas import(
    RegisterRequest, 
    UserResponse, 
    TokenResponse, 
    LoginRequest,
    RefreshRequest
)

from fastapi import Depends
from app.modules.auth.dependencies import require_role
from app.modules.auth.models import User, UserRole



router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    data: RegisterRequest,
    db: DB,
) -> UserResponse:

    repository = AuthRepository(db)
    service = AuthService(db, repository)

    user = await service.register(data)

    return UserResponse.model_validate(user)




@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    db: DB,
    response: Response,
) -> TokenResponse:

    repository = AuthRepository(db)
    service = AuthService(db, repository)

    access_token, refresh_token = await service.login(data)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,      # True in production with HTTPS
        samesite="lax",
    )

    return TokenResponse(
        access_token=access_token,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_tokens(
    request: Request,
    db: DB,
):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
        )

    repository = AuthRepository(db)

    service = AuthService(
        db=db,
        repository=repository,
    )

    return await service.refresh_tokens(
        refresh_token=refresh_token
    )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CurrentUser):
    return current_user



@router.get("/admin-only")
async def admin_only(
    current_user: User = Depends(
        require_role(UserRole.ADMIN)
    ),
):
    return {
        "message": "Welcome, Admin!",
        "user_id": current_user.id,
        "role": current_user.role.value,
    }