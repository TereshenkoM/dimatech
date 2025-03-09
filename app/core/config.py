from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	DB_HOST: str
	DB_PORT: int
	DB_USER: str
	DB_PASS: str
	DB_NAME: str
	JWT_SECRET: str
	JWT_ALGORITHM:str = "HS256"
	JWT_EXP: int = 36000
	SECRET_KEY: str

	@property
	def ASYNC_DATABASE_URL(self):
		return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

	@property
	def JWT_CONFIG(self):
		return self.JWT_SECRET, self.JWT_ALGORITHM, self.JWT_EXP

	@property
	def SECRET_KEY(self):
		return self.SECRET_KEY

	model_config = SettingsConfigDict(env_file=".env")


settings = Settings()