from pydantic import BaseModel, ConfigDict
from datetime import datetime

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