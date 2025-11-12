from app.services.llm_services import generate_llm_output
from app.services.weaviate_services import search_in_weaviate, clear_weaviate_data, client
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

        if topic == "":
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
 
 
        # if isinstance(search_results, list):
        #     combined_text = "\n".join(
        #         [res.get("content") or res.get("text") or "" for res in search_results if isinstance(res, dict)]
        #     )
        # else:
        #     combined_text = str(search_results)

         # Separate article and PDF content
        article_chunks = []
        pdf_chunks = []
        
        for res in search_results:
            if isinstance(res, dict):
                content = res.get("content", "")
                source = res.get("source", "")
                
                # Check if it's from article (has URL) or PDF (has filename)
                if "http" in str(source) or res.get("source_url"):
                    article_chunks.append(content)
                else:
                    pdf_chunks.append(content)
        
        article_text = "\n\n".join(article_chunks) if article_chunks else "No article content available."
        pdf_text = "\n\n".join(pdf_chunks) if pdf_chunks else "No PDF content available."
        
        logger.info(f"Article chunks: {len(article_chunks)}, PDF chunks: {len(pdf_chunks)}")
 
        #  Step 4: Generate questions
        raw_output = generate_llm_output(
            topic if topic else "All Content",
            article_text,
            pdf_text,
            mcq_questions,
            sch_questions,
            truefalse_questions,
            fillups_questions,
            total_people,
            #match_questions
        )

        clean_data = clean_llm_response(raw_output)
        output_dict = {}

        print("............................................")
        print(clean_data)


        # for key, value in clean_data["response"].items():
        #     if key.startswith("person"):
        #         # rename key with underscore instead of space
        #         person_key = key.replace(" ", "_")
        #         output_dict[person_key] = value

        response_data = clean_data.get("response", {})

        if "people" in response_data and isinstance(response_data["people"], list):
            for idx, person_data in enumerate(response_data["people"], start=1):
                person_key = f"person_{idx}"
                output_dict[person_key] = person_data
        else:
            for key, value in response_data.items():
                if key.startswith("person"):
                    person_key = key.replace(" ", "_")
                    output_dict[person_key] = value



        if len(output_dict) != total_people:
            return "Question are not generated properly"
 

        clear_status = clear_weaviate_data(client)
        logger.info(f"Weaviate cleanup status: {clear_status}")
        return output_dict
 
   
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))