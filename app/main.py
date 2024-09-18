from fastapi import FastAPI
from app.routers import repos, activity
from app.utils.error_handlers import init_error_handlers
import logging

# Настройка логирования
logging.basicConfig(filename="app.log", level=logging.ERROR)

# Инициализируем FastAPI приложение
app = FastAPI(
    title="GitHub Repos API",
    description="API для отображения топа публичных репозиториев и их активности",
    version="1.0.0"
)

# Подключаем маршруты для репозиториев и активности
app.include_router(repos.router, prefix="/api/repos", tags=["repos"])
app.include_router(activity.router, prefix="/api/repos", tags=["activity"])

# Подключаем обработчики ошибок
init_error_handlers(app)