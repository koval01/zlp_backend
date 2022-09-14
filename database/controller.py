import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

Base = declarative_base()

engine = create_async_engine(
    os.getenv("DATABASE_URL")
)

async_session = AsyncSession(engine, expire_on_commit=False)

async_sql_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
