from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import data_routers, llm_routers, test,weightage,employee,questions,instructions
from fastapi.middleware.cors import CORSMiddleware
from app.utils.db_seeder import seed_fixed_weightages

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: seed the database
    await seed_fixed_weightages()
    yield
    # Cleanup (if needed)
    pass

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:42000",  # Angular dev server
    
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(data_routers.router, tags=["Data Processing"])
app.include_router(llm_routers.router, tags=["LLM"])
app.include_router(test.router, tags=["Tests"])
app.include_router(weightage.router, tags=["Weightages"])
app.include_router(employee.router, tags=["Employees"])
app.include_router(questions.router,tags=["Questions"])
app.include_router(instructions.router,tags=["Instructions"])