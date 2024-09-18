
from pydantic import BaseModel
from typing import Optional

class RepoSchema(BaseModel):
    """
    Pydantic-схема для валидации данных о репозитории.
    """
    repo_name: str
    owner: str
    position_cur: int
    position_prev: Optional[int]
    stars: int
    watchers: int
    forks: int
    open_issues: int
    language: Optional[str]

    class Config:
        orm_mode = True
