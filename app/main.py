from fastapi import FastAPI
from app.api import data_routers, llm_routers, test, weightage
from contextlib import asynccontextmanager
from app.utils.db_seeder import seed_fixed_weightages
from app.services.weaviate_services import client
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
     # Startup: seed the database
    await seed_fixed_weightages()
    yield
    # Cleanup (if needed)
    pass


app = FastAPI(lifespan=lifespan)


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


@app.on_event("shutdown")
def shutdown_event():
    client.close()
    print("✅ Weaviate connection closed properly.")