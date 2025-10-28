from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.schemas.response import EmployeeResponseResponse
from app.models.response import EmployeeResponse
from app.models.employee import Employee
from app.utils.database import get_db

router = APIRouter(prefix="/employees")

@router.get(
    "/get-candidates/{test_id}",  
    description="Get all candidates who took a specific test"
)
async def get_candidates(test_id: int, db: AsyncSession = Depends(get_db)):
    # Query with eager loading of employee relationship
    query = (
        select(EmployeeResponse)
        .options(selectinload(EmployeeResponse.employee))
        .join(Employee, EmployeeResponse.emp_id == Employee.emp_id)
        .where(EmployeeResponse.t_id == test_id)
    )
    
    result = await db.execute(query)
    candidates = result.scalars().all()
    
    if not candidates:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No candidates found for the given test ID"
        )
    
    candidates_list = [
        {
            "employee_id": candidate.emp_id,
            "employee_name": candidate.employee.full_name,
            "test_id": candidate.t_id,
            "score": candidate.marks,
        }
        for candidate in candidates
    ]
    
    return candidates_list