 
from fastapi import APIRouter, Query, HTTPException
from app.services.llm_services import generate_llm_output
 
router = APIRouter()
 
@router.get("/output/")
def get_llm_output(topic: str = Query(..., description="Enter the query"),
                   results: str = Query(..., description="All the results"),
                   mcq_questions: int = Query(5, description="Number of MCQ questions"),
                   sch_questions: int = Query(3, description="Number of Scenario based questions"),
                   truefalse_questions: int = Query(5, description="Number of True/False questions"),
                   fillups_questions: int = Query(3, description="Number of Fill in the blanks questions"),
                    question_level: str = Query("hard", description="Level of questions"),
                    total_people: int = Query(2, description="Total number of people"),
                    match_questions: int = Query(3, description="Number of Match the following questions")):
    try:
        return generate_llm_output(topic, results, mcq_questions, sch_questions, truefalse_questions, fillups_questions, question_level, total_people, match_questions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))