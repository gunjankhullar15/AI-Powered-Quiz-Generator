from pydantic import BaseModel, EmailStr, ConfigDict

class EmployeeBase(BaseModel):
    full_name: str
    emp_code: str

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    emp_id: int
    model_config = ConfigDict(from_attributes=True)