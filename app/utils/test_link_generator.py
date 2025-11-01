# app/utils/test_link_generator.py
from urllib.parse import urlencode
from app.config.pydantic_config import settings

def generate_test_link(test_id: int) -> str:

    base_url = settings.BASE_URL

    if not base_url:
        raise ValueError("BASE_URL not configured in .env file.")
    if not isinstance(test_id, int) or test_id <= 0:
        raise ValueError("Invalid test_id provided.")

    query_params = {"test_id": test_id}
    test_url = f"{base_url}?{urlencode(query_params)}"
    return test_url