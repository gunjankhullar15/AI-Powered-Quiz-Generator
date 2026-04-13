#from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
import os
import json
import time
import asyncio
import math
from dotenv import load_dotenv
from app.logs.logger_config import setup_logger
from app.services.response_cleaner import clean_llm_response

# Configuration
BATCH_SIZE = 12  # Process 8 people at a time
MAX_RETRIES = 2  # Number of retries for failed batches

logger = setup_logger(__name__)
 
def generate_llm_output(topic: str,
                        article_content: str,
                        pdf_content: str,
                        mcq_questions: int,
                        sch_questions: int,
                        truefalse_questions: int,
                        fillups_questions: int,
                        total_people: int
                        #match_questions: int
                        ):
 
    load_dotenv()  # Load environment variables from .env file
    logger.info("Initializing LLM model...")
    model = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),  #  move this to .env
        model="gpt-4o-mini",
        temperature=0,
        model_kwargs={"response_format": {"type": "json_object"}}
    )
    logger.info("OpenAI model initialized successfully.")
 
    mcq_n_questions = mcq_questions
    n_people = total_people
    # topic = "rag"
    sch_n_questions = sch_questions
    truefalse_n_questions = truefalse_questions
    fillups_n_questions = fillups_questions
    #match_n_questions = match_questions    
   
   
   
    unified_prompt = f"""
You are an expert question generator specializing in multiple formats of assessment questions.  
Your task is to create the following types of questions for **{n_people} different people** based on the given content:
 
- **{mcq_n_questions} MCQs**
- **{sch_n_questions} scenario-based questions**
- **{truefalse_n_questions} true/false questions**
- **{fillups_n_questions} fill-in-the-blanks questions**
 
 
---
 
### Context:
Topic: {topic}
 
**ARTICLE CONTENT:**
{article_content}

**PDF/DOCUMENT CONTENT:**
{pdf_content}


**CRITICAL REQUIREMENT**: 
- For EACH person, Try to balance questions between ARTICLE and PDF content. BUT if PDF content is insufficient, generate all remaining questions from the ARTICLE.
- If content seems insufficient, paraphrase, expand, or logically derive additional questions.
- If there are {mcq_n_questions} MCQs, generate {mcq_n_questions // 2} from article and {mcq_n_questions // 2} from PDF.
- If there are {sch_n_questions} scenarios, generate {sch_n_questions // 2} from article and {sch_n_questions // 2} from PDF.
- If there are {truefalse_n_questions} true/false, generate {truefalse_n_questions // 2} from article and {truefalse_n_questions // 2} from PDF.
- If there are {fillups_n_questions} fill-ups, generate {fillups_n_questions // 2} from article and {fillups_n_questions // 2} from PDF.
- This 50-50 split is MANDATORY for each person.

Level of difficulty: **Easy**
 
---
 
### Output Instructions:
1. Generate **unique** questions for each person — no repetition between people.
2. The **output must be valid JSON only** (no markdown, no explanations outside JSON).
3. Follow the **exact JSON structure** shown below.
4. All string values must be wrapped in **double quotes**.
5. Include accurate **answers** for MCQs, True/False, and Fill in the Blanks questions only (not for scenario-based questions)
6. Skip any section if there’s insufficient data — do not leave blank or null fields.
7. Ensure that questions are content-based only — do not generate questions related to author names, page numbers, indices, or other metadata.
8. Each person MUST have equal questions from article and PDF content.
---
 
### Output JSON Format Example:
 
  {{
    "people": 1,
  
    "person 1": {{
    "all mcq questions": [
      {{
        "question": "What is the primary function of inductive bias in a learning algorithm?",
        "option 1": "To reduce the complexity of the hypothesis space",
        "option 2": "To increase the accuracy of the learner's predictions",
        "option 3": "To define the set of assumptions sufficient to deduce conclusions",
        "option 4": "To minimize training errors",
        "answer": "To reduce the complexity of the hypothesis space",
      
      }}
    ],
  
  
    "all scenario questions": [
      {{
        "question": "Imagine a company wants to use AI to predict employee turnover. What data should they collect and why?"
      }}
    ],
  
  
    "all true/false questions": [
      {{
        "question": "Supervised learning requires labeled data.",
        "option 1": "True",
        "option 2": "False",
        "answer": "True",
        
      }}
    ],
  
  
    "all fill in the blanks questions": [
      {{
        "question": "In machine learning, ________ is used to evaluate the performance of a model.",
        "answer": "cross-validation",

      }}
    ],
  
  }}
}}

 
---
 
### Requirements per Question Type:
 
**1. MCQs**
- Create {mcq_n_questions} MCQs per person.
- Each MCQ should have 4 options, one correct answer.
- Generate {mcq_n_questions // 2} questions from ARTICLE CONTENT.
- Generate {mcq_n_questions // 2} questions from PDF CONTENT.


 
**2. Scenario-based Questions**
- Create {sch_n_questions} scenario-based questions per person.
- Each should present a real-world problem and ask for an applicable concept or solution.
- Generate {sch_n_questions // 2} questions from ARTICLE CONTENT.
- Generate {sch_n_questions // 2} questions from PDF CONTENT.


 
**3. True/False Questions**
- Create {truefalse_n_questions} per person.
- Include two options ("True", "False"), a correct answer.
- Generate {truefalse_n_questions // 2} questions from ARTICLE CONTENT.
- Generate {truefalse_n_questions // 2} questions from PDF CONTENT.


 
**4. Fill in the Blanks**
- Create {fillups_n_questions} per person.
- Include one blank, the correct answer.
- Generate {fillups_n_questions // 2} questions from ARTICLE CONTENT.
- Generate {fillups_n_questions // 2} questions from PDF CONTENT.
- The questions must be generated only from the important content provided above — do not create questions from random or irrelevant lines.
 
 
 
---
 
### Final Instruction:
Return only the **final structured JSON** for all people — each containing all five question types.  
Do **not** include anything outside the JSON.
"""
 
   
    logger.info("Sending prompt to LLM...")
    response1 = model.invoke(unified_prompt)
    logger.info("LLM response received.")
    print("response1:", response1.content)
    return {"response": response1.content}


async def generate_for_batch(
    topic: str,
    article_content: str,
    pdf_content: str,
    mcq_questions: int,
    sch_questions: int,
    truefalse_questions: int,
    fillups_questions: int,
    total_people: int
):
    """
    Generate questions for all people in batches of 8, processed in parallel.
    Automatically divides total_people into batches.
    """
    try:
        load_dotenv()
        total_batches = math.ceil(total_people / BATCH_SIZE)
        logger.info(f"Total people: {total_people}, Batch size: {BATCH_SIZE}, Total batches: {total_batches}")

        combined_results = {}

        async def process_single_batch(batch_index: int):
            """Handles one batch of 8 people"""
            batch_num = batch_index + 1
            start_person_num = batch_index * BATCH_SIZE + 1
            end_person_num = min(start_person_num + BATCH_SIZE - 1, total_people)
            people_in_batch = end_person_num - start_person_num + 1

            logger.info(f"Starting Batch {batch_num}: People {start_person_num}-{end_person_num}")

            model = ChatOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                model="gpt-4o-mini",
                temperature=0,
                model_kwargs={"response_format": {"type": "json_object"}}
            )

            # Calculate splits for each question type
            mcq_from_article = mcq_questions // 2
            mcq_from_pdf = mcq_questions - mcq_from_article
            
            sch_from_article = sch_questions // 2
            sch_from_pdf = sch_questions - sch_from_article
            
            tf_from_article = truefalse_questions // 2
            tf_from_pdf = truefalse_questions - tf_from_article
            
            fillup_from_article = fillups_questions // 2
            fillup_from_pdf = fillups_questions - fillup_from_article



            unified_prompt = f"""
You are an expert question generator specializing in multiple formats of assessment questions.  
Your task is to create the following types of questions for **{people_in_batch} different people** based on the given content:

- **{mcq_questions} MCQs per person**
- **{sch_questions} scenario-based questions per person**
- **{truefalse_questions} true/false questions per person**
- **{fillups_questions} fill-in-the-blanks questions per person**

---
### Context:
Topic: {topic}

**ARTICLE CONTENT:**
{article_content}

**PDF/DOCUMENT CONTENT:**
{pdf_content}


---

### CRITICAL INSTRUCTION - BALANCED SOURCE USAGE:
You MUST generate questions from BOTH the Article Content AND the PDF Content.
DO NOT generate all questions from only the PDF or only the Article.

**MANDATORY DISTRIBUTION PER PERSON:**
- MCQs: Generate {mcq_from_article} questions from ARTICLE + {mcq_from_pdf} questions from PDF = {mcq_questions} total
- Scenarios: Generate {sch_from_article} questions from ARTICLE + {sch_from_pdf} questions from PDF = {sch_questions} total
- True/False: Generate {tf_from_article} questions from ARTICLE + {tf_from_pdf} questions from PDF = {truefalse_questions} total
- Fill-ups: Generate {fillup_from_article} questions from ARTICLE + {fillup_from_pdf} questions from PDF = {fillups_questions} total

You MUST use concepts, information, and terminology from BOTH sources.


---

### CRITICAL REQUIREMENTS:

1. **EXACT COUNTS REQUIRED:**
   - Each person must have EXACTLY {mcq_questions} MCQ questions
   - Each person must have EXACTLY {sch_questions} scenario questions
   - Each person must have EXACTLY {truefalse_questions} true/false questions
   - Each person must have EXACTLY {fillups_questions} fill-in-the-blank questions

2. **Content Sources:**
   - Draw questions from BOTH the article content AND PDF content
   - Mix questions naturally from both sources
   - DO NOT split or separate by source - just generate the required total number

3. **Uniqueness:**
   - Each person must have completely unique questions
   - No repetition of questions between different people
   - Questions can be similar in concept but must be worded differently
   - IMPORTANT: Each test must have SUBSTANTIALLY different questions, not just minor wording changes
   - Example: Don't just change "What is the main goal" to "What is the primary goal"
   - Instead, ask about different aspects: goals, characteristics, advantages, disadvantages, use cases, limitations

4. **Quality Standards:**
   - Questions must be based on TECHNICAL CONTENT ONLY, not metadata
   - STRICTLY FORBIDDEN: Questions about author names, publishers, page numbers, table of contents, prefaces, introductions, acknowledgments, feedback forms, contact information, document structure, UI feedback mechanisms, portal navigation icons, help features, or software interface elements
   - FORBIDDEN QUESTION PATTERNS (apply to ANY content):
     * "What is the goal of [Publisher/Author/Company Name]?"
     * "Where can you send feedback?"
     * "What email/contact method is provided?"
     * "Who wrote/created/authored this?"
     * "Which icon/button allows you to [perform UI action]?"
     * "How do you navigate to the [UI element]?"
     * Questions about table of contents, chapter organization, or document structure
   - ONLY ask questions about the CORE SUBJECT MATTER (the technical/educational content being taught)
   - Fill-in-the-blanks must replace SPECIFIC TECHNICAL TERMS that have only ONE correct answer
   - FORBIDDEN fill-blank patterns:
     * Blanks where the answer word appears in the question itself (circular reasoning)
     * Generic adjectives like "important", "main", "key", "best", "good", "primary"
     * Vague descriptors that could have multiple valid answers
   - REQUIRED fill-blank patterns:
     * Specific terminology, formulas, names of concepts, protocols, or methods
     * Technical specifications, exact values, or precise definitions
     * Terms that require knowledge of the specific content to answer
   - Blanks must NOT be guessable without reading the content
   - Level of difficulty: **Easy**
   
5. **CRITICAL: Avoid Common MCQ Pitfalls:**
   - DO NOT use "Both option X and option Y" as an answer choice
   - DO NOT create "all of the above" or "none of the above" options
   - Each question should test ONE concept clearly
   - All options should be grammatically parallel
   - Distractors should be plausible but clearly incorrect for someone who knows the material

6. **If Content is Limited:**
   - If you cannot find enough unique concepts, rephrase existing concepts differently
   - Paraphrase and reword information creatively
   - NEVER reduce the question count - always generate the exact number required

   
---
 
### Output JSON Format Example:

{{
  "people": {people_in_batch},

  "person 1": {{
    "all mcq questions": [
      {{
        "question": "What is the primary function of inductive bias in a learning algorithm?",
        "option 1": "To reduce the complexity of the hypothesis space",
        "option 2": "To increase the accuracy of the learner's predictions",
        "option 3": "To define the set of assumptions sufficient to deduce conclusions",
        "option 4": "To minimize training errors",
        "answer": "To reduce the complexity of the hypothesis space"
      }}
    ],

    "all scenario questions": [
      {{
        "question": "Imagine a company wants to use AI to predict employee turnover. What data should they collect and why?"
      }}
    ],
 
    "all true/false questions": [
      {{
        "question": "Supervised learning requires labeled data.",
        "option 1": "True",
        "option 2": "False",
        "answer": "True"
      }}
    ],

    "all fill in the blanks questions": [
      {{
        "question": "In machine learning, ________ is used to evaluate the performance of a model.",
        "answer": "cross-vali dation"
      }}
    ]
  }}
}}

---
### Requirements per Question Type:
 
**MCQs:**
- Each must have exactly 4 options
- Exactly one correct answer (NEVER use "Both option X and Y" or "All of the above")
- Options should be plausible but clearly distinguishable
- All options must be grammatically parallel
- Focus on testing understanding, not memorization
- Each question should assess a single, clear concept
- DISTRACTORS must be plausible alternatives from the same conceptual domain (not random unrelated concepts)
- CRITICAL: When asking about benefits/advantages, all distractors should also be framed as benefits (not obvious negatives)
- CRITICAL: When asking about characteristics/features, all distractors should also be characteristics (not obviously wrong statements)
- Distractors should be plausible enough that someone who skimmed the content might choose them
- Example of GOOD distractor logic:
  * If correct answer is a feature → distractors should be other plausible features
  * If correct answer is a benefit → distractors should be other plausible benefits (never costs, limitations, or negatives)
  * If correct answer is a method → distractors should be other plausible methods
- Example of BAD distractor logic:
  * Question: "What is a benefit of X?" → Distractor: "Increased costs" ❌ (obviously negative)
  * Question: "What is a benefit of X?" → Distractor: "Limited functionality" ❌ (obviously negative)
  * Question about features → distractor is "does not work" or "is impossible"
  * Distractors that are obviously negative or undesirable

**Scenario Questions:**
- Present a real-world problem or situation relevant to the content domain
- Ask for application of concepts from the content
- MANDATORY: Include SPECIFIC, CONCRETE context:
  * Quantitative details (exact numbers, measurements, counts, percentages)
  * Named technologies, methods, or approaches mentioned in the content
  * Explicit constraints, requirements, or limitations
  * Specific data types, parameters, or conditions
- Scenarios must be answerable ONLY by someone who read the content (not general knowledge)
- Structure: [Context with specifics] + [Problem] + [Question requiring content knowledge]
- Example EXCELLENT structure: "[Role/Organization] has [specific quantities/data] and needs to [specific goal]. They face [specific constraints]. Which [concept from content] should they use and why?"
- Example POOR structure: "[Organization] is considering [topic]. What should they think about?" (too vague, no specifics)
- Avoid scenarios that can be answered with common sense or general domain knowledge
- No answer required (open-ended)

**True/False:**
- Simple statement format
- Include "option 1": "True" and "option 2": "False"
- Include the correct answer

**Fill in the Blanks:**
- Replace the MOST IMPORTANT keyword/phrase with a blank (________)
- The answer should be a specific term from the content
- Must require knowledge of the content to answer correctly
- The blank must represent a term that has ONLY ONE correct answer in the context of the sentence
- AVOID: Generic words, adjectives, or terms that could have multiple valid answers
- AVOID: Circular blanks where the answer word appears elsewhere in the question
- FOCUS ON: Technical terminology, specific names, formulas, protocols, exact values, or precise definitions that are unique to the content
 
---

### BEFORE SUBMITTING - VERIFY:
✓ I have used content from the ARTICLE to generate {mcq_from_article} MCQs, {sch_from_article} scenarios, {tf_from_article} true/false, {fillup_from_article} fill-ups
✓ I have used content from the PDF to generate {mcq_from_pdf} MCQs, {sch_from_pdf} scenarios, {tf_from_pdf} true/false, {fillup_from_pdf} fill-ups
✓ BOTH sources have been utilized
✓ Each person has unique questions
✓ Total counts are correct
✓ NO "Both option X and Y" answers exist
✓ NO two questions across all people are substantially similar
✓ All fill-blanks have only ONE possible correct answer
✓ NO fill-blank answers appear in the question text itself
✓ ZERO questions about metadata (publishers, authors, feedback, contact info, introductions, UI navigation, help features)
✓ ALL questions test TECHNICAL/SUBJECT MATTER knowledge only
✓ ALL MCQ distractors are plausible positive alternatives (not obviously negative options)
✓ ALL scenarios include specific numbers, technologies, or concrete requirements

---
 
### Final Instructions:
- Return ONLY valid JSON (no markdown, no explanations)
- Generate questions for ALL {people_in_batch} people
- Ensure EXACT question counts per person: {mcq_questions} MCQs, {sch_questions} scenarios, {truefalse_questions} true/false, {fillups_questions} fill-ups
- All string values must use double quotes
- Do NOT reduce counts under any circumstance

"""

            # Retry logic with parsing and cleanup
            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    start_time = time.time()
                    response = await asyncio.to_thread(model.invoke, unified_prompt)
                    elapsed = time.time() - start_time
                    logger.info(f"Batch {batch_num} completed in {elapsed:.2f}s")

                    raw_output = {"response": response.content}
                    clean_data = clean_llm_response(raw_output)
                    response_data = clean_data.get("response", {})

                    batch_output = {}

                    # ✅ Extract each person from response_data
                    if isinstance(response_data, dict):
                        for key, value in response_data.items():
                            if key.lower().startswith("person"):
                                local_num = int(key.split()[-1]) if " " in key else int(key.split("_")[-1])
                                global_num = start_person_num + local_num - 1
                                batch_output[f"person {global_num}"] = value

                    if not batch_output:
                        raise ValueError("Empty batch output from LLM.")

                    logger.info(f"Batch {batch_num} processed successfully with {len(batch_output)} people.")
                    return {"status": "success", "data": batch_output, "batch_num": batch_num}

                except Exception as e:
                    logger.warning(f"Batch {batch_num} attempt {attempt} failed: {e}")
                    if attempt == MAX_RETRIES:
                        return {"status": "error", "batch_num": batch_num, "error": str(e)}

        # Run batches in parallel (max 3 at a time)
        semaphore = asyncio.Semaphore(10)
 
        async def limited_batch(batch_index):
            async with semaphore:
                return await process_single_batch(batch_index)

        tasks = [limited_batch(i) for i in range(total_batches)]
        batch_results = await asyncio.gather(*tasks)

        # ✅ Merge all batches
        merged_output = {"people": total_people}
        for batch_result in batch_results:
            if batch_result and batch_result.get("status") == "success":
                merged_output.update(batch_result["data"])
            else:
                logger.error(f"Failed Batch: {batch_result}")

        logger.info(f"All batches merged. Total people generated: {len(merged_output) - 1}")

        # ✅ Return same format as original function
        print("merged_output:", merged_output)
        return {"response": merged_output}

    except Exception as e:
        logger.exception("Critical error in generate_for_batch")
        return {"response": {"error": str(e)}}