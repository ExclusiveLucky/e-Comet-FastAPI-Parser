import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

class Settings:
    """
    Класс для управления настройками приложения. 
    Все переменные окружения и конфигурации должны быть определены здесь.
    """
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgres://user:password@localhost:5432/repos_db")

settings = Settings()