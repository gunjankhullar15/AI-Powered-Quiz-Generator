from pydantic import BaseModel, ConfigDict, computed_field
from datetime import datetime
from typing import Optional, Literal
from app.models.employee import Employee

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