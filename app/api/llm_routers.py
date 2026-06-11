import json
import re
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.services.llm_services import generate_llm_output
from app.services.weaviate_services import search_in_weaviate
from app.logs.logger_config import setup_logger
from app.services.response_cleaner import clean_llm_response
from app.schemas.test import TestCreate
 
logger = setup_logger(__name__)
router = APIRouter()
 
@router.get("/output/")
def get_llm_output(
    topic: Optional[str] = Query(None, description="Enter the topic for which to generate test questions (ignored if useall_content=True)"),
    useall_content: Optional[bool] = Query(False, description="If True, use all content from Weaviate and ignore topic"),
    mcq_questions: int = Query(5, description="Number of MCQ questions"),
    sch_questions: int = Query(3, description="Number of Scenario-based questions"),
    truefalse_questions: int = Query(5, description="Number of True/False questions"),
    fillups_questions: int = Query(3, description="Number of Fill in the blanks questions"),
    total_people: int = Query(2, description="Total number of people")
    #match_questions: int = Query(3, description="Number of Match the following questions"
):
    """
    Fetch all Weaviate chunks related to the given topic or all content if useall_content=True.
    Each chunk represents ~300 words of relevant text. All chunks are combined
    into a single context for the LLM.
    """
    try:
        # Validation: Either topic or useall_content must be set
        if not topic and not useall_content:
            raise HTTPException(
                status_code=400,
                detail="Either 'topic' must be provided or 'useall_content' must be True."
            )
 
        if topic and useall_content:
            raise HTTPException(
                status_code=400,
                detail="'topic' and 'useall_content' cannot be used together."
            )
 
        try:
            if useall_content:
                logger.info("Fetching all PDF content from Weaviate")
                search_results = search_in_weaviate("*")   #  Fetch all content
                # print(search_results)
            else:
                logger.info(f"Fetching topic-specific chunks for topic: {topic}")
                search_results = search_in_weaviate(topic)
                # print(search_results)
 
            if not search_results or len(search_results) == 0:
                raise HTTPException(status_code=404, detail="No content found in Weaviate for the given query.")
 
            logger.info(f"Weaviate search returned {len(search_results)} results.")
 
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error during Weaviate search: {str(e)}")
 
 
        if isinstance(search_results, list):
            combined_text = "\n".join(
                [res.get("content") or res.get("text") or "" for res in search_results if isinstance(res, dict)]
            )
        else:
            combined_text = str(search_results)
 
        #  Step 4: Generate questions
        raw_output = generate_llm_output(
            topic if topic else "All Content",
            combined_text,
            mcq_questions,
            sch_questions,
            truefalse_questions,
            fillups_questions,
            total_people,
            #match_questions
        )

        clean_data = clean_llm_response(raw_output)
        output_dict = {}
        for key, value in clean_data["response"].items():
            if key.startswith("person"):
                # rename key with underscore instead of space
                person_key = key.replace(" ", "_")
                output_dict[person_key] = value

        if len(output_dict) != total_people:
            return "Question are not generated properly"

        # print(len(output_dict))
        # print(type(output_dict))
        # print(output_dict)

        # for key in output_dict:
        #   print(key)
 
        return clean_data
 
   
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))