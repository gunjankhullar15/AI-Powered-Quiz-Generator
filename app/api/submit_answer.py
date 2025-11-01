from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.utils.database import get_db
from app.services.evaluation import evaluating_user_answers
from app.models.results import Result
from app.models.test import Test
from app.models import Employee
from datetime import datetime
from app.schemas.response import ResponseSchema
import json

router = APIRouter()

@router.post("/submit-answer/", description="Submit answers for evaluation")
async def submit_answer(result: ResponseSchema, db: AsyncSession = Depends(get_db)):
    
    try:
        # Fetch test details first to verify it exists
        test_result = await db.execute(
            select(Test).where(Test.t_id == result.t_id)
        )
        test = test_result.scalar_one_or_none()
        
        if not test:
            raise HTTPException(
                status_code=404,
                detail=f"Test with t_id {result.t_id} not found."
            )
        
        # Verify employee exists
        employee_result = await db.execute(
            select(Employee).where(Employee.emp_id == result.emp_id)
        )
        employee = employee_result.scalar_one_or_none()
        
        if not employee:
            raise HTTPException(
                status_code=404,
                detail=f"Employee with emp_id {result.emp_id} not found. Please complete the instructions step first."
            )
        
        # Convert responses dict to string for the LLM
        responses = result.responses
        
        # # If responses is already a dict, convert it to a JSON string
        # if isinstance(responses, dict):
        #     responses_str = json.dumps(responses)
        # elif isinstance(responses, str):
        #     if not responses.strip():
        #         raise HTTPException(status_code=400, detail="Responses cannot be empty")
        #     responses_str = responses
        # else:
        #     raise HTTPException(status_code=400, detail="Invalid responses format")
        
        # Pass the string to evaluating_user_answers
        user_marks = evaluating_user_answers(
            responses,  # Pass as string
            mcq_marks=1,
            truefalse_marks=1,
            fillups_marks=1,
            scenario_based_marks=3
        )

        today_date = datetime.today()
        total_marks_obtained = user_marks
        
        # Check if result already exists for this employee and test
        existing_result = await db.execute(
            select(Result).where(
                Result.emp_id == result.emp_id,
                Result.t_id == result.t_id
            )
        )
        existing = existing_result.scalar_one_or_none()
        
        if existing:
            # Update existing result
            existing.score = total_marks_obtained  # Fixed: removed trailing comma
            existing.date = today_date
            await db.commit()
            await db.refresh(existing)
        else:
            # Create new result
            new_result = Result(
                date=today_date,
                score=total_marks_obtained,  # Fixed: use extracted value
                emp_id=employee.emp_id,
                t_id=result.t_id
            )
            db.add(new_result)
            await db.commit()
            await db.refresh(new_result)

        percentage = (total_marks_obtained / test.max_marks) * 100
        
        result_data = {
            "full_name": employee.full_name,
            "emp_code": employee.emp_code,
            "score": total_marks_obtained,
            "percentage": f"{round(percentage, 2)}%",
            "total_marks": test.max_marks,
            "status": "Pass" if total_marks_obtained >= test.passing_marks else "Fail",
            "detailed_marks": user_marks
        }

        return result_data

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during answer submission: {str(e)}")