from pydantic import BaseModel, ConfigDict, Field


class ClassCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    section: str = Field(min_length=1, max_length=10)
    academic_year: str = Field(min_length=4, max_length=20)


class ClassResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    section: str
    academic_year: str


class ClassUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    section: str | None = Field(default=None, min_length=1, max_length=10)
    academic_year: str | None = Field(default=None, min_length=4, max_length=20)