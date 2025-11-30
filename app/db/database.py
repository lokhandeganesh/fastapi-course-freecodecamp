from functools import lru_cache
from psycopg_pool import AsyncConnectionPool
from app.db.db_config import settings

conninfo = f"user={settings.database_username} password={settings.database_password} host={settings.database_hostname} port={settings.database_port} dbname={settings.database_name}"

@lru_cache()
def get_async_pool():
	return AsyncConnectionPool(conninfo = conninfo, open = False)

