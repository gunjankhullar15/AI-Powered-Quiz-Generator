from sqlalchemy import Column, Integer, String, DECIMAL, CheckConstraint
from app.utils.database import Base

class Weightage(Base):
    __tablename__ = "weightages"
    
    w_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    question_type = Column(String(50), nullable=False, unique=True)  # Make unique
    weightage = Column(DECIMAL(4, 2), nullable=False)
    
    __table_args__ = (
        CheckConstraint('weightage > 0'),
    )
    
   