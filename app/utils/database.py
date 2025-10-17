import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Create Base class for models with table extension enabled
metadata = MetaData()
Base = declarative_base(metadata=metadata)

load_dotenv()

# Get environment variables
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# URL encode the password
encoded_password = quote_plus(str(DB_PASSWORD))

# Create both sync and async database URLs
#SYNC_SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
ASYNC_SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engines
# sync_engine = create_engine(SYNC_SQLALCHEMY_DATABASE_URL, echo=True)
async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL, echo=True)

# Create session factories
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

# Dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()