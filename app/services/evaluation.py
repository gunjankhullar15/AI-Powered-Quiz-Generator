import json
import re
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
 
def making_llm_output_into_json(llm_output : str):
   
    cleaned = re.sub(r"^```[a-zA-Z]*|```$", "", llm_output.strip())
   
    try:
        json_data = json.loads(cleaned)
        return json_data
    except json.JSONDecodeError as e:
        return {"error": "Invalid JSON format", "details": str(e)}
   
def calculating_score(data : dict):
 
    totals_marks = {q_type: sum(questions.values()) for q_type, questions in data.items()}
 
    # Add overall total marks
    totals_marks['Total Marks'] = sum(totals_marks.values())
 
    return totals_marks
 
 
def evaluating_user_answers(user_answer : str, mcq_marks : int, truefalse_marks : int, fillups_marks : int, scenario_based_marks : int):
   
    load_dotenv()
 
    model = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),  # 👉 move this to .env
        model_name="llama-3.3-70b-versatile"
    )
   
    prompt = f"""
 
consider you are the expert of evaluating the questions and answer attempted by the user.
 
i will give you the content which contain the question, answer given by use and the correct answer of the given question. keep in mind that their are 1 or more then 1 set of questions are present.
 
the type of question are MCQ, True and False, fill in the blanks and scenario based question.
 
MCQ, True and False, fill in the blanks are in the form of question, answer given by user, correct answer and scenario based question are given in the form of question, answer given by user.
 
the content is {user_answer}
 
the MCQ are {mcq_marks} marks, the true and false are {truefalse_marks} marks, fill ups are {fillups_marks} marks and the scenario based question are of {scenario_based_marks} marks.
 
in fill in the blanks you have to check the answer is same to the correct answer or not if not then the answer given by the user is similar or related to the correct answer or not, and for the scenario based question you have to check on the bases of Relevance, Correctness, Completeness of the answer given by the user is correct or not if correct then how much it is correct.
 
for MCQ, True and false, fill in the blanks and scenario based question you have to give me the marks in the given format:
 
example of output format:
 
MCQ:
1 : 1
2 : 0
3 : 1
4 : 1
 
True and false:
1 : 1
2 : 0
3 : 0
4 : 1
 
fill in the blanks:
1 : 1
2 : 0
3 : 0
4 : 1
 
scenario based:
1 : 3
2 : 2
3 : 2.5
4 : 1.5
 
 
important note:
- you have to give me the marks of MCQ, True and false, fill in the blanks from 1 means the output should be 1 or 0.
- you have to give me the marks of scenario based from {scenario_based_marks} means eg : 2,2.5,3,1.
- also keep in mind that if the answer of fill in the blanks and scenario based question is not related then simply give the marks 0.
- Only give the output do not give the explanation.
- the output should be in strict json format only.
 
"""
   
    response = model.invoke(prompt)
 
    dict_response = making_llm_output_into_json(response.content)
 
    user_marks = calculating_score(dict_response)
 
    return user_marks
 