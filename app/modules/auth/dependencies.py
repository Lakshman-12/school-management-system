from typing import Annotated

from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import settings
from app.db.session import DB
from app.modules.auth.repository import AuthRepository
from app.modules.auth.models import User,UserRole


# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="/auth/login"
# )


# async def get_current_user(
#     token: Annotated[str, Depends(oauth2_scheme)],
#     db: DB,
# ) -> User:

#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )


from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_scheme = HTTPBearer()

async def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(bearer_scheme),
    ],
    db: DB,
) -> User:

    token = credentials.credentials
    
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=["HS256"],
        )

        user_id = payload.get("sub")
        token_type = payload.get("type")

        if user_id is None or token_type != "access":
            raise credentials_exception

        user_id = int(user_id)

    except (JWTError, ValueError):
        raise credentials_exception

    repository = AuthRepository(db)
    user = await repository.get_user_by_id(user_id)

    if user is None or not user.is_active:
        raise credentials_exception

    return user



def require_role(*allowed_roles: UserRole):
    async def role_checker(
        current_user: CurrentUser,
    ) -> User:

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )

        return current_user

    return role_checker






CurrentUser = Annotated[
    User,
    Depends(get_current_user),
]

AdminUser = Annotated[
    User,
    Depends(require_role(UserRole.ADMIN)),
]

TeacherUser = Annotated[
    User,
    Depends(require_role(UserRole.TEACHER)),
]