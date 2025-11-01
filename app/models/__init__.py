from app.models.employee import Employee
from app.models.test import Test
from app.models.weightage import Weightage
from app.models.questions import Question
from app.models.testAssignment import TestAssignment
from app.models.response import EmployeeResponse
from app.models.results import Result
from app.models.base import Base


__all__ = [
     "Base",
    "Employee",
    "Test",
    "Weightage",
    "Question",
    "TestAssignment",
    "EmployeeResponse",
    "Result"
]
