import json
import re
from fastapi import HTTPException

def clean_llm_response(raw_output: dict):
    """
    Clean and safely parse the LLM response JSON.
    Removes markdown code fences and extracts valid JSON.
    """
    if not raw_output or "response" not in raw_output:
        raise HTTPException(status_code=500, detail="Invalid LLM response structure.")

    cleaned = raw_output["response"]

    # Remove markdown code fences (```json ... ```)
    cleaned = re.sub(r"```(json)?", "", cleaned).strip("` \n")

    # Try direct JSON parsing
    try:
        return {"response": json.loads(cleaned)}
    except json.JSONDecodeError:
        # Try to extract only the JSON portion
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                return {"response": json.loads(match.group(0))}
            except Exception:
                pass

    raise HTTPException(status_code=500, detail="Failed to parse LLM response JSON.")

