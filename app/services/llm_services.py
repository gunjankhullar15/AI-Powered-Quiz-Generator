#from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
import os
import json
from dotenv import load_dotenv
from app.logs.logger_config import setup_logger
 
logger = setup_logger(__name__)
 
def generate_llm_output(topic: str,
                        results: str,
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
        model="gpt-4o-mini"
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
 
Content:
{results}
 
Level of difficulty: **Easy**
 
---
 
### Output Instructions:
1. Generate **unique** questions for each person — no repetition between people.
2. The **output must be valid JSON only** (no markdown, no explanations outside JSON).
3. Follow the **exact JSON structure** shown below.
4. All string values must be wrapped in **double quotes**.
5. Include accurate **answers**.
6. Skip any section if there’s insufficient data — do not leave blank or null fields.
7. Ensure that questions are content-based only — do not generate questions related to author names, page numbers, indices, or other metadata.
 
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
- Each question should have question number.
 
**2. Scenario-based Questions**
- Create {sch_n_questions} scenario-based questions per person.
- Each should present a real-world problem and ask for an applicable concept or solution.
- Each question should have question number.
 
**3. True/False Questions**
- Create {truefalse_n_questions} per person.
- Include two options ("True", "False"), a correct answer.
- Each question should have question number.
 
**4. Fill in the Blanks**
- Create {fillups_n_questions} per person.
- Include one blank, the correct answer.
- Each question should have question number.
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