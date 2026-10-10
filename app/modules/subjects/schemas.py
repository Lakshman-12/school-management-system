from pydantic import BaseModel, ConfigDict, Field


class SubjectCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )


class SubjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class SubjectUpdate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )