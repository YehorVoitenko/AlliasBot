from sqlalchemy import update

from Allias.models.team import Team
from Allias.repositories.base import Session

session = Session()


def update_team_score_by_id(team_id: int, score: int):
    session \
        .execute(update(Team)
                 .where(Team.id == team_id)
                 .values(score=score))
