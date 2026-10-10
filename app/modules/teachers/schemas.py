from pydantic import BaseModel, ConfigDict, Field,EmailStr



class AdminCreateTeacher(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)

    full_name: str = Field(min_length=2, max_length=100)
    qualification: str | None = Field(
        default=None,
        max_length=100,
    )
    phone: str | None = Field(
        default=None,
        max_length=15,
    )



class TeacherResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    full_name: str
    qualification: str | None
    phone: str | None
    
    
    
class TeacherListResponse(BaseModel):
    items: list[TeacherResponse]
    page: int
    page_size: int
    total: int
    pages: int
    
    
    
class TeacherSelfUpdate(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    phone: str | None = Field(
        default=None,
        max_length=15,
    )


class AdminTeacherUpdate(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    qualification: str | None = Field(
        default=None,
        max_length=100,
    )
    phone: str | None = Field(
        default=None,
        max_length=15,
    )