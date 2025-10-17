from pydantic import BaseModel, ConfigDict

class QuestionBase(BaseModel):
    t_id: int
    question_statement_options: str
    q_type: str
    correct_answers: str

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(QuestionBase):
    q_id: int
    model_config = ConfigDict(from_attributes=True)