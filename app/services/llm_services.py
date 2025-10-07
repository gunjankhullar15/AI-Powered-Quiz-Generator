from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

def generate_llm_output(topic: str,
                        results: str,
                        mcq_questions: int,
                        sch_questions: int,
                        truefalse_questions: int,
                        fillups_questions: int,
                        question_level: str,
                        total_people: int):

    load_dotenv()  # Load environment variables from .env file

    model = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),  # 👉 move this to .env
        model_name="llama-3.3-70b-versatile"
    )

    mcq_n_questions = mcq_questions
    level = question_level
    n_people = total_people
    # topic = "rag"
    sch_n_questions = sch_questions
    truefalse_n_questions = truefalse_questions
    fillups_n_questions = fillups_questions    
    
    prompt = f"""

give me proper answer for the following question on the bases of given content:
question : {topic}


content : {results}

"""
    


    unified_prompt = f"""
You are an expert question generator specializing in multiple formats of assessment questions.  
Your task is to create **{mcq_n_questions} MCQs**, **{sch_n_questions} scenario-based questions**, **{truefalse_n_questions} true/false questions**, and **{fillups_n_questions} fill-in-the-blanks questions** for **{n_people} different people** based on the given content.

---
### Context:
Topic: {topic}

Content:
{results}

Level of difficulty: {level}
---

### Output Instructions:
1. Generate **unique** questions for each person — no repetition between people.
2. The **output must be a valid JSON only** (no markdown, no explanations).
3. Follow the **exact JSON structure** shown below.
4. Ensure all string values are wrapped in **double quotes**.
5. Include clear and accurate **answers** and **explanations**.
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
      "explanation": "Cross-validation helps assess how results generalize to an independent dataset."
    }}
  ]
}}

---

### Requirements per Question Type:

**1. MCQs**
- Create {mcq_n_questions} MCQs per person.
- Each MCQ should have 4 options, one correct answer, and a brief explanation.

**2. Scenario-based Questions**
- Create {sch_n_questions} scenario-based questions per person.
- Each question should describe a real-world situation and ask what technology/method/concept to apply.

**3. True/False Questions**
- Create {truefalse_n_questions} questions per person.
- Include two options ("True", "False"), the correct answer, and a short explanation.

**4. Fill in the Blanks**
- Create {fillups_n_questions} questions per person.
- Each should have one blank and a correct answer with a brief explanation.

---

### Final Instruction:
Return only the final structured JSON (for both people, each having all four question types).  
Do **not** include any text outside the JSON.
"""
    

    response1 = model.invoke(unified_prompt)
    return {"response": response1.content}
