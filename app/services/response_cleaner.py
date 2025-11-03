# import json
# import re
# from fastapi import HTTPException
 
# def clean_llm_response(raw_output: dict):
#     """
#     Clean and safely parse the LLM response JSON.
#     Removes markdown code fences and extracts valid JSON.
#     """
#     if not raw_output or "response" not in raw_output:
#         raise HTTPException(status_code=500, detail="Invalid LLM response structure.")
 
#     cleaned = raw_output["response"]
 
#     # Remove markdown code fences (```json ... ```)
#     cleaned = re.sub(r"```(json)?", "", cleaned).strip("` \n")
 
#     # Try direct JSON parsing
#     try:
#         return {"response": json.loads(cleaned)}
#     except json.JSONDecodeError:
#         # Try to extract only the JSON portion
#         match = re.search(r"\{.*\}", cleaned, re.DOTALL)
#         if match:
#             try:
#                 return {"response": json.loads(match.group(0))}
#             except Exception:
#                 pass
 
#     raise HTTPException(status_code=500, detail="Failed to parse LLM response JSON.")


# import json
# import re
# from fastapi import HTTPException

# def clean_llm_response(raw_output: dict):
#     """
#     Clean and safely parse the LLM response JSON.
#     Handles multiple JSON objects or text-wrapped outputs.
#     """
#     if not raw_output or "response" not in raw_output:
#         raise HTTPException(status_code=500, detail="Invalid LLM response structure.")

#     cleaned = raw_output["response"]

#     # Remove markdown formatting like ```json ... ```
#     cleaned = re.sub(r"```(json)?", "", cleaned).strip("` \n")

#     # Fix common JSON issues (smart quotes, trailing commas)
#     cleaned = cleaned.replace("’", "'").replace("“", '"').replace("”", '"')

#     # Try to wrap multiple objects into a JSON array if needed
#     if "}, {" in cleaned and not cleaned.strip().startswith("["):
#         cleaned = f"[{cleaned}]"

#     # Try JSON parsing
#     try:
#         parsed = json.loads(cleaned)
#     except json.JSONDecodeError:
#         # Try extracting multiple objects
#         matches = re.findall(r"\{.*?\}", cleaned, re.DOTALL)
#         if matches:
#             try:
#                 parsed = [json.loads(m) for m in matches]
#             except Exception as e:
#                 raise HTTPException(status_code=500, detail=f"Partial JSON parse failed: {str(e)}")
#         else:
#             raise HTTPException(status_code=500, detail="Failed to parse LLM JSON output.")

#     # Always wrap in consistent dict structure
#     return {"response": parsed}


import json
import re
from fastapi import HTTPException

def clean_llm_response(raw_output: dict):
    """
    Clean and safely parse the LLM response JSON.
    Removes markdown code fences and extracts valid JSON.
    Fixes small formatting errors like duplicate keys or missing commas.
    """
    if not raw_output or "response" not in raw_output:
        raise HTTPException(status_code=500, detail="Invalid LLM response structure.")

    cleaned = raw_output["response"]

    # Remove markdown code fences
    cleaned = re.sub(r"```(json)?", "", cleaned).strip("` \n")

    # Fix common issues: duplicate keys and missing commas between objects
    # Remove consecutive duplicate keys like `"answer": "x" "answer": "y"`
    cleaned = re.sub(r'"(\w+)"\s*:\s*"([^"]+)"\s*"(\w+)"\s*:', r'"\1": "\2", "\3":', cleaned)

    # Try direct parse
    try:
        return {"response": json.loads(cleaned)}
    except json.JSONDecodeError:
        # Try extracting JSON portion
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            json_str = match.group(0)
            # Apply same cleanup to extracted portion
            json_str = re.sub(r'"(\w+)"\s*:\s*"([^"]+)"\s*"(\w+)"\s*:', r'"\1": "\2", "\3":', json_str)
            try:
                return {"response": json.loads(json_str)}
            except json.JSONDecodeError as e:
                raise HTTPException(status_code=500, detail=f"Partial JSON parse failed: {str(e)}")

    raise HTTPException(status_code=500, detail="Failed to parse LLM response JSON.")
