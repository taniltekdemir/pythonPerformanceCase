from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:1234@localhost/python_case_db"
    RABBITMQ_URL: str = "amqp://guest:guest@localhost//"

settings = Settings()