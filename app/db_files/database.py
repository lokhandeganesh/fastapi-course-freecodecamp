from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.db_files.config import settings

# or we can import database_url from settings
SQLALCHEMY_DATABASE_URL = settings.database_url
# print(SQLALCHEMY_DATABASE_URL)

# Create the Async Engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    # echo=True,
    # future=True
)

# engine = create_async_engine(
#     SQLALCHEMY_DATABASE_URL,
#     pool_size=10,             # Keep 10 connections always ready
#     max_overflow=20,          # Allow up to 30 total connections during spikes
#     pool_timeout=30,          # Wait 30s for a connection before failing
#     pool_recycle=1800,        # Refresh connections every 30 mins (prevents stale links)
#     pool_pre_ping=True,       # Checks if connection is alive before using it
# )


# Setup the Async Session Factory
AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


# The Dependency for your Routers
async def get_db():
    print("Database connection was succesfull!")
    async with AsyncSessionFactory() as session:
        yield session
