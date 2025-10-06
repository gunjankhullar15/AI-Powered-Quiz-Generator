from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

def generate_llm_output(query: str, results: str):

    load_dotenv()  # Load environment variables from .env file

    model = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),  # 👉 move this to .env
        model_name="llama-3.3-70b-versatile"
    )

    mcq_n_questions = 5
    level = "hard"
    n_people = 2
    topic = "rag"
    sch_n_questions = 3
    truefalse_n_questions = 5
    fillups_n_questions = 3


    mcq_prompt = f"""
 
Consider you are the expert of creating mcq type question. you task is to create the {mcq_n_questions} number of mcq question from the given data.
 
the data is :
{results}
 
the level of the queston should be {level}
 
you have to create the questions for {n_people}  people in the following format :
 
example output format:
 
people : 1
[
question 1 : [question]
option 1 : [option]
option 2 : [option]
option 3 : [option]
option 4 : [option]
answer : [option]
explaination : [explaination]
 
question 2 : [question]
option 1 : [option]
option 2 : [option]
option 3 : [option]
option 4 : [option]
answer : [option]
explaination : [explaination]
]
 
people : 2
[
question 1 : [question]
option 1 : [option]
option 2 : [option]
option 3 : [option]
option 4 : [option]
answer : [option]
explaination : [explaination]
 
question 2 : [question]
option 1 : [option]
option 2 : [option]
option 3 : [option]
option 4 : [option]
answer : [option]
explaination : [explaination]
]
 
the question for different people should not be same. means the question should be unique for each person.
 
IMPORTANT : the output format only in json format only and do not include any thing extra in it.
 
"""

    sch_prompt = f"""

Consider you are the expert of creating scenario type question on the given topic. you task is to create the {sch_n_questions} number of scenario question from the given data on the topic : {query}.

the data is :
{results}

the level of the queston should be {level}

you have to create the questions for {n_people}  people in the following format :

example output format:

people : 1
[
question 1 : [question]

question 2 : [question]
]

people : 2
[
question 1 : [question]

question 2 : [question]
]

in the questions you have to give a condition and you have to ask which technology you should apply to solve this problem.

the question for different people should not be same. means the question should be unique for each person.

IMPORTANT : the output format only in json format only and do not include any thing extra in it.

"""
    
    true_false_prompt = f"""

Consider you are the expert of creating True/False type question. you task is to create the {truefalse_n_questions} number of True/False question from the given data.

the data is :
{results}

the level of the queston should be {level}

you have to create the questions for {n_people}  people in the following format :

example output format:

people : 1
[
question 1 : [question]
option 1 : [option]
option 2 : [option]
answer : [option]
explaination : [explaination]

question 2 : [question]
option 1 : [option]
option 2 : [option]
answer : [option]
explaination : [explaination]
]

people : 2
[
question 1 : [question]
option 1 : [option]
option 2 : [option]
answer : [option]
explaination : [explaination]

question 2 : [question]
option 1 : [option]
option 2 : [option]
answer : [option]
explaination : [explaination]
]

the question for different people should not be same. means the question should be unique for each person.

IMPORTANT : the output format only in json format only and do not include any thing extra in it.

"""
    
    fillups_prompt = f"""

Consider you are the expert of creating fill in the blanks type question. you task is to create the {fillups_n_questions} number of fill in the blanks question from the given data.

the data is :
{results}

the level of the queston should be {level}

you have to create the questions for {n_people}  people in the following format :

example output format:

people : 1
[
question 1 : [question]
answer : [option]
explaination : [explaination]

question 2 : [question]
answer : [option]
explaination : [explaination]
]

people : 2
[
question 1 : [question]
answer : [option]
explaination : [explaination]

question 2 : [question]
answer : [option]
explaination : [explaination]
]

the question for different people should not be same. means the question should be unique for each person.

IMPORTANT : the output format only in json format only and do not include any thing extra in it.

"""
    
    response = model.invoke(mcq_prompt)
    allmcq_questions = response.content

    response = model.invoke(sch_prompt)
    allsch_questions = response.content

    response = model.invoke(true_false_prompt)
    alltruefalse_questions = response.content

    finalprompt = f"""
You are an expert in generating well-structured question-and-answer sets from unorganized or scattered data.

Your task is to:
- Analyze the given data for three categories of questions: Multiple Choice Questions (MCQs), Scenario-based Questions, and True/False Questions.
- Convert all provided content into a clean, organized JSON format as shown below.

Here is the input data:

MCQ Questions Data:
{allmcq_questions}

Scenario-based Questions Data:
{allsch_questions}

True/False Questions Data:
{alltruefalse_questions}

fill in the blanks Questions Data:
{fillups_prompt}

Now, using the above data, generate a **structured JSON** in the following format:

{{
  "people": 1,
  "question type": "mcq",
  "all mcq questions": [
    {{
      "question": "What is the primary function of inductive bias in a learning algorithm?",
      "option 1": "To reduce the complexity of the hypothesis space",
      "option 2": "To increase the accuracy of the learner's predictions",
      "option 3": "To define the set of assumptions sufficient to deduce conclusions",
      "option 4": "To minimize training errors",
      "answer": "To reduce the complexity of the hypothesis space",
      "explanation": "Inductive bias restricts the hypothesis space, guiding learning towards more generalizable patterns."
    }}
  ],
  
  "question type": "scenario",
  "all scenario questions": [
    {{
      "question": "Imagine a company wants to use AI to predict employee turnover. What data should they collect and why?"
    }}
  ],
  
  "question type": "true/false",
  "all true/false questions": [
    {{
      "question": "Supervised learning requires labeled data.",
      "option 1": "True",
      "option 2": "False",
      "answer": "True",
      "explanation": "Supervised learning depends on labeled datasets to train models accurately."
    }}
  ],

  "question type": "fill in the blanks",
    "all fill in the blanks questions": [
        {{
        "question": "In machine learning, ________ is used to evaluate the performance of a model.",
        "answer": "cross-validation",
        "explanation": "Cross-validation helps in assessing how the results of a statistical analysis will generalize to an independent dataset."
        }}
    ]
}}

IMPORTANT RULES:
1. The output must be in **valid JSON format** — no extra text, no markdown, no explanations outside the JSON.
2. Ensure all strings are properly enclosed in double quotes.
3. Maintain consistent key names exactly as shown.
4. Only include questions and answers that exist in the given data.
5. If any data is missing, skip it — do not leave blank or null fields.
6. Include all the questions for all the people specified.

Output only the final JSON structure.
"""


    
    
    prompt = f"""

give me proper answer for the following question on the bases of given content:
question : {query}


content : {results}

"""
    
    

    response1 = model.invoke(finalprompt)
    return {"response": response1.content}
