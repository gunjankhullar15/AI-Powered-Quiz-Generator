from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
 
def generate_llm_output(topic: str,
                        results: str,
                        mcq_questions: int,
                        sch_questions: int,
                        truefalse_questions: int,
                        fillups_questions: int,
                        total_people: int,
                        match_questions: int):
 
    load_dotenv()  # Load environment variables from .env file
 
    model = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),  # 👉 move this to .env
        model_name="llama-3.3-70b-versatile"
    )
 
    mcq_n_questions = mcq_questions
    n_people = total_people
    # topic = "rag"
    sch_n_questions = sch_questions
    truefalse_n_questions = truefalse_questions
    fillups_n_questions = fillups_questions
    match_n_questions = match_questions    
   
    
   
    unified_prompt = f"""
You are an expert question generator specializing in multiple formats of assessment questions.  
Your task is to create the following types of questions for **{n_people} different people** based on the given content:
 
- **{mcq_n_questions} MCQs**
- **{sch_n_questions} scenario-based questions**
- **{truefalse_n_questions} true/false questions**
- **{fillups_n_questions} fill-in-the-blanks questions**
- **{match_n_questions} match-the-following questions**
 
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
5. Include accurate **answers** and **explanations**.
6. Skip any section if there’s insufficient data — do not leave blank or null fields.
 
---
 
### Output JSON Format Example:
 
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
      "Source": "content above"
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
      "Source": "content above"
    }}
  ],
 
  "question type": "fill in the blanks",
  "all fill in the blanks questions": [
    {{
      "question": "In machine learning, ________ is used to evaluate the performance of a model.",
      "answer": "cross-validation",
      "Source": "LLM knowledge"
    }}
  ],
 
  "question type": "match the following",
  "all match the following questions": [
    {{
      "question 1": "Match the following AI concepts with their descriptions.",
      "pairs": {{
        "Supervised Learning": "Uses labeled data to train a model",
        "Unsupervised Learning": "Finds hidden patterns in unlabeled data",
        "Reinforcement Learning": "Learns by receiving rewards or penalties"
      }},
      "answer": {{
        "Supervised Learning": "Uses labeled data to train a model",
        "Unsupervised Learning": "Finds hidden patterns in unlabeled data",
        "Reinforcement Learning": "Learns by receiving rewards or penalties"
      }},
      "Source": "LLM knowledge"
    }}
  ]
}}
 
---
 
### Requirements per Question Type:
 
**1. MCQs**
- Create {mcq_n_questions} MCQs per person.
- Each MCQ should have 4 options, one correct answer, and source which tell how this question is made weather it is made from the given content or these question is generated from the llm knowledge.
- Each question should have question number.
 
**2. Scenario-based Questions**
- Create {sch_n_questions} scenario-based questions per person.
- Each should present a real-world problem and ask for an applicable concept or solution.
- Each question should have question number.
 
**3. True/False Questions**
- Create {truefalse_n_questions} per person.
- Include two options ("True", "False"), a correct answer, and source which tell how this question is made weather it is made from the given content or these question is generated from the llm knowledge.
- Each question should have question number.
 
**4. Fill in the Blanks**
- Create {fillups_n_questions} per person.
- Include one blank, the correct answer, and source which tell how this question is made weather it is made from the given content or these question is generated from the llm knowledge.
- Each question should have question number.
 
**5. Match the Following**
- Create {match_n_questions} match-the-following questions per person.
- Each should contain a list of items to match with corresponding options and have total 4 match the following per question.
- Include answers and source which tell how this question is made weather it is made from the given content or these question is generated from the llm knowledge.
- In the question you have to suffle the pairs so that the answer will not come in front of the pair in the question.
- Each question should have question number.
- Format must follow JSON strictly as shown above.
 
---
 
### Final Instruction:
Return only the **final structured JSON** for all people — each containing all five question types.  
Do **not** include anything outside the JSON.
"""
 
   
 
    response1 = model.invoke(unified_prompt)
    return {"response": response1.content}
 
 
