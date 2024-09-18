import requests
import os
import psycopg2
from psycopg2.extras import execute_values
from fastapi import HTTPException
from app.database import get_db_connection

GITHUB_API_URL = "https://api.github.com/search/repositories"

def fetch_top_repos():
    """
    Получает топ-100 репозиториев с GitHub по количеству звезд.

    :return: Список объектов репозиториев
    :raises HTTPException: В случае ошибки при выполнении запроса к GitHub API
    """
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {os.getenv('GITHUB_API_TOKEN')}"
    }
    
    params = {
        "q": "stars:>1",
        "sort": "stars",
        "per_page": 100
    }

    response = requests.get(GITHUB_API_URL, headers=headers, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Ошибка при запросе к GitHub API")

    return response.json().get("items", [])


def save_to_db(repos):
    """
    Сохраняет список репозиториев в базу данных PostgreSQL.
    
    :param repos: Список репозиториев для сохранения
    :raises HTTPException: В случае ошибки при сохранении данных в базу данных
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            query = """
            INSERT INTO repos (repo_name, owner, stars, watchers, forks, open_issues, language, position_cur, position_prev)
            VALUES %s
            ON CONFLICT (repo_name) DO UPDATE 
            SET stars = EXCLUDED.stars, watchers = EXCLUDED.watchers, forks = EXCLUDED.forks, open_issues = EXCLUDED.open_issues, position_cur = EXCLUDED.position_cur
            """
            values = [
                (
                    repo['full_name'], repo['owner']['login'], repo['stargazers_count'], 
                    repo['watchers_count'], repo['forks_count'], repo['open_issues_count'], 
                    repo['language'], idx + 1, None
                )
                for idx, repo in enumerate(repos)
            ]
            
            execute_values(cursor, query, values)
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Ошибка при сохранении данных в базу")
    finally:
        conn.close()


def run():
    """
    Основная функция для выполнения парсинга топ-репозиториев с GitHub и сохранения их в базу данных.
    """
    try:
        repos = fetch_top_repos()
        if repos:
            save_to_db(repos)
        else:
            raise HTTPException(status_code=404, detail="Не удалось получить репозитории")
    except Exception as e:
        # Логирование ошибки (добавьте реальный логгер в вашем проекте)
        print(f"Ошибка во время выполнения парсинга: {e}")
