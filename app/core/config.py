from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	DB_HOST: str
	DB_PORT: int
	DB_USER: str
	DB_PASS: str
	DB_NAME: str
	JWT_SECRET: str

	@property
	def ASYNC_DATABASE_URL(self):
		return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

	@property
	def JWT_CONFIG(self):
		JWT_ALGORITHM = "HS256"
		JWT_EXP = 3600

		return self.JWT_SECRET, JWT_ALGORITHM, JWT_EXP

	model_config = SettingsConfigDict(env_file=".env")


settings = Settings()