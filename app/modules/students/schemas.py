from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field


class StudentCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    admission_number: str = Field(min_length=1, max_length=50)
    date_of_birth: date | None = None
    gender: str | None = Field(default=None, max_length=20)
    class_id: int
    parent_id: int


class StudentUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    admission_number: str | None = Field(default=None, min_length=1, max_length=50)
    date_of_birth: date | None = None
    gender: str | None = Field(default=None, max_length=20)
    class_id: int | None = None
    parent_id: int | None = None
    is_active: bool | None = None


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    admission_number: str
    date_of_birth: date | None
    gender: str | None
    class_id: int
    parent_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class StudentDetailResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    admission_number: str
    date_of_birth: date | None
    gender: str | None
    class_id: int
    class_name: str
    class_section: str
    class_academic_year: str
    parent_id: int
    parent_name: str
    parent_phone: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class StudentListResponse(BaseModel):
    items: list[StudentResponse]
    page: int
    page_size: int
    total: int
    pages: int
