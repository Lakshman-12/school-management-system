from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ParentCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    relationship: str | None = Field(default=None, max_length=50)
    phone: str = Field(min_length=5, max_length=20)
    email: EmailStr | None = None
    address: str | None = Field(default=None, max_length=255)
    user_id: int | None = None


class ParentUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    relationship: str | None = Field(default=None, max_length=50)
    phone: str | None = Field(default=None, min_length=5, max_length=20)
    email: EmailStr | None = None
    address: str | None = Field(default=None, max_length=255)
    is_active: bool | None = None


class ParentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int | None
    first_name: str
    last_name: str
    relationship: str | None
    phone: str
    email: str | None
    address: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class ParentListResponse(BaseModel):
    items: list[ParentResponse]
    page: int
    page_size: int
    total: int
    pages: int
