from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import TestCreate
from app.models import Test
from app.utils.database import get_db

router = APIRouter(prefix="/tests")  # Add this line



@router.post("/create-test")
async def create_test(test: TestCreate, db: AsyncSession = Depends(get_db)):
    total_questions = (
        test.no_of_mcq
        + test.no_of_short_ans
        + test.no_scenario_based
        + test.no_of_fill_blanks
        + test.no_of_true_false
    )

    if test.duration <= 0:
        raise HTTPException(status_code=400, detail="Duration must be greater than zero.")
    if test.max_marks <= 0:
        raise HTTPException(status_code=400, detail="Max marks must be greater than zero.")

    new_test = Test(
        topic=test.topic,
        test_name=test.test_name,
        due_date=test.due_date,
        no_of_mcq=test.no_of_mcq,
        no_of_short_ans=test.no_of_short_ans,
        no_scenario_based=test.no_scenario_based,
        no_of_fill_blanks=test.no_of_fill_blanks,
        no_of_true_false=test.no_of_true_false,
        duration=test.duration,
        max_marks=test.max_marks,
        total_questions=total_questions,  # calculated here
        passing_marks=test.passing_marks,
        created_at=test.created_at,
    )

    db.add(new_test)
    await db.commit()
    await db.refresh(new_test)
    return new_test

@router.get("/get-test/{test_id}")
async def get_test(test_id: int, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    
    result = await db.execute(select(Test).where(Test.t_id== test_id))
    test = result.scalar_one_or_none()
    
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    return test

@router.get("/get-all-tests")
async def get_all_tests(db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    
    result = await db.execute(select(Test))
    tests = result.scalars().all()
    

    tests_list = [
        {
            "description": test.description,
            "t_id": test.t_id,
            "test_name": test.test_name,
            "due_date": test.due_date,
            "test_url": test.test_url
        }
        for test in tests
    ]
    
    return tests_list

