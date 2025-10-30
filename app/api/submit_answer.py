from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.database import get_db
from app.services.evaluation import evaluating_user_answers
from app.models.results import Result
from datetime import datetime


router = APIRouter()

@router.post("/submit-answer/", description="Submit answers for evaluation")
async def submit_answer(user_answer : str, employe_id : int, test_id : int, db : AsyncSession = Depends(get_db)):
    
    try:
        # Example marks allocation, these could be dynamic or fetched from DB
        mcq_marks = 1
        truefalse_marks = 1
        fillups_marks = 1
        scenario_based_marks = 3

        user_marks = evaluating_user_answers(
            user_answer,
            mcq_marks,
            truefalse_marks,
            fillups_marks,
            scenario_based_marks
        )

        today_date = datetime.today()

        print(user_marks)

        # storing the result in the database
        new_result = Result(
            date=today_date,
            score=user_marks['Total Marks'],
            emp_id=employe_id,  # Example employee ID
            t_id=test_id     # Example test ID
        )

        db.add(new_result)
        await db.commit()
        await db.refresh(new_result)

        return {"your marks" : user_marks}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during answer submission: {str(e)}")