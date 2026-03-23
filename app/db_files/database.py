from collections.abc import AsyncGenerator
from fastapi.exceptions import ResponseValidationError
# import asyncio

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db_files.config import settings
from app.logging.logger import logger

engine = create_async_engine(
    settings.asyncpg_url.unicode_string(),
    future=True,
    echo=True,
)

# expire_on_commit=False will prevent attributes from being expired
# after commit.
AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

print("Database connection was succesfull!")


# Dependency
async def get_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError:
            # Re-raise SQLAlchemy errors to be handled by the global handler
            raise
        except Exception as ex:
            # Only log actual database-related issues, not response validation
            if not isinstance(ex, ResponseValidationError):
                logger.error(f"Database-related error: {repr(ex)}")
            raise  # Re-raise to be handled by appropriate handlers

# async def setup_db():
#     async with engine.begin() as conn:
#         await conn.execute(text("CREATE SCHEMA IF NOT EXISTS course"))

# if __name__ == "__main__":
#     asyncio.run(setup_db())
