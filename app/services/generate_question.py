from app.services.llm_services import generate_llm_output, generate_for_batch
from app.services.weaviate_services import search_in_weaviate, clear_weaviate_data, client
from app.logs.logger_config import setup_logger
from app.services.response_cleaner import clean_llm_response
from fastapi import HTTPException
import time

logger = setup_logger(__name__)

BATCH_SIZE = 8

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


async def generating_question_from_llm_batched(topic: str,
                                               mcq_questions: int,
                                               sch_questions: int,
                                               truefalse_questions: int,
                                               fillups_questions: int,
                                               total_people: int):
    """
    Batched version - generates questions for multiple people in parallel batches
    Much faster for large numbers (50+ people)
    """
    try:
        start_time = time.time()
        useall_content = False

        if topic == "":
            useall_content = True
            
        # Validation
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
 
        # Fetch content from Weaviate (once for all batches)
        try:
            if useall_content:
                logger.info("Fetching all PDF content from Weaviate")
                search_results = search_in_weaviate("*")
            else:
                logger.info(f"Fetching topic-specific chunks for topic: {topic}")
                search_results = search_in_weaviate(topic)
 
            if not search_results or len(search_results) == 0:
                raise HTTPException(
                    status_code=404, 
                    detail="No content found in Weaviate for the given query."
                )
 
            logger.info(f"Weaviate search returned {len(search_results)} results.")
 
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error during Weaviate search: {str(e)}"
            )
 
        # Separate article and PDF content
        article_chunks = []
        pdf_chunks = []
        
        for res in search_results:
            if isinstance(res, dict):
                content = res.get("content", "")
                source = res.get("source", "")
                
                if "http" in str(source) or res.get("source_url"):
                    article_chunks.append(content)
                else:
                    pdf_chunks.append(content)
        
        article_text = "\n\n".join(article_chunks) if article_chunks else "No article content available."
        pdf_text = "\n\n".join(pdf_chunks) if pdf_chunks else "No PDF content available."
        
        logger.info(f"Article chunks: {len(article_chunks)}, PDF chunks: {len(pdf_chunks)}")
        logger.info(f"Starting batched generation for {total_people} people with batch size {BATCH_SIZE}")
        logger.info(f"Topic: {topic if topic else 'All Content'}")
        logger.info(f"Article content: {len(article_text)} characters")
        logger.info(f"PDF content: {len(pdf_text)} characters")
 

        # Process in batches
        batch_results = await generate_for_batch(
            topic=topic if topic else "All Content",
            article_content=article_text,
            pdf_content=pdf_text,
            mcq_questions=mcq_questions,
            sch_questions=sch_questions,
            truefalse_questions=truefalse_questions,
            fillups_questions=fillups_questions,
            total_people=total_people
        )

        # Check if batched generation was successful
        if batch_results.get("status") == "error":
            raise HTTPException(
                status_code=500,
                detail=batch_results.get("message", "Batch generation failed")
            )

        # Combine all batch results
        combined_results = batch_results.get("response", {})
        
        # Detailed logging of merged results
        logger.info("="*80)
        logger.info("VERIFYING MERGED JSON STRUCTURE")
        logger.info(f"Total persons in combined_results: {len(combined_results)}")
        logger.info(f"Person keys: {list(combined_results.keys())[:5]}...")
        
        if "people" in combined_results and isinstance(combined_results["people"], int):
            del combined_results["people"]

        if combined_results:
            sample_key = next(
                (k for k in combined_results.keys() if isinstance(combined_results[k], dict)), 
                None
            )
            if not sample_key:
                logger.error("No valid person structure found in combined_results")
                raise HTTPException(status_code=500, detail="Invalid merged JSON structure")
            sample_person = combined_results[sample_key]
            logger.info(f"Sample person structure (person: {sample_key}):")
            for question_type, questions in sample_person.items():
                if isinstance(questions, list):
                    logger.info(f"   - {question_type}: {len(questions)} questions")
                else:
                    logger.info(f"   - {question_type}: {questions}")
            
            # Verify format matches original
            expected_keys = ["all mcq questions", "all scenario questions", 
                           "all true/false questions", "all fill in the blanks questions"]
            actual_keys = list(sample_person.keys())
            
            logger.info(f"   Checking JSON format compatibility:")
            logger.info(f"   Expected format keys: {expected_keys}")
            logger.info(f"   Actual format keys: {actual_keys}")
            
            format_match = all(key in actual_keys for key in expected_keys)
            logger.info(f"   Format matches original: {'YES' if format_match else 'NO'}")
        
        logger.info("="*80)
        
        if len(combined_results) != total_people:
            logger.warning(
                f"Expected {total_people} people, but got {len(combined_results)} results"
            )
 
        # Clear Weaviate data
        clear_status = clear_weaviate_data(client)
        logger.info(f"Weaviate cleanup status: {clear_status}")
        
        end_time = time.time()
        total_time = end_time - start_time
        
        logger.info(f"Total generation completed in {total_time:.2f} seconds")
        
        # Return results with metadata
        return {
            "status": "success",
            "combined_results": combined_results,
            "successful": batch_results.get("successful", 0),
            "failed": batch_results.get("failed", 0),
            "total_batches": batch_results.get("total_batches", 0),
            "total_time_seconds": total_time
        }
 
    except Exception as e:
        logger.error(f"Error in batched question generation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))