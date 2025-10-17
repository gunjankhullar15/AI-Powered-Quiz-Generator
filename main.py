from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import data_routers, llm_routers, test,weightage
from app.utils.db_seeder import seed_fixed_weightages

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: seed the database
    await seed_fixed_weightages()
    yield
    # Cleanup (if needed)
    pass

app = FastAPI(lifespan=lifespan)

# Register routers
app.include_router(data_routers.router, tags=["Data Processing"])
app.include_router(llm_routers.router, tags=["LLM"])
app.include_router(test.router, tags=["Tests"])
app.include_router(weightage.router, tags=["Weightages"])