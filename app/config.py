"""
Модуль, содержащий конфигурационные настройки приложения
"""
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """
    Конфигурационные настройки приложения, загружаемые из виртуального окружения и .env файла
    """
    # pylint: disable=too-few-public-methods
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        """Вложенный класс, содержащий дополнительные настройки конфигурации"""
        env_file = ".env"
        extra = "ignore"

settings = Settings()
