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

# # @router.post("/submit-answers/{q_id}")
# async def submit_answers(
#     q_id: int,
#     db: AsyncSession = Depends(get_db)
# ):
#     """Submit answer for a specific question."""
    
#     try:
#         # Verify question exists
#         question_result = await db.execute(
#             select(Question).where(Question.q_id == q_id)
#         )
#         question = question_result.scalar_one_or_none()
        
#         if not question:
#             raise HTTPException(
#                 status_code=404,
#                 detail=f"Question with id {q_id} not found"
#             )
        
#         # Create employee response record
#         db_response = EmployeeResponse(
#             t_id=Test.t_id,
#             q_id=q_id,
#             emp_id=Employee.emp_id,
#             responses=EmployeeResponse.responses,
#             marks=0  # Will be calculated during evaluation
#         )
#         db.add(db_response)

#          # Commit changes
#         await db.commit()
#         await db.refresh(db_response)
        
#         return {
#             "message": "Answer submitted successfully",
#             "test_id": Test.t_id,
#             "emp_id": Employee.emp_id,
#             "question_id": q_id
#         }
        
#     except HTTPException:
#         await db.rollback()
#         raise
#     except Exception as e:
#         await db.rollback()
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error submitting answer: {str(e)}")