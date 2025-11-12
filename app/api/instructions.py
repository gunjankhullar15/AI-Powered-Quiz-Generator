from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_
from app.schemas.employee import EmployeeCreate
from app.utils.database import get_db
from app.models import Employee, Test, Question, TestAssignment

router = APIRouter(prefix="/instructions")


@router.post("/{test_id}")
async def register_employee_and_get_instructions(
    test_id: int,
    emp: EmployeeCreate,
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
    
    # Calculate passing percentage
    percentage = (test.passing_marks / test.max_marks) * 100
    percentage = round(percentage, 2)
    
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
4. **Exiting fullscreen mode will immediately submit your test.**
5. Please ensure a **stable internet connection** and attempt the test carefully.

✅ **Good luck with your test!**
"""
    
    # Check if employee already exists
    existing_emp = await db.execute(
        select(Employee).where(Employee.emp_code == emp.emp_code)
    )
    employee = existing_emp.scalar_one_or_none()
    
    if not employee:
        # Create new employee
        employee = Employee(
            emp_code=emp.emp_code,
            full_name=emp.full_name
        )
        db.add(employee)
        await db.commit()
        await db.refresh(employee)

     # Check if test is already assigned to this employee
    existing_assignment_result = await db.execute(
        select(TestAssignment)
        .join(Question)
        .where(
            and_(
                TestAssignment.emp_id == employee.emp_id,
                Question.t_id == test_id
            )
        )
    )
    existing_assignment = existing_assignment_result.scalar_one_or_none()

    if existing_assignment:
        # If already assigned, return the same assignment (no new assignment)
        return {
            "instructions": instruction_page,
            "emp_code": employee.emp_code,
            "test_id": test.t_id,
            "q_id": existing_assignment.q_id
        }

    question_result = await db.execute(
        select(Question)
        .where(Question.t_id == test_id, Question.assigned == False)
        .limit(1)
    )
    question = question_result.scalar_one_or_none()

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No available questions left to assign for this test."
        )

    # Create TestAssignment entry
    test_assignment = TestAssignment(
        q_id=question.q_id,
        emp_id=employee.emp_id
    )
    db.add(test_assignment)

    # Mark question as assigned
    await db.execute(
        update(Question)
        .where(Question.q_id == question.q_id)
        .values(assigned=True)
    )
    
    await db.commit()

    return {
        "instructions": instruction_page,
        "emp_code": employee.emp_code,
        "test_id": test.t_id,
        "q_id": question.q_id,
        "title": test.test_name,
        "duration": test.duration,
    }