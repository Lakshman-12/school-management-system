from pydantic import BaseModel, ConfigDict, Field


class TeacherAssignmentCreate(BaseModel):
    teacher_id: int = Field(gt=0)
    class_id: int = Field(gt=0)
    subject_id: int = Field(gt=0)


class TeacherAssignmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    teacher_id: int
    class_id: int
    subject_id: int
    
    
    
class TeacherAssignmentDetailResponse(BaseModel):
    id: int
    teacher_id: int
    teacher_name: str | None = None
    class_name: str
    section: str
    academic_year: str
    subject_name: str