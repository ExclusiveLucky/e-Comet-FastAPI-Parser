from fastapi import APIRouter, Query, HTTPException
from app.database import get_db_connection
from app.schemas.repo import RepoSchema

router = APIRouter()

@router.get("/top100", response_model=list[RepoSchema])
def get_top_100_repos(order_by: str = Query("stars", enum=["stars", "forks", "watchers"])):
    """
    Возвращает топ-100 репозиториев с GitHub, отсортированных по количеству звезд, форков или просмотров.
    
    :param order_by: Поле для сортировки (stars, forks, watchers)
    :return: Список репозиториев
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            query = f"SELECT * FROM repos ORDER BY {order_by} DESC LIMIT 100"
            cursor.execute(query)
            repos = cursor.fetchall()
            if not repos:
                raise HTTPException(status_code=404, detail="Репозитории не найдены")
    finally:
        conn.close()
    
    return repos
