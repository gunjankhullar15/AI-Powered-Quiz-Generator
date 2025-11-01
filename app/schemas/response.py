from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from typing import Optional, Dict, Any

class EmployeeResponseBase(BaseModel):
    t_id: int
    q_id: int
    emp_id: int
    responses: Optional[str] = None
    marks: Decimal = 0

class EmployeeResponseCreate(EmployeeResponseBase):
    pass
class ResponseSchema(BaseModel):
    t_id: int
    emp_id: int
    responses: Dict[str,Any]

class EmployeeResponseResponse(EmployeeResponseBase):
    emp_id: int
    employee_name: str
    test_id: int
    score: Decimal
    
    model_config = ConfigDict(from_attributes=True)