from fastapi import FastAPI
from app.api import data_routers, llm_routers

app = FastAPI()

# Register routers
app.include_router(data_routers.router, tags=["Data Processing"])
app.include_router(llm_routers.router, tags=["LLM"])
