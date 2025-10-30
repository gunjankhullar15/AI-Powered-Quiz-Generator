from pydantic import BaseModel, ConfigDict

class QuestionBase(BaseModel):
    t_id: int
    question_statement_options: str
    assigned: bool = False

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(BaseModel):
    total_answers: int
    test_id: int
    emp_id: int
    question_id: int
    model_config = ConfigDict(from_attributes=True)