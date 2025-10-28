from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.utils.database import Base

class TestAssignment(Base):
    __tablename__ = "test_assignments"
    
    ta_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    t_id = Column(Integer, ForeignKey("tests.t_id"), nullable=False)
    emp_id = Column(Integer, ForeignKey("employees.emp_id"), nullable=False)
    date = Column(DateTime, nullable=False)
   
    
    # Relationships
    test = relationship("Test", back_populates="test_assignments")
    employee = relationship("Employee", back_populates="test_assignments")