from fastapi import APIRouter, Depends, HTTPException, status   
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.employee import EmployeeCreate
from fastapi import APIRouter, Depends, HTTPException, status   
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.utils.database import get_db
from app.models import Employee, Test

router = APIRouter(prefix="/instructions")

@router.post("/{test_id}")
async def get_instructions(
    test_id: int,
    emp : EmployeeCreate,
    db: AsyncSession = Depends(get_db)
):
    """Get test instructions for a specific employee and test."""
    
    # Fetch test details
    test_result = await db.execute(
        select(Test).where(Test.t_id == test_id)
    )
    test = test_result.scalar_one_or_none()
    
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found"
        )
    percentage= (test.passing_marks/test.max_marks)*100
    percentage=round(percentage,2)
    
    # Create instruction page
    instruction_page = f"""
 
Welcome to your assessment!
 
Please read the instructions carefully before you begin.
 
⏱ **Test Duration:** {test.duration} minutes
🧠 **Minimum Passing Score:** {percentage}%
 
### Test Structure:
- **Multiple Choice Questions (MCQs):** {test.no_of_mcq}
- **True/False Questions:** {test.no_of_true_false}
- **Fill in the Blanks:** {test.no_of_fill_blanks}
- **Scenario-Based Questions:** {test.no_scenario_based}

### Important Instructions:
1. You must attempt **all questions** in the test.
2. You **cannot skip** a question; you must have to attempt all the question.
3. In case of **internet or system interruption**, your test will be **automatically submitted**.
4. Please ensure a **stable internet connection** and attempt the test carefully.
 
✅ **Good luck with your test!**
"""
    emp=Employee(
        emp_code=emp.emp_code,
        full_name=emp.full_name
    )
    db.add(emp)
    await db.commit()

    return {"instructions": instruction_page}
