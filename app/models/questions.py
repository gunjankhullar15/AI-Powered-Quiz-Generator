from sqlalchemy import Column, Integer, String,Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Question(Base):
    __tablename__ = "questions"
    
    q_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    t_id = Column(Integer, ForeignKey("tests.t_id"), nullable=False)
    question_statement_options = Column(Text, nullable=False)
    assigned=Column(Boolean, default=False)
    
    # Relationships
    test = relationship("Test", back_populates="questions")
    employee_responses = relationship("EmployeeResponse", back_populates="question")