from app.services.llm_services import generate_llm_output
from app.services.weaviate_services import search_in_weaviate
from app.logs.logger_config import setup_logger
from app.services.response_cleaner import clean_llm_response
from fastapi import HTTPException

logger = setup_logger(__name__)

def generating_question_from_llm(topic : str,
                                 mcq_questions : int,
                                 sch_questions : int,
                                 truefalse_questions : int,
                                 fillups_questions : int,
                                 total_people : int):
    try:
        useall_content = False

        if topic == None:
            useall_content = True
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
                print(search_results)
            else:
                logger.info(f"Fetching topic-specific chunks for topic: {topic}")
                search_results = search_in_weaviate(topic)
                print(search_results)
 
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
 
        return output_dict
 
   
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))