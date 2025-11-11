from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Result(Base):
    __tablename__ = "results"
    
    r_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    date = Column(DateTime, nullable=False)
    score = Column(Integer, nullable=False)
    emp_id = Column(Integer, ForeignKey("employees.emp_id"), nullable=False)
    t_id = Column(Integer, ForeignKey("tests.t_id"), nullable=False)
    attempted= Column(Integer, nullable=False, default=0)
    
    # Relationships
    employee = relationship("Employee", back_populates="results")
    test = relationship("Test", back_populates="results")