from sqlalchemy import Column, Integer, Text, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from app.utils.database import Base

class EmployeeResponse(Base):
    __tablename__ = "employee_responses"
    
    e_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    t_id = Column(Integer, ForeignKey("tests.t_id"), nullable=False)
    q_id = Column(Integer, ForeignKey("questions.q_id"), nullable=False)
    emp_id = Column(Integer, ForeignKey("employees.emp_id"), nullable=False)
    responses = Column(Text, nullable=True)
    marks = Column(DECIMAL(5, 2), default=0)
    
    # Relationships
    test = relationship("Test", back_populates="employee_responses")
    question = relationship("Question", back_populates="employee_responses")
    employee = relationship("Employee", back_populates="employee_responses")