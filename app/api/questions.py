from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Question, EmployeeResponse, Employee, Test
from app.utils.database import get_db
from app.schemas.questions import Questiondata

router = APIRouter(prefix="/questions")

@router.post("/start-test", description="Get questions for a specific test and employee")  
async def get_questions(ques: Questiondata, db: AsyncSession = Depends(get_db)):
    
    result = await db.execute(select(Question).where(Question.q_id == ques.q_id))
    questions = result.scalar_one_or_none()
    
    # Check if questions exist BEFORE using it
    if not questions:
        raise HTTPException(status_code=404, detail="Questions not found.")
    
    questions_data = [
        {
            "test_id": questions.t_id,
            "q_id": questions.q_id,
            "emp_code": ques.emp_code,
            "question_text": questions.question_statement_options,
        }
    ]
    
    return questions_data