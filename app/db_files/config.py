from pydantic import PostgresDsn, RedisDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    test_database_name: str
    database_username: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    docshield_admin_pass: str
    docshield_developer_pass: str
    docshield_viewer_pass: str

    redis_host: str
    redis_port: int
    redis_db: str
    redis_password: str
    redis_decode_response: bool

    class Config:
        env_file = ".env"
        # Optional: Instead of adding fields,
        # you can tell Pydantic to ignore extras
        extra = "ignore"

    @computed_field
    @property
    def database_url(self) -> str:
        return "postgresql+psycopg://{user}:{pw}@{host}:{port}/{db}".format(
            user=self.database_username,
            pw=self.database_password,
            host=self.database_hostname,
            port=self.database_port,
            db=self.database_name
            )

    @computed_field
    @property
    def redis_url(self) -> RedisDsn:
        """
        This is a computed field that generates a RedisDsn URL for redis-py.

        The URL is built using the MultiHostUrl.build method, which takes the following parameters:
        - scheme: The scheme of the URL. In this case, it is "redis".
        - host: The host of the Redis database, retrieved from the REDIS_HOST environment variable.
        - port: The port of the Redis database, retrieved from the REDIS_PORT environment variable.
        - path: The path of the Redis database, retrieved from the REDIS_DB environment variable.

        Returns:
            RedisDsn: The constructed RedisDsn URL for redis-py.
        """
        return MultiHostUrl.build(
            scheme="redis",
            host=self.redis_host,
            port=self.redis_port,
            path=self.redis_db,
            password=self.redis_password
        )

    @computed_field
    @property
    def asyncpg_url(self) -> PostgresDsn:
        """
        This is a computed field that generates a PostgresDsn URL for asyncpg.

        The URL is built using the MultiHostUrl.build method, which takes the following parameters:
        - scheme: The scheme of the URL. In this case, it is "postgresql+asyncpg".
        - username: The username for the Postgres database, retrieved from the POSTGRES_USER environment variable.
        - password: The password for the Postgres database, retrieved from the POSTGRES_PASSWORD environment variable.
        - host: The host of the Postgres database, retrieved from the POSTGRES_HOST environment variable.
        - path: The path of the Postgres database, retrieved from the POSTGRES_DB environment variable.

        Returns:
            PostgresDsn: The constructed PostgresDsn URL for asyncpg.
        """
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.database_username,
            password=self.database_password,
            host=self.database_hostname,
            path=self.database_name,
        )

    @computed_field
    @property
    def test_asyncpg_url(self) -> PostgresDsn:
        """
        This is a computed field that generates a PostgresDsn URL for the test database using asyncpg.

        The URL is built using the MultiHostUrl.build method, which takes the following parameters:
        - scheme: The scheme of the URL. In this case, it is "postgresql+asyncpg".
        - username: The username for the Postgres database, retrieved from the POSTGRES_USER environment variable.
        - password: The password for the Postgres database, retrieved from the POSTGRES_PASSWORD environment variable.
        - host: The host of the Postgres database, retrieved from the POSTGRES_HOST environment variable.
        - path: The path of the Postgres test database, retrieved from the POSTGRES_TEST_DB environment variable.

        Returns:
            PostgresDsn: The constructed PostgresDsn URL for the test database with asyncpg.
        """
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.database_username,
            password=self.database_password,
            host=self.database_hostname,
            path=self.test_database_name,
        )

    @computed_field
    @property
    def postgres_url(self) -> PostgresDsn:
        """
        This is a computed field that generates a PostgresDsn URL

        The URL is built using the MultiHostUrl.build method, which takes the following parameters:
        - scheme: The scheme of the URL. In this case, it is "postgres".
        - username: The username for the Postgres database, retrieved from the POSTGRES_USER environment variable.
        - password: The password for the Postgres database, retrieved from the POSTGRES_PASSWORD environment variable.
        - host: The host of the Postgres database, retrieved from the POSTGRES_HOST environment variable.
        - path: The path of the Postgres database, retrieved from the POSTGRES_DB environment variable.

        Returns:
            PostgresDsn: The constructed PostgresDsn URL.
        """
        return MultiHostUrl.build(
            scheme="postgres",
            username=self.database_username,
            password=self.database_password,
            host=self.database_hostname,
            path=self.database_name,
        )


settings = Settings()
