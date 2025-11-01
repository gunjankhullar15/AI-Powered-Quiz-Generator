from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base

class Employee(Base):
    __tablename__ = "employees"
    
    emp_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    full_name = Column(String(100), nullable=False)
    emp_code = Column(String(50), unique=True, nullable=False)
    
    # Relationships
    test_assignments = relationship("TestAssignment", back_populates="employee")
    employee_responses = relationship("EmployeeResponse", back_populates="employee")
    results = relationship("Result", back_populates="employee")