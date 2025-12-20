from pydantic_settings import BaseSettings


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


settings = Settings()
