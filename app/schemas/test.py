from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from datetime import datetime, timezone
from decimal import Decimal

class TestBase(BaseModel):
    topic: str
    test_name: str
    description: str
    due_date: datetime  # Should be timezone-aware
    no_of_mcq: int = 0
    no_of_short_ans: int = 0
    no_scenario_based: int = 0
    no_of_fill_blanks: int = 0
    no_of_true_false: int = 0
    duration: int
    max_marks: Decimal
    passing_marks: Decimal
    created_at: datetime  # Should be timezone-aware

    model_config = ConfigDict(from_attributes=True)

    @field_validator('due_date', 'created_at')
    @classmethod
    def ensure_timezone_aware(cls, v: datetime) -> datetime:
        if v.tzinfo is None or v.tzinfo.utcoffset(v) is None:
            raise ValueError("Datetime must be timezone-aware (e.g., include UTC offset).")
        return v

class TestCreate(TestBase):
    pass

class TestResponse(TestBase):
    t_id: int
    test_url: Optional[str] = None  # This will be present in response
    model_config = ConfigDict(from_attributes=True)
