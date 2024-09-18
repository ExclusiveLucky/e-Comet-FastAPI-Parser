import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import settings
from fastapi import HTTPException

def get_db_connection():
    """
    Устанавливает соединение с базой данных PostgreSQL.
    Использует настройки из переменной окружения DATABASE_URL.
    
    :return: Объект соединения с базой данных
    :raises HTTPException: Если не удалось подключиться к базе данных
    """
    try:
        conn = psycopg2.connect(settings.DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail="Ошибка подключения к базе данных")