from pydantic_settings import BaseSettings
from pydantic import computed_field


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    docshield_admin_pass: str
    docshield_developer_pass: str
    docshield_viewer_pass: str

    class Config:
        env_file = ".env"
        # Optional: Instead of adding fields,
        # you can tell Pydantic to ignore extras
        extra = "ignore"

    @computed_field
    @property
    def database_url(self) -> str:
        return "postgresql+psycopg://{user}:{pw}@{host}:{port}/{db}".format(
            user={self.database_username},
            pw={self.database_password},
            host={self.database_hostname},
            port={self.database_port},
            db={self.database_name}
            )


settings = Settings()
