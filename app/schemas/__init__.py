from .employee import EmployeeBase, EmployeeCreate, EmployeeResponse
from .test import TestBase, TestCreate, TestResponse
from .weightage import WeightageBase, WeightageCreate, WeightageResponse
from .questions import QuestionBase, QuestionCreate, QuestionResponse
from .testAssignment import TestAssignmentBase, TestAssignmentCreate, TestAssignmentResponse
from .response import EmployeeResponseBase, EmployeeResponseCreate, EmployeeResponseResponse
from .result import ResultBase, ResultCreate, ResultResponse

__all__ = [
    # Employee
    "EmployeeBase", "EmployeeCreate", "EmployeeResponse",
    # Test
    "TestBase", "TestCreate", "TestResponse",
    # Weightage
    "WeightageBase", "WeightageCreate", "WeightageResponse",
    # Question
    "QuestionBase", "QuestionCreate", "QuestionResponse",
    # Test Assignment
    "TestAssignmentBase", "TestAssignmentCreate", "TestAssignmentResponse",
    # Employee Response
    "EmployeeResponseBase", "EmployeeResponseCreate", "EmployeeResponseResponse",
    # Result
    "ResultBase", "ResultCreate", "ResultResponse"
]