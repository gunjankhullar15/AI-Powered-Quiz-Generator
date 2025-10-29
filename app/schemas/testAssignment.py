from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TestAssignmentBase(BaseModel):
    q_id: int
    emp_id: int



class TestAssignmentCreate(TestAssignmentBase):
    pass

class TestAssignmentResponse(TestAssignmentBase):
    ta_id: int
    model_config = ConfigDict(from_attributes=True)