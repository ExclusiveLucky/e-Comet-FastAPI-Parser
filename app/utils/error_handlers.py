from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from psycopg2 import OperationalError
import logging

# Логгер для записи ошибок
logger = logging.getLogger("app_errors")
logger.setLevel(logging.ERROR)

def init_error_handlers(app: FastAPI):
    """
    Инициализация централизованной обработки ошибок для FastAPI приложения.

    :param app: Экземпляр приложения FastAPI
    """

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc: HTTPException):
        """
        Обработчик HTTP-ошибок (например, 404, 500).

        :param request: Запрос, при котором произошла ошибка
        :param exc: Исключение HTTPException
        :return: JSON-ответ с детализированной ошибкой
        """
        logger.error(f"HTTP ошибка {exc.status_code}: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail}
        )

    @app.exception_handler(OperationalError)
    async def database_exception_handler(request, exc: OperationalError):
        """
        Обработчик ошибок подключения к базе данных.

        :param request: Запрос, при котором произошла ошибка
        :param exc: Исключение OperationalError
        :return: JSON-ответ с ошибкой подключения
        """
        logger.error("Ошибка базы данных: %s", str(exc))
        return JSONResponse(
            status_code=500,
            content={"message": "Ошибка подключения к базе данных. Пожалуйста, попробуйте позже."}
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc: Exception):
        """
        Глобальный обработчик ошибок для всех необработанных исключений.

        :param request: Запрос, при котором произошла ошибка
        :param exc: Исключение Exception
        :return: JSON-ответ с ошибкой сервера
        """
        logger.error("Необработанная ошибка: %s", str(exc))
        return JSONResponse(
            status_code=500,
            content={"message": "Произошла ошибка на сервере. Пожалуйста, попробуйте позже."}
        )
