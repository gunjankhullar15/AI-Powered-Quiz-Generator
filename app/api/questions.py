from ast import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas import QuestionResponse
from app.models import Question,EmployeeResponse,Employee,Test
from app.utils.database import get_db

router=APIRouter(prefix="/questions")

@router.get("/{id}")
async def get_questions(id: int,db: AsyncSession=Depends(get_db)):

    result= await db.execute(select(Question).where(Question.t_id==id))
    questions = result.scalar_one_or_none()

    if not questions:
        raise HTTPException(status_code=404,details="Questions not found.")
    return questions
