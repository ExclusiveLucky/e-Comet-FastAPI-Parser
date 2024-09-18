class Repo:
    """
    Модель данных для репозитория. 
    Определяет основные поля, используемые в API и базе данных.
    """
    def __init__(self, repo_name: str, owner: str, stars: int, watchers: int, 
                 forks: int, open_issues: int, language: str, 
                 position_cur: int, position_prev: int):
        self.repo_name = repo_name
        self.owner = owner
        self.stars = stars
        self.watchers = watchers
        self.forks = forks
        self.open_issues = open_issues
        self.language = language
        self.position_cur = position_cur
        self.position_prev = position_prev
