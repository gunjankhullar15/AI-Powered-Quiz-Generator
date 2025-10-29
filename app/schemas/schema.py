from pydantic import BaseModel, EmailStr, ConfigDict, computed_field, field_validator
from decimal import Decimal
from typing import Optional, Literal
from datetime import datetime, timezone
from app.models.model import Employee


class EmployeeBase(BaseModel):
    full_name: str
    department: str
    email: EmailStr

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    emp_id: int
    model_config = ConfigDict(from_attributes=True)



class QuestionBase(BaseModel):
    t_id: int
    question_statement_options: str
    q_type: str
    correct_answers: str

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(QuestionBase):
    q_id: int
    model_config = ConfigDict(from_attributes=True)



class EmployeeResponseBase(BaseModel):
    t_id: int
    q_id: int
    emp_id: int
    responses: Optional[str] = None
    marks: Decimal = 0

class EmployeeResponseCreate(EmployeeResponseBase):
    pass

class EmployeeResponseResponse(EmployeeResponseBase):
    e_id: int
    model_config = ConfigDict(from_attributes=True)




class ResultBase(BaseModel):
    date: datetime
    score: int
    emp_id: int
    t_id: int 
    passing_marks: int 

class ResultCreate(ResultBase):
    pass

class ResultResponse(ResultBase):
    r_id: int

    @computed_field
    def status(self) -> Literal["Pass", "Fail"]:
        """Dynamically calculate pass/fail status"""
        return "Pass" if self.score >= self.passing_marks else "Fail"
    model_config = ConfigDict(from_attributes=True)



class TestBase(BaseModel):
    topic: str
    test_name: str
    description: str
    due_date: datetime  # Should be timezone-aware
    no_of_mcq: int = 0
    no_of_short_ans: int = 0
    no_scenario_based: int = 0
    no_of_fill_blanks: int = 0
    no_of_true_false: int = 0
    duration: int
    max_marks: Decimal
    passing_marks: Decimal
    created_at: datetime  # Should be timezone-aware

    model_config = ConfigDict(from_attributes=True)

    @field_validator('due_date', 'created_at')
    @classmethod
    def ensure_timezone_aware(cls, v: datetime) -> datetime:
        if v.tzinfo is None or v.tzinfo.utcoffset(v) is None:
            raise ValueError("Datetime must be timezone-aware (e.g., include UTC offset).")
        return v

class TestCreate(TestBase):
    pass

class TestResponse(TestBase):
    t_id: int
    test_url: Optional[str] = None  # This will be present in response
    model_config = ConfigDict(from_attributes=True)



class TestAssignmentBase(BaseModel):
    t_id: int
    emp_id: int
    date: datetime
    completion_status: str = 'Not Completed'

class TestAssignmentCreate(TestAssignmentBase):
    pass

class TestAssignmentResponse(TestAssignmentBase):
    ta_id: int
    model_config = ConfigDict(from_attributes=True)


class WeightageBase(BaseModel):
    question_type: str
    weightage: Decimal

class WeightageCreate(WeightageBase):
    pass

class WeightageResponse(WeightageBase):
    w_id: int
    model_config = ConfigDict(from_attributes=True)