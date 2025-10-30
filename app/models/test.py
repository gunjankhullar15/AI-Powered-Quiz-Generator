from sqlalchemy import Column, Integer, String, TIMESTAMP, DECIMAL, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from app.utils.database import Base
class Test(Base):
    __tablename__ = "tests"
    
    t_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    topic = Column(String(200), nullable=False)
    test_name = Column(String(150), nullable=False)
    test_url = Column(String(2083), nullable=True)
    description = Column(String(500), nullable=True)
    due_date = Column(TIMESTAMP(timezone=True), nullable=False)
    no_of_mcq = Column(Integer, default=0)
    no_scenario_based = Column(Integer, default=0)
    no_of_fill_blanks = Column(Integer, default=0)
    no_of_true_false = Column(Integer, default=0)
    duration = Column(Integer, nullable=False)
    max_marks = Column(DECIMAL(6, 2), nullable=False)
    total_questions = Column(Integer, nullable=False)
    passing_marks = Column(DECIMAL(5, 2), nullable=False)
    no_of_people=Column(Integer, default=0, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    # Business rule: Total questions should equal sum of all question types
    __table_args__ = (
        CheckConstraint('total_questions = no_of_mcq  + no_scenario_based + no_of_fill_blanks + no_of_true_false'),
        CheckConstraint('duration > 0'),
        CheckConstraint('max_marks > 0')
    )
    
    # Relationships
    questions = relationship("Question", back_populates="test")
  
    employee_responses = relationship("EmployeeResponse", back_populates="test")
    results = relationship("Result", back_populates="test")