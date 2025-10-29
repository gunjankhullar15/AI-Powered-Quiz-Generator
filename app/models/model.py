from sqlalchemy import Column, Integer, String,  Text, ForeignKey, TIMESTAMP, DECIMAL, DateTime, CheckConstraint, Enum
from sqlalchemy.orm import relationship
from app.database.database import Base

class Employee(Base):
    __tablename__ = "employees"
    
    emp_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    full_name = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    
    # Relationships
    test_assignments = relationship("TestAssignment", back_populates="employee")
    employee_responses = relationship("EmployeeResponse", back_populates="employee")
    results = relationship("Result", back_populates="employee")


class Question(Base):
    __tablename__ = "questions"
    
    q_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    t_id = Column(Integer, ForeignKey("tests.t_id"), nullable=False)
    question_statement_options = Column(Text, nullable=False)
    q_type = Column(String(50), nullable=False) #
    correct_answers = Column(Text, nullable=False)#
       
    # Relationships
    test = relationship("Test", back_populates="questions")
    employee_responses = relationship("EmployeeResponse", back_populates="question")


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



class Result(Base):
    __tablename__ = "results"
    
    r_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    date = Column(DateTime, nullable=False)
    score = Column(Integer, nullable=False)
    emp_id = Column(Integer, ForeignKey("employees.emp_id"), nullable=False)
    t_id = Column(Integer, ForeignKey("tests.t_id"), nullable=False)
    
    # Relationships
    employee = relationship("Employee", back_populates="results")
    test = relationship("Test", back_populates="results")



class Test(Base):
    __tablename__ = "tests"
    
    t_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    topic = Column(String(200), nullable=False)
    test_name = Column(String(150), nullable=False)
    test_url = Column(String(2083), nullable=True)
    description = Column(String(500), nullable=True)
    due_date = Column(TIMESTAMP(timezone=True), nullable=False)
    no_of_mcq = Column(Integer, default=0)
    no_of_short_ans = Column(Integer, default=0)
    no_scenario_based = Column(Integer, default=0)
    no_of_fill_blanks = Column(Integer, default=0)
    no_of_true_false = Column(Integer, default=0)
    duration = Column(Integer, nullable=False)
    max_marks = Column(DECIMAL(6, 2), nullable=False)
    total_questions = Column(Integer, nullable=False)
    passing_marks = Column(DECIMAL(5, 2), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    # Business rule: Total questions should equal sum of all question types
    __table_args__ = (
        CheckConstraint('total_questions = no_of_mcq + no_of_short_ans + no_scenario_based + no_of_fill_blanks + no_of_true_false'),
        CheckConstraint('duration > 0'),
        CheckConstraint('max_marks > 0')
    )
    
    # Relationships
    questions = relationship("Question", back_populates="test")
    test_assignments = relationship("TestAssignment", back_populates="test")
    employee_responses = relationship("EmployeeResponse", back_populates="test")
    results = relationship("Result", back_populates="test")



class TestAssignment(Base):
    __tablename__ = "test_assignments"
    
    ta_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    t_id = Column(Integer, ForeignKey("tests.t_id"), nullable=False)
    emp_id = Column(Integer, ForeignKey("employees.emp_id"), nullable=False)
    date = Column(DateTime, nullable=False)
    completion_status = Column(Enum('Completed', 'Not Completed', name='completion_status'), default='Not Completed')
    
    # Relationships
    test = relationship("Test", back_populates="test_assignments")
    employee = relationship("Employee", back_populates="test_assignments")



class Weightage(Base):
    __tablename__ = "weightages"
    
    w_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    question_type = Column(String(50), nullable=False, unique=True)  # Make unique
    weightage = Column(DECIMAL(4, 2), nullable=False)
    
    __table_args__ = (
        CheckConstraint('weightage > 0'),
    )
    
   