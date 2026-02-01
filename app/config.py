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

	@computed_field
	@property
	def database_url(self) -> str:
		return f"postgresql+psycopg://{self.database_username}:{self.database_password}@{self.database_hostname}:{self.database_port}/{self.database_name}"


settings = Settings()
