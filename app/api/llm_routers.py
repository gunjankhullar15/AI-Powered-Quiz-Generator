# from fastapi import APIRouter, Query, HTTPException
# from app.services.llm_services import generate_llm_output

# router = APIRouter()

# @router.get("/output/")
# def get_llm_output(topic: str = Query(..., description="Enter the query"),
#                    results: str = Query(..., description="All the results"),
#                    mcq_questions: int = Query(5, description="Number of MCQ questions"),
#                    sch_questions: int = Query(3, description="Number of Scenario based questions"),
#                    truefalse_questions: int = Query(5, description="Number of True/False questions"),
#                    fillups_questions: int = Query(3, description="Number of Fill in the blanks questions"),
#                     question_level: str = Query("hard", description="Level of questions"),
#                     total_people: int = Query(2, description="Total number of people")):
#     try:
#         return generate_llm_output(topic, results, mcq_questions, sch_questions, truefalse_questions, fillups_questions, question_level, total_people)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# import json
# from fastapi import APIRouter, Query, HTTPException
# from app.services.llm_services import generate_llm_output

# router = APIRouter()

# @router.get("/output/")
# def get_llm_output(
#     topic: str = Query(..., description="Enter the query"),
#     results: str = Query(..., description="All the results"),
#     mcq_questions: int = Query(5, description="Number of MCQ questions"),
#     sch_questions: int = Query(3, description="Number of Scenario based questions"),
#     truefalse_questions: int = Query(5, description="Number of True/False questions"),
#     fillups_questions: int = Query(3, description="Number of Fill in the blanks questions"),
#     question_level: str = Query("hard", description="Level of questions"),
#     total_people: int = Query(2, description="Total number of people")
# ):
#     try:
#         raw_output = generate_llm_output(
#             topic, results, mcq_questions, sch_questions,
#             truefalse_questions, fillups_questions,
#             question_level, total_people
#         )

#         # 🧩 Convert stringified JSON into a Python dict
#         if isinstance(raw_output, dict) and "response" in raw_output:
#             try:
#                 raw_output["response"] = json.loads(raw_output["response"])
#             except json.JSONDecodeError:
#                 pass  # if it’s already valid JSON or malformed, skip

#         return raw_output

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# import json
# from fastapi import APIRouter, Query, HTTPException
# from app.services.llm_services import generate_llm_output
# from app.services.weaviate_services import search_in_weaviate

# router = APIRouter()

# @router.get("/output/")
# def get_llm_output(
#     topic: str = Query(..., description="Enter the topic for the test / questions"),
#     mcq_questions: int = Query(5, description="Number of MCQ questions"),
#     sch_questions: int = Query(3, description="Number of Scenario-based questions"),
#     truefalse_questions: int = Query(5, description="Number of True/False questions"),
#     fillups_questions: int = Query(3, description="Number of Fill in the blanks questions"),
#     question_level: str = Query("hard", description="Level of questions"),
#     total_people: int = Query(2, description="Total number of people"),
#     limit: int = Query(3, description="Number of relevant chunks to retrieve from Weaviate")
# ):
       
#     try:
#         # 1️⃣ Use `topic` itself as the search query to fetch relevant chunks
#         try:
#             search_results = search_in_weaviate(topic, limit)
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Error during search: {str(e)}")

#         # 2️⃣ Combine retrieved chunks into a single text context
#         if isinstance(search_results, list):
#             combined_text = "\n".join(
#                 [res.get("text", "") for res in search_results if isinstance(res, dict)]
#             )
#         else:
#             combined_text = str(search_results)

#         # 3️⃣ Generate questions via the LLM using the combined context
#         raw_output = generate_llm_output(
#             topic,
#             combined_text,
#             mcq_questions,
#             sch_questions,
#             truefalse_questions,
#             fillups_questions,
#             question_level,
#             total_people
#         )

#         # 4️⃣ If the returned output has a “response” field as a JSON string, parse it
#         if isinstance(raw_output, dict) and "response" in raw_output:
#             try:
#                 raw_output["response"] = json.loads(raw_output["response"])
#             except json.JSONDecodeError:
#                 pass  # leave it as is if parsing fails

#         return raw_output

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

import json
import re
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.services.llm_services import generate_llm_output
from app.services.weaviate_services import search_in_weaviate

router = APIRouter()

@router.get("/output/")
def get_llm_output(
    topic: Optional[str] = Query(None, description="Enter the topic for which to generate test questions (ignored if useall_content=True)"),
    useall_content: Optional[bool] = Query(False, description="If True, use all content from Weaviate and ignore topic"),
    mcq_questions: int = Query(5, description="Number of MCQ questions"),
    sch_questions: int = Query(3, description="Number of Scenario-based questions"),
    truefalse_questions: int = Query(5, description="Number of True/False questions"),
    fillups_questions: int = Query(3, description="Number of Fill in the blanks questions"),
    total_people: int = Query(2, description="Total number of people"),
    match_questions: int = Query(3, description="Number of Match the following questions"
)):
    """
    Fetch all Weaviate chunks related to the given topic or all content if useall_content=True.
    Each chunk represents ~300 words of relevant text. All chunks are combined
    into a single context for the LLM.
    """
    try:
        # ✅ Validation: Either topic or useall_content must be set
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

        # ✅ Step 1: Decide what to search
        if useall_content:
            query = ""  # Fetch everything
        else:
            query = topic

        # ✅ Step 2: Fetch from Weaviate
        try:
            search_results = search_in_weaviate(query)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error during Weaviate search: {str(e)}")

        # ✅ Step 3: Combine chunks into a single text context
        if isinstance(search_results, list):
            combined_text = "\n".join(
                [res.get("text", "") for res in search_results if isinstance(res, dict)]
            )
        else:
            combined_text = str(search_results)

        # ✅ Step 4: Generate questions
        raw_output = generate_llm_output(
            topic if topic else "All Content",
            combined_text,
            mcq_questions,
            sch_questions,
            truefalse_questions,
            fillups_questions,
            total_people,
            match_questions
        )

        # ✅ Step 5: Parse JSON safely
        if isinstance(raw_output, dict) and "response" in raw_output:
            cleaned_response = raw_output["response"]

            # 🔹 Remove Markdown backticks and language hints
            cleaned_response = re.sub(r"```(json)?", "", cleaned_response).strip()

            # 🔹 Attempt to parse JSON safely
            try:
                parsed_response = json.loads(cleaned_response)
                raw_output["response"] = parsed_response
            except json.JSONDecodeError:
                # If parsing fails, try extracting only JSON part
                match = re.search(r"\{.*\}", cleaned_response, re.DOTALL)
                if match:
                    try:
                        raw_output["response"] = json.loads(match.group(0))
                    except Exception:
                        pass  # fallback to text
                else:
                    raw_output["response"] = cleaned_response  # leave as text


        return raw_output

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


