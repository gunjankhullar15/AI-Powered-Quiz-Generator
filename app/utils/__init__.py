from app.utils.database import async_engine, Base
from app.models.employee import Employee
from app.models.test import Test
from app.models.weightage import Weightage
from app.models.questions import Question
from app.models.testAssignment import TestAssignment
from app.models.response import EmployeeResponse
from app.models.results import Result

def init_db():
    # Create all tables
    Base.metadata.create_all(bind=async_engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()