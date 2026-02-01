from pydantic_config import SettingsModel, SettingsConfig

class Settings(SettingsModel):
	database_hostname: str
	database_port: int
	database_password: str
	database_name: str
	database_username: str

	secret_key: str
	algorithm: str
	access_token_expire_minutes: int

	redis_host: str
	redis_port: int
	redis_password: str
	redis_decode_response: bool
	redis_db: int

	docshield_admin_pass: str
	docshield_developer_pass: str
	docshield_viewer_pass: str

	model_config = SettingsConfig(
		# env_file='.env',
		config_file='./app/secretes/config.toml',
		config_file_required=True,
	)

settings = Settings()
# print(settings)