from fastapi import APIRouter, HTTPException
from app.database import get_db_connection

router = APIRouter()

@router.get("/{owner}/{repo}/activity")
def get_repo_activity(owner: str, repo: str, since: str, until: str):
    """
    Возвращает активность репозитория (по дням) за указанный период времени.
    
    :param owner: Владелец репозитория
    :param repo: Название репозитория
    :param since: Начальная дата
    :param until: Конечная дата
    :return: Список коммитов и авторов за каждый день
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            query = """
            SELECT date, COUNT(commit_id) AS commits, array_agg(author) AS authors
            FROM commits
            WHERE repo_name = %s AND owner = %s AND date BETWEEN %s AND %s
            GROUP BY date
            """
            cursor.execute(query, (repo, owner, since, until))
            activity = cursor.fetchall()
            if not activity:
                raise HTTPException(status_code=404, detail="Данные активности не найдены")
    finally:
        conn.close()
    
    return activity
