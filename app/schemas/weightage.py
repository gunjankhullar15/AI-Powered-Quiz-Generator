from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class WeightageBase(BaseModel):
    question_type: str
    weightage: Decimal

class WeightageCreate(WeightageBase):
    pass

class WeightageResponse(WeightageBase):
    w_id: int
    model_config = ConfigDict(from_attributes=True)